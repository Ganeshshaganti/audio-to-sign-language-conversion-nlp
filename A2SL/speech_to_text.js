window.onload = function () 
{
    const startButton = document.getElementById("start-listening");
    const outputText = document.getElementById("speech-output");
    const sceneContainer = document.getElementById("sign-language-output");

    if (!('webkitSpeechRecognition' in window)) {
        alert("Your browser does not support speech recognition. Try using Chrome.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    startButton.onclick = function () {
        recognition.start();
    };

    recognition.onresult = function (event) {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                transcript += event.results[i][0].transcript.trim().toLowerCase() + " ";
            }
        }
        outputText.innerText = transcript;
        animateSignAvatar(transcript.trim());
    };
};
