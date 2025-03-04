function toggleMenu() {
    const menu = document.querySelector('.nav-section-mobile');
    const blinder = document.querySelector('.blinder');
    const menuToggle = document.querySelector('.menu-toggle');
    menu.classList.toggle('active');
    blinder.classList.toggle('active');
    // Toggle animation for hamburger icon
    menuToggle.classList.toggle('close');
}

function toggleCollabMenu(device) {
    if (device == "web"){
        const menu = document.getElementById("collabMenu");
        menu.classList.toggle("active");
    }
    else {
        const menu1 = document.querySelector('.nav-section-mobile');
        const menuToggle = document.querySelector('.menu-toggle');
        menu1.classList.toggle('active');
        menuToggle.classList.toggle('close');
        const menu2 = document.getElementById("collabMenu");
        menu2.classList.toggle("active");
    }
}