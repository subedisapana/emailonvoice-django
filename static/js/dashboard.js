const wait = (ms) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
};

async function pagestart()
{
  responsiveVoice.speak("Login successful");
  await wait(3000);
  responsiveVoice.speak("Select a number, 1 to Compose, 2 to check inbox,  3 to check sent mails and 4 to logout");
  await wait(10000);
  speechToText("number");
  await wait(4000);
  if (number = "1"){
    Composemail();
  } else if (number = "2"){
    Checkinbox();
  }
  else if (number = "3"){
    Checksentmails();
  }
  else if (number = "4"){
    Loggingout();
  } 
   
}    
   
function Composemail() {
    document.getElementById("compose").click();
}

function Checkinbox() {
  document.getElementById("checkinbox").click();
}

function Checksentmails() {
  document.getElementById("checksentmails").click();
}

function Loggingout() {
  document.getElementById("logout").click();
}

function speechToText(attribute) {
  // Converts speech to text when invoked...
  console.log("Starting dictation....");

  if (window.hasOwnProperty('webkitSpeechRecognition')) {

      var recognition = new webkitSpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.lang = "en-US";
      recognition.start();

      recognition.onresult = function (e) {
          console.log("It gave something ==> ", e.results[0][0].transcript);
          document.getElementById(attribute).value = e.results[0][0].transcript.replace(/\s/g,'');
      };

      recognition.onerror = function (e) {
          console.log("It gave error", e);
          recognition.stop();
      }

  }
}

