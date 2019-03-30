import sys
import urllib.request
import random
import os


def call(base_url, tags, text, number, api_key):
    response = urllib.request.Request(base_url + "/journals/api/entry/",
                                      data={"names": ",".join(tags),
                                            "message": text,
                                            "phone": number,
                                            "api_key": api_key},
                                      method="POST")
    print(response)


#A test suite to simulate the API calls from AWS Lambda after a SMS is received
if __name__ == "__main__":
    if sys.argv[1] == "dev":
        base_url = "http://127.0.0.1:8000"
        api_key = os.environ["API_KEY"]
        number = "+11234567890"
    elif sys.argv[1] == "prod":
        base_url = "https://smsjournal.xyz"
        api_key = "undetermined"
        number = "undetermined"
        print("prod not ready yet")
        exit()
    else:
        print("must specify dev or prod")
        exit()
    call(base_url, "", "Test Message Default Only", number, api_key)
    #call(base_url, "special", "Test Message Special Only", number, api_key)
    #call(base_url, "special,other", "Test Message Special and Other", number, api_key)
    #call(base_url, "new_" + str(random.randint(0, 10000000000000)), "Test Message New", number, api_key)
