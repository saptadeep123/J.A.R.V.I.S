$(document).ready(function () {
    $('.text').textillate({
        loop:true,
        sync:true,
        in:{
            effect:'bounceIn',
        },
        out:{
            effect:'bounceOut',
        }
    });

    //siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 640,
        height: 200,
        style:"ios9",
        amplitude:"0.5",
        speed:"0.15",
        autostart:true,
        lerpSpeed:0.02,
        ranges:null,
        pixelDepth:0.02,
      });
      //siri message animation
      $('.siri-message').textillate({
        loop:true,
        sync:true,
        in:{
            effect:'fadeInUp',
            sync : true,
        },
        out:{
            effect:'fadeOutUp',
            sync : true,
        }
    });

    //mic button click event
    $("#micbutton").click(function () {
       eel.playassistentsound()
       $("#oval").attr("hidden" , true);
       $("#siriWave").attr("hidden" , false);
       eel.takeallCommands()()
        
    });

    function handleKeyUp(e) {
        // Check for Windows key (Meta) + J
        if (e.key.toLowerCase() === 'j' && e.metaKey) {
            e.preventDefault();
            console.log("Windows+J pressed - activating voice assistant");
            
            // Your voice assistant functions
            eel.playassistentsound();
            $("#oval").attr("hidden", true);
            $("#siriWave").attr("hidden", false);
            eel.takeallCommands()();
        }
    }
    
    // Add event listener properly
    document.addEventListener('keyup', handleKeyUp);
    
    function playassistent (message){
        if(message != ""){
            $("#oval").attr("hidden" ,true);
            $("#siriWave").attr("hidden", false);
            eel.takeallCommands(message);
            $("#chatbox").val("");
            $("#micbutton").attr("hidden" ,  false);
            $("#sendbtn").attr("hidden",true);

        }
    }

    function showhidebutton(message){
        if(message == 0){
            $("#micbutton").attr("hidden" ,  false);
            $("#sendbtn").attr("hidden" , true);
        }else{
            $("#micbutton").attr("hidden" , true);
            $("#sendbtn").attr("hidden" , false);
        }
    }

    $("#chatbox").keyup(function(){
         let message = $("#chatbox").val();
         showhidebutton(message);
    });

    $("#sendbtn").click(function(){
        let message = $("#chatbox").val();
        playassistent(message);
    })

    eel.expose(promptForMessage);
function promptForMessage() {
    const message = prompt("What message would you like to send?");
    if (message) {
        eel.send_message_content(message);
    }
}


 });


