//Google Docs Init
//document.getElementById('gDoc').appendChild('p')
//="<b>1/1/2000 12:00 AM</b>";

function SMSJTitle(){
    //Uses a typewriter effect to expand the header text
    var texts = ['Send ', 'My', 'Self ', 'J'];
    //typing function
    function type(txt, i=0) {
        if (i < txt.length) { //with timeout this is a while loop
            if (i == 0) {
                document.getElementById("Title"+txt.trim()).innerHTML = "<span id='TitleFirst" + txt.trim() + "'>" + txt.charAt(i) + "</span>";
                document.getElementById("TitleFirst"+txt.trim()).classList.add("first-letter-title")
            } else {
                document.getElementById("Title"+txt.trim()).innerHTML += txt.charAt(i);
            }
            setTimeout(function(){type(txt, i+1)}, 300);
        }
    }
    //call typing function on each text span
    function typeCaller(t, i=0){
        type(t[i]);
        if (i == 1) {
            setTimeout(function(){typeCaller(t, i+1)}, 600);
        } else if (i < 4) {
            setTimeout(function(){typeCaller(t, i+1)}, 1500);
        }
    }
    //wait a couple seconds on load.
    setTimeout(function(){typeCaller(texts);}, 2000);
}

window.onload = SMSJTitle();

function setYear() {
    document.getElementById("year").innerHTML = (new Date()).getFullYear();
}

window.onload = setYear();

function beginSignup() {
    document.getElementById("signupArea").innerHTML = '<h4 class="card-header">Phone Number</h4><div class="card-body"><p>To get started, please enter and confirm your phone number.</p><div id="noMatch" hidden class="alert alert-danger" role="alert">Error: phone numbers don\'t match.</div><div id="noFormat" hidden class="alert alert-danger" role="alert">Error: phone numbers not recognized.</div><form><input class="form-control" type="tel" required id="phoneNumber"><br><input class="form-control" type="tel" required id="phoneNumberConfirm"></form></div><div class="card-footer"><a onclick="getGoogle()" class="btn btn-primary cardButton">Next</a></div>'
    document.getElementById("phoneNumber").placeholder = "Phone Number";
    document.getElementById("phoneNumberConfirm").placeholder = "Confirm Phone Number";
}

function verifyNumber() {
    phoneNumber = document.getElementById("phoneNumber").value.match(/\d+/g).join(""); //get all numbers regardless of formatting
    phoneNumberConfirm = document.getElementById("phoneNumberConfirm").value.match(/\d+/g).join("");
    if ((phoneNumber == phoneNumberConfirm) && (phoneNumber.length == 10)) {
        return true;
    }
    else if (phoneNumber.length == 10) {
        document.getElementById("noMatch").hidden = false;
        return false;
    }
    else {
        document.getElementById("noFormat").hidden = false;
        return false;
    }
}

function getGoogle() {
    correct = verifyNumber();
    if (correct) {
        document.getElementById("signupArea").innerHTML = '<h4 class="card-header">Google Account</h4><div class="card-body"><p>Grant access to your Google account to create journals.</p></div><div class="card-footer"><a onclick="getPayment()" id="googleSignin" class="btn btn-primary cardButton">Grant Access</a></div>'
        document.getElementById("googleAccount").placeholder = "Google Account";
    }
}

function getPayment() {
    Auth.signIn(); //wait, verify
    document.getElementById("signupArea").innerHTML = '<h4 class="card-header">Payment</h4><div class="card-body"><p>SMSJournal costs $1.49 per month, billed annually as $17.88. Your payment is processed securely by Stripe. To complete setup, please enter your credit card information.</p></div><div class="card-footer"><a onclick="PayWithStripe()" id="StripePurchase" class="btn btn-primary cardButton">Pay with Stripe</a></div>'
}

function getStripe() {
    //get Payment
    document.getElementById("signupArea").innerHTML = '<h4 class="card-header">Signup Complete</h4><div class="card-body"><p>Thank you for signing up for SMSJournal! To get started, check your phone for a welcome text message.</p></div><div class="card-footer"></div>'
}

//window.onload = alert("SMSJournal is a work in progress. To be notified of its completion, email info@grammiegram.com");
//<a onclick="getStripe()" id="stripeSignin" class="btn btn-primary cardButton">Pay Now</a>

function addToGDoc(s) { //TODO: Fix bug with send after edit
    timestamp = Date().toString().split(":").splice(0, 2).join(":");
    document.getElementById("gDoc").innerHTML = timestamp + "\n" + s + "\n\n" + document.getElementById("gDoc").innerHTML
}

document.getElementById("sendMessage").addEventListener('keypress', function(e){
    if (e.keyCode == 13) {
        field = document.getElementById("sendMessage");
        str = field.value;
        //delete the field
        field.value = "";
        //appendChild new message
        newMessage = document.createElement("div");
        newMessage.className = "message me"
        newMessage.innerHTML = str;
        document.getElementById("SMSMessages").appendChild(newMessage);
        //add to google docs with timestamp
        addToGDoc(str);
    }
});

window.onload = addToGDoc("Send a message to see it appear in Google Docs.")
