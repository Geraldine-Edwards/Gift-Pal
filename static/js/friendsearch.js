document.addEventListener('DOMContentLoaded', function () {
    // Find the search button and input
    const searchButton = document.querySelector('button[type="submit"]'); // Target the submit button
    const searchInput = document.querySelector('input[name="search_query"]'); // Target the search input
    const searchResults = document.getElementById('search-results'); // Target the search results container

    if (searchButton && searchInput && searchResults) {
        searchButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the form from submitting

            const query = searchInput.value.trim();
            if (query.length < 2) {
                alert('Search query must be at least 2 characters long');
                return;
            }

            // Include CSRF token in the headers
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            // Make a Fetch request to the search usernames endpoint
            fetch(`/friends/search_usernames/?search_query=${query}`, {
                headers: {
                    'X-CSRFToken': csrfToken, // Include CSRF token for Django
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Clear any existing results
                    searchResults.innerHTML = '';

                    if (data.length > 0) {
                        data.forEach(function(user) {
                            const resultItem = document.createElement('div');
                            resultItem.className = 'search-result-item';

                            // Create elements for the profile image and username
                            const img = document.createElement('img');
                            img.src = user.profile_image || 'https://res.cloudinary.com/dqm93egis/image/upload/v1738488445/nobody_l7bbqh.jpg';
                            img.className = 'rounded-circle';
                            img.style.width = '50px';
                            img.style.height = '50px';
                            img.style.objectFit = 'cover';
                            img.style.marginRight = '10px';

                            const span = document.createElement('span');
                            span.textContent = user.username;

                            resultItem.appendChild(img);
                            resultItem.appendChild(span);

                            // Hidden form for sending friend request
                            const form = document.createElement('form');
                            form.method = 'POST';
                            form.action = '/friends/add-friend/';  // Your form action

                            const csrfTokenInput = document.createElement('input');
                            csrfTokenInput.type = 'hidden';
                            csrfTokenInput.name = 'csrfmiddlewaretoken';
                            csrfTokenInput.value = csrfToken;

                            const friendIdInput = document.createElement('input');
                            friendIdInput.type = 'hidden';
                            friendIdInput.name = 'friend_id';
                            friendIdInput.value = user.id;

                            const submitButton = document.createElement('button');
                            submitButton.type = 'submit';
                            submitButton.textContent = 'Add Friend';

                            form.appendChild(csrfTokenInput);
                            form.appendChild(friendIdInput);
                            form.appendChild(submitButton);

                            // Append the form to the result item and result item to the search results
                            resultItem.appendChild(form);
                            searchResults.appendChild(resultItem);
                        });
                    } else {
                        const noResults = document.createElement('div');
                        noResults.textContent = 'No registered user found with that username.';
                        searchResults.appendChild(noResults);
                    }
                })
                .catch(error => {
                    console.error('Error fetching usernames:', error);
                    alert('An error occurred while searching. Please try again.');
                });
        });
    } else {
        console.warn('Search elements not found');
    }
});