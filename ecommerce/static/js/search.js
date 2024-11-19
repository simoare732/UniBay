function setFilter(filter) {
    let f = document.getElementById('dropdownMenuButton');
    f.innerText = filter;

    if (window.location.pathname.includes('list_products')) {
        // Take the option for showing the products
        let sortValue;
        switch (filter) {
            case 'Prezzo basso-alto':
                sortValue = 'price-asc';
                break;
            case 'Prezzo alto-basso':
                sortValue = 'price-desc';
                break;
            case 'Più venduti':
                sortValue = 'most-sold';
                break;
            default:
                sortValue = 'default';
        }

        const query = new URLSearchParams(window.location.search);
        query.set('sort', sortValue);

        // Ajax request to update the products
        fetch(`${window.location.pathname}?` + query.toString(), {
            headers: {
                'x-requested-with': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            // Update results in the page
            document.getElementById('results').innerHTML = html;
        })
        .catch(error => console.error('Errore durante il caricamento dei prodotti ordinati:', error));
    }
}
