document.querySelector('[type="submit"]').onclick = () => {
    wiggle();
}

// enable wiggle for 500ms
function wiggle(isEnabled) {
    for (elem of document.querySelectorAll('input:invalid')) {
        // 0.5s plus or minus [0.0, 0.2]
        let offset = Math.random() * 0.5 - 0.2;
        let duration = 0.5 + offset;

        elem.style.animation = 'wiggle ' + duration + 's';
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
