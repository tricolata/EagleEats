// apply 'active' class as appropriate
function setStage(status) {
    let stage;

    switch (status) {
        case 'received': stage = 1; break;
        case 'cooking': stage = 2; break;
        case 'ready': stage = 3; break;
        case 'complete': stage = 4; break;
    }

    for (let i = 1; i <= stage; i++) {
        document.querySelector('.stage.stage' + i).classList.add('active');

        if (i !== 1) {
            document.querySelector('.joiner.stage' + i).classList.add('active');
        }
    }
}
