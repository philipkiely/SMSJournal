// Keep everything in a namespace so that there're no conflicts
var Auth = (function() {
    var GoogleAuth;
    var isAuthorized = false;

    // Load Google API auth2 modules
    function loadClient() {
        console.log("LoadClient called")
        gapi.load("auth2", initClient);
    }

    // Set GoogleAuth
    function setAuth() {
        console.log("setAuth called")
        GoogleAuth = gapi.auth2.getAuthInstance();
        GoogleAuth.isSignedIn.listen(updateStatus);
        var status = GoogleAuth.isSignedIn.get();
        updateStatus(status);
    }

    // Initialize Google API Client
    function initClient() {
        console.log("InitClient called")
        gapi.auth2.init({
            // This clientId is ONLY to be used in development, not production
            // To use it, set really-this-is-localhost.com to point to 127.0.0.1 in your hosts file
            // Run a local webserver (I use the python http.server) and go to really-this-is-localhost.com to test it
            // Use client id under "SMSJournal Client" in credentials page for prod
            "clientId": "752165490166-j74ipne57mdk7la4vuv97d2i434ibjar.apps.googleusercontent.com",
            "scope": "profile https://www.googleapis.com/auth/documents",
            "discoveryDocs": "https://www.googleapis.com/discovery/v1/apis?name=scripts"
        }).then(setAuth);
    }

    // Update Sign In Status
    function updateStatus(signedIn) {
        console.log("updateStatus called")
        var btn = document.getElementById("googleSignin");
        var txt = document.getElementById("text");
        var info = document.getElementById("info");
        if (signedIn) {
            isAuthorized = true;
            //btn.onclick = revoke;
            //btn.innerHTML = "Revoke access!";
            //txt.innerHTML = "Authorized!";
            var user = GoogleAuth.currentUser.get();
            var profile = user.getBasicProfile();
            var name = profile.getName();
            var email = profile.getEmail();
            //info.innerHTML = "Name: " + name + "<br>Email: " + email;
        } else {
            isAuthorized = false;
            btn.onclick = signIn;
            btn.innerHTML = "Grant access!";
            txt.innerHTML = "Unauthorized!";
            info.innerHTML = " ";
        }
    }

    // Revoke access to google account
    function revoke() {
        console.log("revoke called")
        GoogleAuth.disconnect();
    }

    // Grant access to google account
    function signIn() {
        console.log("signin called")
        GoogleAuth.signIn();
    }

    return {loadClient, signIn, isAuthorized, GoogleAuth};
})();
window.onload = Auth.loadClient();
window.onload = console.log("auth loaded")
