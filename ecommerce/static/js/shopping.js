function updateQuantity(itemPk, action){
    fetch(`/shopping/update_item_quantity/${itemPk}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'action': action })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            if(data.quantity === 0){
                document.getElementById('cart-item-${itemPk}').remove();
            }
            else{
                document.getElementById(`quantity-${itemPk}`).innerText = data.quantity;
            }
            // Aggiorna la quantità e il prezzo totale nel template
            document.getElementById(`small-quantity`).innerText = data.total_items;
            document.getElementById('total-items').innerText = data.total_items;
            document.getElementById('total-price').innerText = `${parseFloat(data.total_price).toFixed(2).replace('.',',')}`;
            document.getElementById('total-price-summary').innerText = `${parseFloat(data.total_price).toFixed(2).replace('.',',')}`;
        }
    })
    .catch(error => console.error('Error:', error));
}