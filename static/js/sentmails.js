const wait = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

async function voice() {
    responsiveVoice.speak("Your recent mails are:");
    await wait(3000);
    var num = document.getElementById("1").value
    console.log ("this" + num);
    responsiveVoice.speak(num);
    await wait(3000);
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