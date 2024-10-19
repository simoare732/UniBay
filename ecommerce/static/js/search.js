function setFilter(filter) {
    let f = document.getElementById('dropdownMenuButton');
    f.innerText = filter;

    if (window.location.pathname.includes('list_products')) {
        // Take the option for showing the products
        let sortValue;
        switch (filter) {
            case 'Prezzo basso-alto':
                sortValue = 'price-asc';  // Usa 'price-asc' invece di 'price_asc'
                break;
            case 'Prezzo alto-basso':
                sortValue = 'price-desc';  // Usa 'price-desc' invece di 'price_desc'
                break;
            case 'Più venduti':
                sortValue = 'most-sold';   // Usa 'most-sold' invece di 'most_sold'
                break;
            default:
                sortValue = 'default';     // Valore di default
        }

        const query = new URLSearchParams(window.location.search);
        query.set('sort', sortValue);

        // Richiesta AJAX per aggiornare i risultati
        fetch(`${window.location.pathname}?` + query.toString(), {
            headers: {
                'x-requested-with': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            // Aggiorna i risultati nella pagina
            document.getElementById('results').innerHTML = html;
        })
        .catch(error => console.error('Errore durante il caricamento dei prodotti ordinati:', error));
    }
}
