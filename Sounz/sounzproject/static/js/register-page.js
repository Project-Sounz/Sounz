
var registerButton = document.getElementById('register-button');
var termsCheckbox = document.getElementById('agree');

termsCheckbox.addEventListener('change', function() {
    registerButton.disabled = !termsCheckbox.checked;
});
function ua(){
    var uaContent = document.getElementById("user-agreement");
    var rightContent = document.getElementById("main-right-section");
    if(uaContent.style.display === "none"){
        uaContent.style.display = "block";
        rightContent.style.display = "none";
    }
    else{
        uaContent.style.display = "none";
        rightContent.style.display = "block";
    }    
};
const passwordInput = document.getElementById("password");

function validatePassword() {
    const password = passwordInput.value;
    const passwordError = document.getElementById("password-error");

    const passwordPattern =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!passwordPattern.test(password)) {
        passwordError.innerHTML =
            "Password must be at least 8 characters long and include:<br>- 1 uppercase letter<br>- 1 lowercase letter<br>- 1 number<br>- 1 special character (@, #, $, etc.)";
    } else {
        passwordError.innerHTML = "";
    }
}

passwordInput.addEventListener("input", validatePassword);

document.getElementById('profile_picture_input').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('profile_picture_preview');
                const uploadImg = document.getElementById('upload-dp-img');
                preview.src = e.target.result;
                preview.style.display = 'block';
                uploadImg.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });

function togglePassword(fieldId, toggleElement) {
            var passwordField = document.getElementById(fieldId);
            if (passwordField.type === "password") {
                passwordField.type = "text";
                toggleElement.textContent = ":: hide";
            } else {
                passwordField.type = "password";
                toggleElement.textContent = ":: show";
            }
        }
function validateForm() {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;
            var isValid = true;

            if (username === "") {
                document.getElementById('username-error').innerText = "* username is required";
                isValid = false;
            } else {
                document.getElementById('username-error').innerText = "";
            }

            if (password === "") {
                document.getElementById('password-error').innerText = "* password is required";
                isValid = false;
            } else {
                document.getElementById('password-error').innerText = "";
            }

            return isValid;
        }