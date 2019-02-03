//for security, some information has been temporarily removed
//this information is for testing purposes only and is replaced with ALLCAPSVARIABLES

function addEntry(doc, text) {
  var body = doc.getBody();
  body.insertParagraph(0, text+"\n\n");
  var d = new Date();
  var timestamp = Utilities.formatDate(d, "GMT+1", "dd/MM/yyyy") + " " + d.toLocaleTimeString() + "\n";
  body.insertParagraph(0, timestamp);
}

function createJournal(name, text) {
  var doc = DocumentApp.create(name); //create new journal with name
  addEntry(doc, text); //write associated entry
}

function createFirst(text) {
  var doc = DocumentApp.create('Journal'); //create default journal
  addEntry(doc, text); //write associated entry
}

function process(event) {
  if (event.tags.length == 0) { // default journal
    try {
      var doc = DocumentApp.openById("GOOGLEDOCSID");
      addEntry(doc, event.message);
    } catch(e) {
      createFirst(event.message);
    }
  } else { //special journals no default
    event.tags.forEach (function (tag) {
      try {
        var doc = DocumentApp.openById(tag);
        addEntry(doc, event.message);
      } catch(e) {
        createJournal(tag, event.message);
      }
    });
  }
}

function processtest(event) {
  event.tags.forEach (function (tag) {
      try {
        var doc = DocumentApp.openById(tag);
        addEntry(doc, event.message);
      } catch(e) {
        createJournal(tag, event.message);
      }
   });
}

function doGet(e) { //TODO IMPORTANT: Replace with doPost and use encrypted post body.
  //login
  //parse
  x = e.parameters
  x.tags = [x.tags]
  processtest(x); //TODO use actual process
}

function test() {
  f1 = {"tags": [], "message": "First Message to Default Journal"}
  f2 = {"tags": [], "message": "Second Message to Default Journal"}
  f3 = {"tags": [], "message": "Third Message to Default Journal"}
  s1 = {"tags": ["Special"], "message": "First Message to Special Journal"}
  s2 = {"tags": ["Special", "Other"], "message": "Second Message to Special Journal. First Message to Other Journal."}
  s3 = {"tags": ["Other"], "message": "Second Message to Other Journal"}
  //process(f1)
  process(f2)
  //process(f3)
  //process(s1)
  //process(s2)
  //process(s3)
}
