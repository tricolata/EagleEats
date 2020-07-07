window.addEventListener('load', setActiveTab);

function setActiveTab() {
    // get last segment of page path
    let pageName = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
    let activeTab = undefined;
    switch (pageName) {
        case 'deals': {
            activeTab = document.querySelector('#deals-button');
            break;
        }

        case 'menu': {
            activeTab = document.querySelector('#menu-button');
            break;
        }

        case 'login': {
            activeTab = document.querySelector('#login-button');
            break;
        }

        case 'signup': {
            activeTab = document.querySelector('#signup-button');
            break;
        }

        case 'cart': {
            activeTab = document.querySelector('#cart-button');
            break;
        }
    }

    activeTab.classList.add('active');
}