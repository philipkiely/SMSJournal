function addEntry(doc, text) {
  var body = doc.getBody();
  body.insertParagraph(0, text+"\n\n");
  var d = new Date();
  var timestamp = Utilities.formatDate(d, "GMT+1", "dd/MM/yyyy") + " " + d.toLocaleTimeString() + "\n"; //TODO: Localize
  var recorded = "Recorded at " + timestamp.slice(11, 15) + timestamp.slice(18, 21) + " on " + timestamp.slice(0, 10) + "\n";
  body.insertParagraph(0, recorded);
}

function createJournal(name, text, phone) {
  var doc = DocumentApp.create(name); //create new journal with name
  addEntry(doc, text); //write associated entry
  var data = {
    'name': name,
    'id': doc.getId(),
    'phone_number': phone,
    'api_key': "test_key"
  };
  var options = {
    'method' : 'post',
    'payload' : data
  };
  UrlFetchApp.fetch('https://smsjournal.xyz/journals/api/create_journal/', options);
}

function process(tags, message, phone) {
  tags.forEach (function (tag) {
      try {
        var doc = DocumentApp.openById(tag); //will fail if tag is not a document ID, expected behavior
        addEntry(doc, message);
      } catch(e) {
        createJournal(tag, message, phone); //in the event of a failure, create a new journal
      }
   });
}

function doPost(e) {
  //login
  tags = String(e["parameters"]["ids"]).split(","); //parse journals
  message = e["parameters"]["message"];
  phone = e["parameters"]["phone"];
  process(tags, message, phone);
}
