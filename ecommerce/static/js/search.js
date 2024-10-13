function setCategory(category) {
    let c = document.getElementById('categoryDropdown')
    c.innerText = category;
}

function searchWithCategory() {
    // Take the selected Category
    let selectedCategory = document.getElementById('categoryDropdown').innerText;
    let selectedFilter = document.getElementById('dropdownMenuButton').innerText;
    // Take the search input
    const searchInput = document.querySelector('input[type="search"]').value;
    // Construct the search URL
    const searchUrl = `/search?category=${selectedCategory}&query=${searchInput}&filter=${selectedFilter}`;
    // Redirect the browser to the searchUrl
    window.location.href = searchUrl;
}

function setFilter(filter) {
    let f = document.getElementById('dropdownMenuButton')
    f.innerText = filter;
}