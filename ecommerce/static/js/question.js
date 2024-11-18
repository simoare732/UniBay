function showSection(section) {
    // Remove "active" state from all buttons
    document.getElementById("btn-reviews").classList.remove("active");
    document.getElementById("btn-questions").classList.remove("active");

    // Remove "active" state from all sections
    document.getElementById("reviews-section").classList.remove("active");
    document.getElementById("questions-section").classList.remove("active");

    document.getElementById('reviews-buttons').classList.remove("active");
    document.getElementById('questions-buttons').classList.remove("active");

    document.getElementById(section + "-buttons").classList.add("active");

    // Add "active" state to all sections
    document.getElementById(section + "-section").classList.add("active");

    // Add "active" state to the button
    document.getElementById("btn-" + section).classList.add("active");
}

// Set the default section to show when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
    showSection('reviews');
});


function toggleReplyForm(questionId) {
    document.getElementById(`reply-section-${questionId}`).classList.add('d-none');
    document.getElementById(`reply-form-${questionId}`).classList.remove('d-none');
}

// Nasconde il modulo di risposta e mostra il bottone Rispondi
function cancelReply(questionId) {
    document.getElementById(`reply-form-${questionId}`).classList.add('d-none');
    document.getElementById(`reply-section-${questionId}`).classList.remove('d-none');
}


// Show the answer form in 'question_list' page
function toggleAnswerForm(questionPk) {
    const form = document.getElementById(`answer-form-${questionPk}`);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}