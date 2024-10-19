const stars = document.querySelectorAll('#star-rating i');
const ratingInput = document.getElementById('rating');
let currentRating = 0; // Valore corrente della valutazione selezionata

// Aggiungi evento click su ogni stella
stars.forEach(star => {
    star.addEventListener('click', function() {
        const rating = this.getAttribute('data-value');

        // Aggiorna il campo nascosto con la valutazione selezionata
        ratingInput.value = rating;
        currentRating = rating; // Memorizza la valutazione corrente

        // Cambia visivamente le stelle (piene fino a quella selezionata)
        updateStars(rating);
    });

    // Aggiungi effetto hover per mostrare temporaneamente la valutazione
    star.addEventListener('mouseover', function() {
        const rating = this.getAttribute('data-value');
        updateStars(rating);  // Riempie le stelle in base a dove è il mouse
    });

    // Quando il mouse esce dall'area delle stelle, ripristina la valutazione selezionata
    star.addEventListener('mouseout', function() {
        updateStars(currentRating); // Torna alla valutazione corrente
    });
});

// Funzione per aggiornare lo stato visivo delle stelle
function updateStars(rating) {
    stars.forEach((s, index) => {
        if (index < rating) {
            s.classList.remove('far'); // Rimuove l'icona vuota
            s.classList.add('fas');    // Aggiunge l'icona piena
        } else {
            s.classList.remove('fas'); // Rimuove l'icona piena
            s.classList.add('far');    // Aggiunge l'icona vuota
        }
    });
}