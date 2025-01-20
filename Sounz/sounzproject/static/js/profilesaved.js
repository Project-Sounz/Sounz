var postButton = document.getElementById('postbutton');
var savedButton = document.getElementById('savedbutton');

const postSection = document.getElementById('profile-content-controller-posts');
const savedSection = document.getElementById('profile-content-controller-saved');
document.addEventListener('DOMContentLoaded', function() {
    savedButton.classList.add('active');
    savedSection.style.display = 'block';
    postSection.style.display = 'none';
});
function loadPosts(){
    postButton.classList.add('active');
    savedButton.classList.remove('active');
    postSection.style.display = 'block';
    savedSection.style.display = 'none';
}
function loadSaved(){
    postButton.classList.remove('active');
    savedButton.classList.add('active');
    postSection.style.display = 'none';
    savedSection.style.display = 'block';
}