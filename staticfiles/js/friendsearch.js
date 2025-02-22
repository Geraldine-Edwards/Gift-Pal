document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search_query');
    const searchResults = document.getElementById('search-results');

    searchButton.addEventListener('click', function () {
        const query = searchInput.value.trim();
        if (query.length < 2) return;  // Ignore short inputs
    
        // Make a Fetch request to the search usernames endpoint
        fetch('/friends/search_usernames/?search_query=' + query)
            .then(response => response.json())
            .then(data => {
                // Get the search results div in the template
                searchResults.innerHTML = ''; // Clear any existing results

                if (data.length > 0) {
                    data.forEach(function(user) {
                        var resultItem = document.createElement('div');
                        resultItem.className = 'search-result-item';

                        // Create elements for the profile image and username
                        var img = document.createElement('img');
                        img.src = user.profile_image || 'https://res.cloudinary.com/dqm93egis/image/upload/v1738488445/nobody_l7bbqh.jpg';
                        img.className = 'rounded-circle';
                        img.style.width = '50px';
                        img.style.height = '50px';
                        img.style.objectFit = 'cover';
                        img.style.marginRight = '10px';

                        var span = document.createElement('span');
                        span.textContent = user.username;

                        resultItem.appendChild(img);
                        resultItem.appendChild(span);

                        // Hidden form for sending friend request
                        var form = document.createElement('form');
                        form.method = 'POST';
                        form.action = '/friends/add-friend/';  // Your form action

                        var csrfTokenInput = document.createElement('input');
                        csrfTokenInput.type = 'hidden';
                        csrfTokenInput.name = 'csrfmiddlewaretoken';
                        csrfTokenInput.value = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

                        var friendIdInput = document.createElement('input');
                        friendIdInput.type = 'hidden';
                        friendIdInput.name = 'friend_id';
                        friendIdInput.value = user.id;

                        var submitButton = document.createElement('button');
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
                    var noResults = document.createElement('div');
                    noResults.textContent = 'No registered user found with that username.';
                    searchResults.appendChild(noResults);
                }
            })
            .catch(error => console.error('Error fetching usernames:', error));
    });
});