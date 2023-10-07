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
        if(name.startsWith(query)) {
            row.removeAttribute('style')
        } else {
            row.setAttribute('style', 'display: none;')
        }
    }
}

// close flash message
function dismissFlash() {
    var flash = document.getElementsByClassName('pop-flash')[0]
    console.log(flash);
    flash.style.opacity = 0 // start fading out
    setTimeout(function(){
        flash.style.display = 'none'
    }, 600) // duration in milliseconds of fade out
}

setTimeout(dismissFlash, 5000)