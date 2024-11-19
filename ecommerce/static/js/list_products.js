// This script is used to filter the products by title
document.getElementById('searchInput').addEventListener('keyup', function() {
    // Get the search value and convert it to lowercase for case-insensitive comparison
    var searchValue = this.value.toLowerCase();
    // Get all the elements with the class 'product-card'
    var productCards = document.querySelectorAll('.product-card');
    // For every product do the following
    productCards.forEach(function(card) {
        // Get the title of the product and convert it to lowercase for case-insensitive comparison
        var title = card.querySelector('.card-title').innerText.toLowerCase();
        // If the title includes the search value, display the card, otherwise hide it
        if (title.includes(searchValue)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
});