// tags all header elements so that they can be
// linked to in the table of contents
window.addEventListener('load', () => {

    // for all h1, h2, h3, h4, h5, h6
    for(let i = 1; i <= 6; i++) {
        for (header of document.querySelectorAll('h' + i)) {
            let formattedId = header.innerText.replace(/ /g, "-").toLowerCase();
            header.id = formattedId
        }
    }
});
