from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from core.decorators import define_usage
from .models import Journal, process_journal_name
from core.models import Metrics
from users.models import Subscriber
from django.conf import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import delorean
import pickle
import os
from django.utils import timezone


#HELPER METHODS
def to_human_readable(d, tz):
    s = str(d.shift(tz).truncate("minute").format_datetime()).split(":")
    return "Recorded " + ":".join(s[:-1]) + s[-1][-3:] + ":"


def write_to_gdoc(docID, message, service):
    print("write called")
    test = delorean.Delorean()
    t = "US/Central" #user.timezone pytz.all_timezones
    date_time = to_human_readable(test, t)
    print(date_time)
    requests = [{'insertText': {'location': {'index': 1},
                                'text': message+"\n\n"}},
                {'insertText': {'location': {'index': 1},
                                'text': date_time+"\n\n"}}]
    service.documents().batchUpdate(documentId=docID, body={'requests': requests}).execute()
    print("write complete")


#url /journals/api/
@define_usage(returns={"url_usage": "Dict"})
@api_view(["GET"])
@permission_classes((AllowAny,))
def api_root(request):
    details = {}
    for item in list(globals().items()):
        if item[0][0:4] == "api_":
            if hasattr(item[1], "usage"):
                details[reverse(item[1].__name__)] = item[1].usage
    return Response(details)


#url /journals/api/entry
@define_usage(params={"names": "String", "message": "String", "phone": "String", "api_key": "String"},
              returns={"Error": "String"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_journal_entry(request):
    print("journal entry called")
    if request.data["api_key"] != settings.API_KEY: #will be env variable in settings
        return Response({"Error": "API Key Incorrect"})
    try:
        met = Metrics.objects.get(current=True)
        met.log_journal_entry()
    except:
        pass #never fail user request because of a metrics error
    try:
        subscriber = Subscriber.objects.get(phone=request.data["phone"])
        user_journals = subscriber.journal_set.all()
    except:
        return Response({"Error": "Subscriber with that phone number not found"})
    try:
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(settings.BASE_DIR, str(subscriber.id) + 'token.pickle')):
            with open(os.path.join(settings.BASE_DIR, str(subscriber.id) + 'token.pickle'), 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in. ##RIGHT NOW JUST WRITES TO ONE ACCOUNT
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                f = open(os.path.join(settings.BASE_DIR, 'credentials.json'), 'w') #THIS IS SO JANKY but we can't keep this as a file in the codebase
                f.write(settings.GOOGLE_CREDENTIALS)
                f.close()
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(settings.BASE_DIR, 'credentials.json'),
                    ['https://www.googleapis.com/auth/documents'])
                os.remove(os.path.join(settings.BASE_DIR, 'credentials.json')) #END JANK
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(os.path.join(settings.BASE_DIR, str(subscriber.id) + 'token.pickle'), 'wb') as token:
                pickle.dump(creds, token)
        service = build('docs', 'v1', credentials=creds)
    except:
        return Response({"Error": "Google Service Initialization Error"})
    try:
        names = request.data["names"].split(",")
    except:
        return Response({"Error": "names parameter not included in call"})
    if names == [""]:
        names = ["SMSJournal"]
    print(request.data["phone"])
    print("here")
    print(names)
    for name in names:
        print(name)
        try:
            print("try")
            journal = user_journals.get(name=process_journal_name(name))
            print("got journal")
            write_to_gdoc(journal.google_docs_id, request.data["message"], service)
        except:
            print("except")
            doc = service.documents().create(body={"title": name}).execute()
            print("doc made")
            print(doc["documentId"])
            print(doc.get("title"))
            write_to_gdoc(doc["documentId"], request.data["message"], service)
            print("written")
            journal = Journal(subscriber=subscriber,
                              name=process_journal_name(name),
                              google_docs_id=doc["documentId"])
            journal.save()
        subscriber.last_entry = timezone.now()
        subscriber.total_entries = subscriber.total_entries + 1
        subscriber.save()
        return Response({})
