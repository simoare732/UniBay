// Select all stars and rating input
const stars = document.querySelectorAll('#star-rating i');
const ratingInput = document.getElementById('rating');
// Value of the current selected rating
let currentRating = 0;

// For every star is added an event listener to handle the click event
stars.forEach(star => {
    star.addEventListener('click', function() {
        // Get the rating value of the clicked star (like 1,2,...5)
        const rating = this.getAttribute('data-value');

        // Update the hidden input value
        ratingInput.value = rating;
        // Save the current rating
        currentRating = rating; // Memorizza la valutazione corrente

        // Change the visual state of the stars
        updateStars(rating);
    });

    // Add an event listener to handle the mouseover event (to color the stars when the mouse is over them)
    star.addEventListener('mouseover', function() {
        // Get the rating value of the hovered star
        const rating = this.getAttribute('data-value');
        // Change the visual state of the stars
        updateStars(rating);
    });

    // Add an event listener to handle the mouseout event (to uncolor the stars when the mouse is out them)
    star.addEventListener('mouseout', function() {
        // Back to the current rating
        updateStars(currentRating);
    });
});

// Func to update the visual state of the stars (the index is between 0 and 4)
function updateStars(rating) {
    stars.forEach((s, index) => {
        // If the index of the star is less than the rating the star is colored
        if (index < rating) {
            s.classList.remove('far'); // Remove empty icon
            s.classList.add('fas');    // Add full icon
        // Otherwise the star is uncolored
        } else {
            s.classList.remove('fas'); // Remove full icon
            s.classList.add('far');    // Add empty icon
        }
    });
}

