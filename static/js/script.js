
document.addEventListener('DOMContentLoaded', function () {
    var navbarToggler = document.querySelector('.navbar-toggler');
    var navbarCollapse = document.querySelector('.navbar-collapse');
    var mainContent = document.querySelector('.main-content');
    var uploadProfilePic = document.querySelector('.edit-profile-picture')

    navbarToggler.addEventListener('click', function () {
        if (navbarCollapse.classList.contains('show')) {
            mainContent.style.marginTop = '60px'; // Adjust based on the height of your navbar
        } else {
            mainContent.style.marginTop = '200px'; // Adjust based on the expanded height of your navbar
        }
        document.getElementById('upload-profile-picture').click();
    });
});