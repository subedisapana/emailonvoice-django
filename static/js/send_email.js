const wait = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

async function pageStartUp() {
    responsiveVoice.speak("Compose your email");
    await wait(3000);
    responsiveVoice.speak("Whom do you want to send your email?");
    await wait(4000);
    speechToText("to_email");
    await wait(10000);
    responsiveVoice.speak("Please speak your subject");
    await wait(4000);
    speechToText("subject");
    await wait(10000);
    responsiveVoice.speak("What is your message?");
    await wait(4000);
    speechToText("message");
    await wait(10000);
    Sendemail();
}

function Sendemail() {
    // Login the user with the spoken credentials
    document.getElementById("signin").click();
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