function switchImage(url) {
    document.getElementById('main-image').src = url;
}


function toggleFavorite(productId) {
    // This take the heart icon element
    const heartIcon = document.getElementById(`heart-icon`);

    // Send a POST request to the server. The URL is built using the productId taken as parameter
    fetch(`/watchlist/toggle_favorite/${productId}/`, {
        method: 'POST',
        // The request includes headers specifying the content type (JSON) and the CSRF token
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Aggiunge il CSRF token
        },
    })

    .then(response => response.json())
        // Manage the response. The heart icon is updated based on the server response
    .then(data => {
        if (data.is_favorite) {
            heartIcon.classList.remove("far");
            heartIcon.classList.add("fas"); // Full heart
        } else {
            heartIcon.classList.remove("fas");
            heartIcon.classList.add("far"); // Empty heart
        }
    })
        // In case of any error, log the error to the console
    .catch(error => console.error('Errore:', error));
}


function removeFavorite(favoriteId) {
    fetch(`/watchlist/remove_favorite/${favoriteId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // CSRF token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update the UI to remove the favorite item
            document.getElementById(`favorite-item-${favoriteId}`).remove();
        } else {
            console.error('Failed to remove favorite:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

