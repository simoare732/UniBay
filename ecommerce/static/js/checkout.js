document.getElementById("submit-button").addEventListener("click", function(event) {
    // Verify the form before submitting it
    let form = document.getElementById("checkout-form");
    if (form.checkValidity()) {
        form.submit();
    } else {
        form.reportValidity();
    }
});