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

/* slideIndex holds ....? */
let slideIndex = [1, 1];
/* Class the members of each slideshow group with different CSS classes */
let slideId = ["mySlides1", "mySlides2"]

/* Display first slide images at start */
showSlides(1, 0);
showSlides(1, 1);

function plusSlides(n, no) {
    showSlides(slideIndex[no] += n, no);
    // reset image carousel 
    // if (no == 0) {
    //     let x = document.getElementsByClassName(slideId[0]);
    //     for (i = 0; i < x.length; i++) {
    //         x[i].style.display = "none";
    //     }
    //     x[slideIndex[1]-1].style.display = "block";
    // }
}

function showSlides(n, no) {
    let i;
    let x = document.getElementsByClassName(slideId[no]);
    if (n > x.length) {slideIndex[no] = 1}
    if (n < 1) {slideIndex[no] = x.length}
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex[no]-1].style.display = "block";
}
