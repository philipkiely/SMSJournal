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
