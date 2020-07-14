function buildCustomizer(itemName, options) {
    let customizer = document.querySelector('#customizer');
    let optionPanel = document.querySelector('#option-panel');

    // close button
    let closeButton = document.createElement('button');
    closeButton.id = 'close-button';
    closeButton.innerText = '+';
    closeButton.onclick = destroyCustomizer;

    optionPanel.appendChild(closeButton);

    // header
    let header = document.createElement('h1');
    header.innerHTML = 'Customize your <span>' + itemName + '</span>';
    optionPanel.appendChild(header);

    let form = document.createElement('form');
    form.action = '/cart';
    form.method = 'post';
    form.classList.add('options');

    // option labels
    let optionLabels = document.createElement('div');
    optionLabels.classList.add('option-labels');
    
    for (mod of ['None', 'Lite', 'Reg', 'Xtra']) {
        let label = document.createElement('p');
        label.innerText = mod;
        optionLabels.appendChild(label);
    }

    optionPanel.appendChild(optionLabels);

    // options
    for (option of options) {
        form.appendChild(buildOption(option));
    }

    // submit button
    let submitButton = document.createElement('input');
    submitButton.type = 'submit';
    submitButton.id = 'add-button';
    submitButton.value = 'Add to Cart';
    form.appendChild(submitButton);

    optionPanel.appendChild(form);

    // show customizer
    customizer.style.display = 'block';
}

function buildOption(option) {
    let optionWrapper = document.createElement('div');
    optionWrapper.classList.add('option');

    let optionSelection = document.createElement('div');
    optionSelection.classList.add('option-selection');

    for (mod of ['none', 'lite', 'reg', 'xtra']) {
        let input = document.createElement('input');
        input.type = 'radio';
        input.id = option + '-' + mod;
        input.value = mod;
        input.name = option;

        // default to regular amount
        if (mod === 'reg') {
            input.checked = true;
        }

        let label = document.createElement('label');
        label.setAttribute('for', input.id);

        optionSelection.appendChild(input);
        optionSelection.appendChild(label);
    }

    let optionName = document.createElement('p');
    optionName.innerText = option;

    optionWrapper.appendChild(optionSelection);
    optionWrapper.appendChild(optionName);

    return optionWrapper;
}

function destroyCustomizer() {
    let customizer = document.querySelector('#customizer');
    let optionPanel = document.querySelector('#option-panel');

    customizer.style.display = 'none';

    // destroy innerHTML so there is no form
    // to be sent accidentally
    optionPanel.innerHTML = '';
}
