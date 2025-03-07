$(document).ready(function() {
    
    // Function to get the CSRF token from the cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Like/Unlike Event
    $('.like-event').click(function() {
        const eventId = $(this).data('event-id');
        const button = $(this);
        
        $.ajax({
            url: `/friends/event/${eventId}/like/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token
            },
            success: function(response) {
                // Update button icon and like count
                if (response.liked) {
                    button.html('<i class="fas fa-heart"></i> ' + response.like_count); // Solid heart
                } else {
                    button.html('<i class="far fa-heart"></i> ' + response.like_count); // Outline heart
                }
            }
        });
    });

    // Like/Unlike Wishlist Item
    $('.like-wishlist').click(function() {
        const itemId = $(this).data('item-id');
        const button = $(this);
        const likeCountSpan = button.find('.like-count'); // Find the like count span
        
        $.ajax({
            url: `/friends/wishlist/${itemId}/like/`, // Correct URL
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token
            },
            success: function(response) {
                if (response.liked) {
                    button.html('<i class="fas fa-heart"></i> ' + response.like_count);
                } else {
                    button.html('<i class="far fa-heart"></i> ' + response.like_count);
                }
                // Update the like count
                likeCountSpan.text(response.like_count);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error); // Log the error for debugging
            }
        });
    });
});