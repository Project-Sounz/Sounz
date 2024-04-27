function toggleMenu() {
    const menu = document.querySelector('.nav-section-mobile');
    const blinder = document.querySelector('.blinder');
    const menuToggle = document.querySelector('.menu-toggle');
    menu.classList.toggle('active');
    blinder.classList.toggle('active');
    // Toggle animation for hamburger icon
    menuToggle.classList.toggle('close');
}
