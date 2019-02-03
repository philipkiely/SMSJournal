function triggerGoogleScript () {
    Auth.GoogleAuth.script.scripts.run({
        "scriptId": "", // Here, the ID of the API executable script belongs
        "resource": {
            "function": "createFirst",
            "parameters": [text],
            "devMode": false // If set to true, this lets us run the most recent edit, but only if sent from script owner's account
        }
    });
}
