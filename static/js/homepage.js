function pagestartup() {
    responsiveVoice.speak("Welcome to Email On Voice");
    setTimeout(1000);
    responsiveVoice.speak("Please speak your email address");
    setTimeout(readEmail, 6000);
}

function loginUser() {
    // Login the user with the spoken credentials
    document.getElementById("signin").click();
}

function readEmail() {
    speechToText("email");
    setTimeout(readPassword, 10000);
}

function readPassword() {
    responsiveVoice.speak("Please speak your password");
    speechToText("password");
    
    setTimeout(loginUser, 10000);
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