// set event listeners for password fields
for (input of document.querySelectorAll('input[type="password"]')) {
    input.addEventListener('input', updateRequired);
}

function updateRequired() {
    password_inputs = document.querySelectorAll('input[type="password"]')

    // for each password field
    for (input of password_inputs) {
        input.required = true;
        // if any input is filled, they are all required
        if (input.value.length > 0) {
            for (i of password_inputs) {
                i.required = true;
            }

            return;
        }
    }

    // if we've reached here, none of the password fields are filled
    // so, set none of them required
    for (input of password_inputs) {
        input.required = false;
    }
}
