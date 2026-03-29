document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.querySelector('nav');
    window.onscroll = function() {
        if (window.pageYOffset > 50) {
            navbar.style.background = "#fff"; // Change to a solid background
        } else {
            navbar.style.background = "transparent"; // Keep it transparent
        }
    };
});
