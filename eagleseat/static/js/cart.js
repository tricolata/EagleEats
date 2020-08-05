function removeFromCart(pos) {
    var form = document.createElement('form');
    form.action = '/cart'
    form.method = 'post';

    form.style.display = 'none';

    // dummy input elements
    const removeInput = document.createElement('input');
    removeInput.name = 'removePos';
    removeInput.value = pos;

    form.appendChild(removeInput);

    document.querySelector('body').appendChild(form)

    form.submit();
}

// disable checkout button for empty cart
window.addEventListener('load', () => {
    // get order items
    let orderItems = document.querySelectorAll('.orderItem');

    if (orderItems.length == 0) {
        document.getElementById('checkout').disabled = true;
    }
});
