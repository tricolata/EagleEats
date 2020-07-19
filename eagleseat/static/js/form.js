document.querySelector('[type="submit"]').onclick = () => {
    wiggle();
}

// enable wiggle for 500ms
function wiggle(isEnabled) {
    for (elem of document.querySelectorAll('input:invalid')) {
        elem.style.animation = 'wiggle 0.5s';
        elem.style.backgroundColor = '#ffdbdb';
    }

    for (elem of document.querySelectorAll('input:not(:invalid)')) {
        elem.style.backgroundColor = '';
    }

    setTimeout(() => {
        for (elem of document.querySelectorAll('input:invalid')) {
            elem.style.animation = '';
        }
    }, 500);
}
