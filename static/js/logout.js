const wait = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };
  
  async function page() {
      responsiveVoice.speak("You have logged out successfully");
      await wait(4000);
      responsiveVoice.speak("If you want to sign in again, Please speak your email address");
      await wait(6000);
      speechToText("email");
      await wait(10000);
      responsiveVoice.speak("Please speak your password");
      await wait(4000);
      speechToText("password");
      await wait(10000);
      loginUser();
  
  }

  function loginUser() {
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