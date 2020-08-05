// disable checkout button for empty cart
window.addEventListener('load', () => {
    // get order items
    let orderItems = document.querySelectorAll('.orderItem');

    if (orderItems.length == 0) {
        document.getElementById('checkout').disabled = true;
    }
});
