$(document).ready(function () {
    //display message
eel.expose(DisplayMessage)
function DisplayMessage(message) {
    $(".siri-message li:first").text(message);
    $(".siri-message").textillate('start');
}

//display hood
eel.expose(showHood)
function showHood() {
    $("#oval").attr("hidden" , false);
    $("#siriWave").attr("hidden" , true);
}

eel.expose(senderText)

function senderText(message){
    var chat = document.getElementById("chat-canvas-body");
    if(message.trim() !== ""){
        chat.innerHTML +=`<div class = "row justify-content-end mb-4">
        <div class = "width-size">
        <div class = "sender_message">${message}</div>
        </div>`;

        chat.scrollTop = chat.scrollHeight;
    }
}

eel.expose(receiverText)
function receiverText(message){
    var chat = document.getElementById("chat-canvas-body");
    if(message.trim() !== ""){
        chat.innerHTML +=`<div class = "row justify-content-end mb-4">
        <div class = "width-size">
        <div class = "receiver_message">${message}</div>
        </div>`;

        chat.scrollTop = chat.scrollHeight;
    }

}


}); 
