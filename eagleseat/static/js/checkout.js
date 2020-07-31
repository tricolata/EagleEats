function showCard() {
    var x = document.getElementById("creditCard");
    x.style.display = "flex";
    var y = document.getElementById("opener");
    y.style.display="none";
    var z = document.getElementById("cash");
    z.style.display="none";
    
      
      
      
      
  }
  function showCash() {
    var x = document.getElementById("cash");
    x.style.display = "block";
    var y = document.getElementById("opener");
    y.style.display="none";
    var z = document.getElementById("creditCard");
    z.style.display="none";


  }
  function viewOrder() {
    var x = document.getElementById("orderSummary");
    
    if (window.getComputedStyle(x).display == "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }
