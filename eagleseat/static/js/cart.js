function removeFromCart(pos) {
    var form = document.createElement('form');
    form.action = '/cart'
    form.method = 'post';

    // dummy input elements
    const removeInput = document.createElement('input');
    removeInput.name = 'removePos';
    removeInput.value = pos;

    form.appendChild(removeInput);

    form.submit();
}
