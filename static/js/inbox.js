const wait = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

async function voices() {
    responsiveVoice.speak("Your recent mails are:");
    await wait(3000);
    var from;
    var sub;
    
    for (i = 1; i < 7; i++) { 
      from = document.getElementById(i).innerHTML;
      console.log(from);
      responsiveVoice.speak(from);
      await wait(6000);
      i=i+1;
      //await wait(6000);
      responsiveVoice.speak("Subject:");
      await wait(2000);
      sub = document.getElementById(i).innerHTML;
      console.log(sub);
      responsiveVoice.speak(sub);
      await wait(6000);
      i=i+1;
      //await wait(3000);
    }
}    
