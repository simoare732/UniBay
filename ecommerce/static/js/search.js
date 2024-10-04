function setCategory(category) {
    let c = document.getElementById('categoryDropdown')
    c.innerText = category;
}

function searchWithCategory() {
    const searchInput = document.querySelector('input[type="search"]').value;
    const searchUrl = `/search?category=${selectedCategory}&query=${searchInput}`;
    window.location.href = searchUrl;
}