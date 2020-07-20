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

    // create dummy form element for itemName
    const nameInput = document.createElement('input');
    nameInput.type = 'hidden';
    nameInput.name = 'name';
    nameInput.value = itemName;

    // append dummy input
    form.appendChild(nameInput);

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

// set default category to entree
changeCategory('entree');
function changeCategory(category) {
    // all menu items that are NOT in category
    let otherItems = document.querySelectorAll('.menu-item:not(.' + category + ')');

    // all meny items that are in category
    let categoryItems = document.querySelectorAll('.menu-item.' + category);

    // hide all items in otherItems
    for (item of otherItems) {
        item.style.display = 'none'
    }

    // show all items in categoryItems
    for (item of categoryItems) {
        // clear display, let css define
        item.style.display = ''
    }

    // css selector of the button for the new category
    let selector = '#' + category + '-button';

    console.log(selector);

    // the active category
    let activeCategoryButton = document.querySelector(selector);

    // the other categories' buttons
    let otherCategoryButtons = document.querySelectorAll('.menu-navbar button:not(' + selector + ')');

    // set active button
    activeCategoryButton.classList.add('active');

    // unset all other buttons
    for (button of otherCategoryButtons) {
        button.classList.remove('active');
    }
}
