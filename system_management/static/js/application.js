// NEW CODE //

document.addEventListener('DOMContentLoaded', function() {
    var otherCheckbox = document.getElementById('other');
    var otherInput = document.getElementById('other-method-group');
  
    otherCheckbox.addEventListener('change', function() {
      if (otherCheckbox.checked) {
        otherInput.style.display = 'block';
      } else {
        otherInput.style.display = 'none';
      }
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    var vatSelect = document.getElementById('app-vat-registration');
    var vatInputGroup = document.getElementById('vat-number-group');
  
    vatSelect.addEventListener('change', function() {
      if (vatSelect.value === 'Yes') {
        vatInputGroup.style.display = 'block';
      } else {
        vatInputGroup.style.display = 'none';
      }
    });
  });

  
  function submitForm(formId) {
    var form = $('#' + formId);
    
    // Serialize form data
    var formData = form.serialize();

    console.log(formData);

    // AJAX request
    $.ajax({
        type: 'POST',
        url: form.attr('action'),  // Use form's action attribute as the URL
        data: formData,
        dataType: 'json',
        success: function(response) {
            alert('Application submitted successfully!');  // Show success message
            location.reload(true);  // Reload the page after successful submission
        },
        error: function(xhr, errmsg, err) {
            // Display errors from Django view
            if (xhr.responseJSON && xhr.responseJSON.error) {
                alert('Failed to submit application: ' + xhr.responseJSON.error);  // Show Django view's error message
            } else {
                alert('Failed to submit application: ' + errmsg);  // Show general error message
            }
        }
    });

}

// NEW CODE //


// Function to retrieve the current tab index from browser storage
function getCurrentTab() {
    return sessionStorage.getItem('currentTab') || 0;
}

// Function to save the current tab index in browser storage
function setCurrentTab(tabIndex) {
    sessionStorage.setItem('currentTab', tabIndex);
}


var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {

    var x = document.getElementsByClassName("step");
    for (var i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[n].style.display = "block";

    

    //... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "next";
    }

    // Set the current tab index in browser storage
    setCurrentTab(n);

    // Run a function to display the correct step indicator
    fixStepIndicator(n);
}

// Function to initialize the form
function initializeForm() {
    var currentTab = getCurrentTab(); // Get the current tab index from browser storage
    showTab(parseInt(currentTab)); // Display the current tab
}

// Call the initializeForm function when the page loads
window.onload = initializeForm;


function nextPrev(n) {
    var x = document.getElementsByClassName("step");
    if (n == 1 && !validateForm()) {
        alert("Please fill in all required fields.");
        return false;
    }
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    if (currentTab >= x.length) {
        submitForm("signUpForm");
        return false;
    }
    showTab(currentTab);
}


function validateForm() {
    var isValid = true;
    var x = document.getElementsByClassName("step")[currentTab].querySelectorAll('input, select');
    for (var i = 0; i < x.length; i++) {
        if (x[i].required && !x[i].value.trim()) {
            isValid = false;
            break;
        }
    }
    return isValid;
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("stepIndicator");
    for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class on the current step:
    x[n].className += " active";
}
