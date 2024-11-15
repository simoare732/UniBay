document.addEventListener('DOMContentLoaded', () => {
    const quantityInput = document.getElementById('quantity')
    const quantityMax = parseInt(document.getElementById('quantity').max, 10);
    const errorMessage = document.getElementById('quantity-error');

    quantityInput.addEventListener('input', () => {
        const inp = parseInt(quantityInput.value, 10);
        // If the input is not valid, or is less than 1 or is greater than the max quantity, the buttons are disabled
        if(isNaN(inp) || inp < 1){
            document.getElementById('cart-btn').disabled = true;
            document.getElementById('buy-now-btn').disabled = true;
        }

        else if (inp > quantityMax) {
            errorMessage.classList.remove('d-none');
            document.getElementById('cart-btn').disabled = true;
            document.getElementById('buy-now-btn').disabled = true;
        }
        else {
            errorMessage.classList.add('d-none');
            document.getElementById('cart-btn').disabled = false;
            document.getElementById('buy-now-btn').disabled = false;
        }
    });
});
