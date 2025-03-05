document.addEventListener('DOMContentLoaded', function() {
    // Find the edit avatar button
    const editAvatarButton = document.querySelector('.btn-edit-avatar');
    // Find the file input inside the modal
    const uploadProfilePictureInput = document.querySelector('#uploadProfilePictureModal input[type="file"]');

    if (editAvatarButton && uploadProfilePictureInput) {
        // Add click event listener to the edit avatar button
        editAvatarButton.addEventListener('click', function() {
            uploadProfilePictureInput.click(); // Trigger file input click
        });
    } else {
        console.warn('Elements not found');
    }
});