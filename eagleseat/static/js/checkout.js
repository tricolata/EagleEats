// hide submit button on page load
window.addEventListener('load', () => {
    document.getElementById("submit").style.display = 'none';
});

function showCard() {
    var x = document.getElementById("creditCard");
    x.style.display = "flex";
    var y = document.getElementById("opener");
    y.style.display="none";
    var z = document.getElementById("cash");
    z.style.display="none";

    // set card details as required
    var cardNumber = document.querySelector('input[name="cardNumber"]');
    cardNumber.required = true;

    var expDate = document.querySelector('input[name="expDate"]');
    expDate.required = true;

    var submitButton = document.getElementById("submit")
    submitButton.style.display = 'block';
    
  }
  function showCash() {
    var x = document.getElementById("cash");
    x.style.display = "block";
    x.required = false
    var y = document.getElementById("opener");
    y.style.display="none";
    y.required = false
    var z = document.getElementById("creditCard");
    z.style.display="none";

    // set card details as not required
    var cardNumber = document.querySelector('input[name="cardNumber"]');
    cardNumber.required = false;

    var expDate = document.querySelector('input[name="expDate"]');
    expDate.required = false;

    var submitButton = document.getElementById("submit")
    submitButton.style.display = 'block';

  }
  function viewOrder() {
    var x = document.getElementById("orderSummary");
    
    if (window.getComputedStyle(x).display == "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }
