document.addEventListener('DOMContentLoaded', () => {
    const buyNowBtn = document.getElementById('buy-now-btn');
    const quantityInput = document.getElementById('quantity');
    const maxQuantity = parseInt(quantityInput.getAttribute('max'), 10);

    const productId = buyNowBtn.getAttribute('data-product-id');
    const checkoutUrl = buyNowBtn.getAttribute('data-checkout-url');
    const token = buyNowBtn.getAttribute('data-token');


    buyNowBtn.addEventListener('click', () => {
        const selectedQuantity = parseInt(quantityInput.value, 10);

        // Controlla se la quantità è valida
        if (isNaN(selectedQuantity) || selectedQuantity < 1 || selectedQuantity > maxQuantity) {
            alert('Errore durante l\'indirizzamento');
            return; // Block the execution of the function
        }

        // If the quantity is valid, redirect the user to the checkout page
        window.location.href = `${checkoutUrl}?product_id=${productId}&quantity=${selectedQuantity}&token=${token}`;
    });
});
