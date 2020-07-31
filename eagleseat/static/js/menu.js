function buildCustomizer(itemName, itemId, options, hasSize) {
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

    // create dummy form element for itemId
    const idInput = document.createElement('input');
    idInput.type = 'hidden';
    idInput.name = 'id';
    idInput.value = itemId;

    // append dummy input
    form.appendChild(idInput);

    form.classList.add('options');

    // size
    if (hasSize) {
        let sizeLabels = document.createElement('div');
        sizeLabels.classList.add('option-labels');

        for (size of ['small', 'medium', 'large', 'giant']) {
            let label = document.createElement('p');
            label.innerText = size
            sizeLabels.appendChild(label);
        }

        form.appendChild(sizeLabels);

        // size option radio buttons
        form.appendChild(buildOption('size'));
    }

    // options
    if (options !== 'None') {
        // option labels
        let optionLabels = document.createElement('div');
        optionLabels.classList.add('option-labels');

        for (mod of ['none', 'lite', 'regular', 'extra']) {
            let label = document.createElement('p');
            label.innerText = mod;
            optionLabels.appendChild(label);
        }

        form.appendChild(optionLabels);

        let optionsJSON = JSON.parse(options);
        for (option of optionsJSON.options) {
            form.appendChild(buildOption(option));
        }
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

    // remove focus from customize button
    setTimeout(() => {
        document.querySelector('form input[type="submit"]').focus()
        document.querySelector('form input[type="submit"]').blur()
    }, 0);
}

function buildOption(option) {
    let optionWrapper = document.createElement('div');
    optionWrapper.classList.add('option');

    let optionSelection = document.createElement('div');
    optionSelection.classList.add('option-selection');

    if (option === "size") {
        optionNames = ['small', 'medium', 'large', 'giant'];
    } else {
        optionNames = ['none', 'lite', 'regular', 'extra'];
    }

    for (mod of optionNames) {
        let input = document.createElement('input');
        input.type = 'radio';
        input.id = option + '-' + mod;
        input.value = mod;
        input.name = option;

        // default to regular amount
        if (mod === 'regular' || mod === 'medium') {
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

// remove any category with no items in it
removeEmptyCategories(['entree', 'side', 'dessert', 'drink']);
function removeEmptyCategories(affectedCategories) {
    let numItems = 0;

    for (category of affectedCategories) {
        numItems = document.querySelectorAll('.menu-item.' + category).length
        if (numItems == 0) {
            // no items in category, remove button
            removeEmptyCategory(category);
        }
    }
}

// remove passed category button
function removeEmptyCategory(category) {
    let categoryButton = document.querySelector('#' + category + '-button');

    // remove category button
    categoryButton.parentNode.removeChild(categoryButton);
}

// set default category to first category
let firstCategoryButtonId = document.querySelector('.menu-navbar button').id;

// category name (singular) is category button text up to '-button'
let suffixIndex = firstCategoryButtonId.indexOf('-button');
let firstCategoryName = firstCategoryButtonId.substring(0, suffixIndex);
changeCategory(firstCategoryName);
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
