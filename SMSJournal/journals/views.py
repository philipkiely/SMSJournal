from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from core.decorators import define_usage
from .models import Journal
from .serializers import JournalSerializer


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


#url /journals/api/create_journal
@define_usage(params={"name": "String", "id": "String", "phone_number": "Integer", "api_key": "String"},
              returns={"journal_info": "Dict"})
@api_view(["POST"]) #PUT?
@permission_classes((AllowAny,))
def api_create_journal(request):
    if request.api_key != "test_key": #will be env variable in settings
        return Response({"Error": "API Key Incorrect"})
    journal = JournalSerializer(data={"name": request.data["name"],
                                      "id": request.data["id"],
                                      "phone_number": request.data["phone_number"]})
    if journal.is_valid():
        journal.save()
        return Response({"Created": True})
    else:
        return Response({"Created": False})


#url /journals/api/create_journal
@define_usage(params={"name": "String", "phone_number": "Integer", "api_key": "String"},
              returns={"journal_info": "Dict"})
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_get_journal(request):
    if request.api_key != "test_key": #will be env variable in settings
        return Response({"Error": "API Key Incorrect"})
    try:
        journal = Journal.objects.get(phone_number=request.data["phone_number"]).get(name=request.data["name"].lower())
    except:
        return Response({"Error": "Journal with phone number not found"})
    try:
        return Response({"id": journal.id}) #Return Journal ID for use in docs URL
    except:
        return Response({"Error": "Journal with name not found"})
