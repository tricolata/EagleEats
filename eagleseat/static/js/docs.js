// tags all header elements so that they can be
// linked to in the table of contents
window.addEventListener('load', () => {
    // for all h1, h2, h3, h4, h5, h6
    for(let i = 1; i <= 6; i++) {
        for (header of document.querySelectorAll('h' + i)) {
            // lowercases text and replaces '-' with ' '
            // e.g. Data Storange and Exchange -> data-storage-and-exchange
            //      Setup and Installation     -> setup-and-installation
            //      Environment Variables      -> environment-variables
            let formattedId = header.innerText.replace(/ /g, "-").toLowerCase();
            header.id = formattedId
        }
    }
});
