function search() {
    var input, query, rows;
    input = document.querySelector('#searchBtn')

    // search query
    query = input.value.toLowerCase().trim()
    
    // NodeList of staff rows from table body
    rows = (document.querySelectorAll('tbody tr'))

    for(let row of rows) {
        // staff name from class name
        let name = row.className.toLowerCase()
        if(name.includes(query)) {
            row.removeAttribute('style')
        } else {
            row.setAttribute('style', 'display: none;')
        }
    }
}