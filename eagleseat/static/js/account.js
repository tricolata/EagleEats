// set eventlisteners for input fields
for (input of document.querySelectorAll('input')) {
    if (input.type == 'password') {
        input.addEventListener('input', updateRequired);
    } else {
        input.addEventListener('input', updateSubmittable);
    }
}

// set event listeners for password fields
for (input of document.querySelectorAll('input[type="password"]')) {
    input.addEventListener('input', updateRequired);
}

function updateRequired() {
    passwordInputs = document.querySelectorAll('input[type="password"]');

    // set password field as required if they have data
    if (isPasswordRequired()) {
        // for each password field
        for (input of passwordInputs) {
            if (input.value.length > 0) {
                for (i of passwordInputs) {
                    i.required = true;
                }
            }
        }
    } else {
        // if we've reached here, none of the password fields are filled
        // so, set none of them required
        for (input of passwordInputs) {
            input.required = false;
        }
    }
}

// returns true if any of the password fields are filled
function isPasswordRequired() {
    for (input of document.querySelectorAll('input[type="password"]')) {
        if (input.value.length > 0) {
            return true;
        }
    }

    return false;
}

function hasMatchingPasswords() {
    let newPassword = document.querySelector('#new-password');
    let confirmPassword = document.querySelector('#confirm-password');

    return newPassword === oldPassword;
}
