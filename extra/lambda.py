#Some values are currently changed to protect information while testing
#These values are in ALLCAPS

import json
import urllib.request


def lambda_handler(event, context):
    testdb = { #VERY TEMPORARY DICTIONARY TO EMULATE DB
        "MYPHONENUMBER": {"active": True,
                          "defaultjournal": "JOURNALID",
                          "special": "SPECIALJOURNALID"}
    }
    message = json.loads(event['Records'][0]['Sns']['Message'])
    if message['originationNumber'] in testdb: #make sure user exists (TEST)
        user = testdb[message['originationNumber']]
    else:
        return
    if not user["active"]: #if user is inactive do not proceed
        return
    words = message['messageBody'].split(" ")
    tags = []
    text = ""
    for word in words:
        if word == "":
            continue
        elif word[0] == "@": #if a words starts with @, it is an @tag
            if word[1:].lower() in user:
                tags.append(user[word[1:].lower()])
            else:
                tags.append(word[1:])
        else:
            text += word + "+"
    if text != "": #strip extra space from end
        text = text[:-1]
    #refresh_token = userbase.getToken(message['originationNumber'])
    #access_token = google.getAccessToken(refresh_token)
    #execute_app_script(access_token, tags, text)
    if tags == []:
        url = "https://script.google.com/macros/s/ACCESSURL/exec?tags=" + user["defaultjournal"] + "&message=" + text
    else:
        url = "https://script.google.com/macros/s/ACCESSURL/exec?tags="
        for tag in tags:
            url += tag + "+"
        url += "&message=" + text
    r = urllib.request.urlopen(url) #TODO: Post
    print("tags", tags, "message", text, "url", url)
