function showSection(section) {
    // Rimuove lo stato "active" da tutti i bottoni
    document.getElementById("btn-reviews").classList.remove("active");
    document.getElementById("btn-questions").classList.remove("active");

    // Rimuove lo stato "active" da tutte le sezioni
    document.getElementById("reviews-section").classList.remove("active");
    document.getElementById("questions-section").classList.remove("active");

    // Aggiunge "active" alla sezione cliccata
    document.getElementById(section + "-section").classList.add("active");

    // Evidenzia il bottone corrispondente
    document.getElementById("btn-" + section).classList.add("active");
}

// Imposta la sezione iniziale attiva (opzionale)
document.addEventListener("DOMContentLoaded", function() {
    showSection('reviews'); // Avvia con le recensioni
});