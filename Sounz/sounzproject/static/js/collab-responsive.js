let chatsection = document.getElementById('chatContainer');
let collabsection = document.getElementById('collabTool');
let chatopenButton = document.getElementById('chatOpen');
let chatcloseButton = document.getElementById('chatClose');

function chattoggle(){
    chatsection.classList.toggle('focus');
    collabsection.classList.toggle('unfocus');
    chatcloseButton.classList.toggle('on');
    chatopenButton.classList.toggle('off');
}
