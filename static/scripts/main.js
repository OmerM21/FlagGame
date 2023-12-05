function autocomplete(inp, arr, submitButton) {
    var currentFocus;
    var optionSelected = false;
  
    inp.addEventListener("input", function(e) {
      var val = this.value;
      closeAllLists();
  
      if (optionSelected) {
        return false;
      }
  
      currentFocus = -1;
  
      if (val.length === 0) {
        return; // Allow typing when the value is empty
      }
  
      var matchingItems = arr.filter(function(item) {
        return item.substr(0, val.length).toUpperCase() == val.toUpperCase();
      });
  
      if (matchingItems.length === 1) {
        inp.value = matchingItems[0];
        closeAllLists();
        optionSelected = true;
        inp.blur();
        submitButton.focus();
        return;
      }
  
      var a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(a);
  
      for (var i = 0; i < matchingItems.length; i++) {
        var b = document.createElement("DIV");
        b.innerHTML =
          "<strong>" + matchingItems[i].substr(0, val.length) + "</strong>";
        b.innerHTML += matchingItems[i].substr(val.length);
        b.innerHTML += "<input type='hidden' value='" + matchingItems[i] + "'>";
        b.addEventListener("click", function(e) {
          inp.value = this.getElementsByTagName("input")[0].value;
          closeAllLists();
          optionSelected = true;
          inp.blur();
          submitButton.focus();
        });
        a.appendChild(b);
      }
    });
  
    inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        currentFocus++;
        addActive(x);
      } else if (e.keyCode == 38) {
        currentFocus--;
        addActive(x);
      } else if (e.keyCode == 13) {
        e.preventDefault();
        if (currentFocus > -1) {
          if (x) x[currentFocus].click();
        }
      }
    });
  
    inp.addEventListener("blur", function() {
      optionSelected = false;
    });
  
    function addActive(x) {
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = x.length - 1;
      x[currentFocus].classList.add("autocomplete-active");
    }
  
    function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
  
    function closeAllLists(elmnt) {
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
  
    document.addEventListener("click", function(e) {
      closeAllLists(e.target);
    });
  }
  