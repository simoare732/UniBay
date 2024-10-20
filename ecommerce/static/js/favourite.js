function switchImage(url) {
    document.getElementById('main-image').src = url;
}

function toggleFavorite() {
    const heartIcon = document.getElementById('heart-icon');
    if (heartIcon.classList.contains("far")) {
        heartIcon.classList.remove("far");
        heartIcon.classList.add("fas"); // Filled heart
    } else {
        heartIcon.classList.remove("fas");
        heartIcon.classList.add("far"); // Outlined heart
    }
    const isFavorite = heartIcon.classList.toggle('favorite');
    localStorage.setItem('isFavorite', isFavorite);
}

document.addEventListener('DOMContentLoaded', (event) => {
    const heartIcon = document.getElementById('heart-icon');
    const isFavorite = localStorage.getItem('isFavorite') === 'true';
    if (isFavorite) {
        heartIcon.classList.add('favorite');
    }
});