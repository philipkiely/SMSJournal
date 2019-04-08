import json
import urllib.request
import os

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    words = message['messageBody'].split(" ")
    tags = []
    text = ""
    for word in words:
        if word == "":
            continue
        elif word[0] == "@": #if a words starts with @, it is an @tag
            tags.append(word[1:])
        else:
            text += word + "+"
    if text != "": #strip extra space from end
        text = text[:-1]
    response = urllib.request.Request("https://smsjournal.xyz/journals/api/entry/",
                                              data={"names": ",".join(tags),
                                                    "message": text,
                                                    "phone": message['originationNumber'],
                                                    "api_key": os.environ["api_key"]},
                                              method="POST")
