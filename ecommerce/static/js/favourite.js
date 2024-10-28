function switchImage(url) {
    document.getElementById('main-image').src = url;
}


function toggleFavorite(productId) {
    // This take the heart icon element
    const heartIcon = document.getElementById('heart-icon');

    // Send a POST request to the server. The URL is built using the productId taken as parameter
    fetch(`/watchlist/toggle_favorite/${productId}/`, {
        method: 'POST',
        // The request includes headers specifying the content type (JSON) and the CSRF token
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Aggiunge il CSRF token
        },
        // The request body is a JSON string containing the product ID
        body: JSON.stringify({ 'product_id': productId })
    })
        // The response from the server is converted to JSON
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
