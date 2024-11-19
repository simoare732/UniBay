// Show the answer form in 'question_list' page
function toggleAnswerForm(questionPk) {
    const form = document.getElementById(`answer-form-${questionPk}`);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}

// Filter the questions based on the checkboxes
function filterQuestions() {
    const showApproved = document.getElementById('filter-approved').checked;
    const showUnanswered = document.getElementById('filter-unanswered').checked;

    // Find all question cards
    const questionCards = document.querySelectorAll('.question-card');

    questionCards.forEach(card => {
        const hasApprovedAnswer = card.getAttribute('data-has-approved-answer') === 'True';

        // Show/hide based on checkbox states
        if (
            (showApproved && hasApprovedAnswer) ||
            (showUnanswered && !hasApprovedAnswer)
        ) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {
    // Attiva entrambi i checkbox
    document.getElementById('filter-approved').checked = true;
    document.getElementById('filter-unanswered').checked = true;

    // Esegui il filtro per mostrare tutte le domande
    filterQuestions();
});