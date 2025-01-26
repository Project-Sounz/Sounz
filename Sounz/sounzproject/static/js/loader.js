window.onload = () => {
    const preloader = document.getElementById('loader');
    const content = document.getElementById('export-htmls');
    preloader.style.display = 'none'; // Hide preloader
    content.style.display = 'block'; // Show content
};

// document.addEventListener("DOMContentLoaded", () => {
//     const profilepic_def = document.getElementById('navbar-user-profile-pic-loader')
//     const profilepic = document.getElementById('navbar-user-profile-pic')
//     const profilepic_a = document.getElementById('navbar-user-profile-pic-a')
//     profilepic.onload = () => {
    
//         profilepic_def.style.display = 'none';
//         profilepic.style.display = 'block';
//         profilepic_a.style.display = 'block';
//     }
// });
