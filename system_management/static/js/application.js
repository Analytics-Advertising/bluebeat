// NEW CODE //
document.addEventListener('DOMContentLoaded', function() {
    function enforceNumericLimit(inputId) {
        var input = document.getElementById(inputId);

        input.addEventListener('input', function() {
            // Remove any non-digit characters
            var value = input.value.replace(/\D/g, '');

            // Limit to 10 digits
            if (value.length > 10) {
                value = value.slice(0, 10);
            }

            input.value = value;
        });
    }

    // Apply to each phone number field
    enforceNumericLimit('app-phone-number');
    enforceNumericLimit('app-alt-phone-number');
    enforceNumericLimit('app-direct-phone-number');
});


document.addEventListener('DOMContentLoaded', function() {
    var otherCheckbox = document.getElementById('other');
    var otherInputGroup = document.getElementById('other-method-group');
    var otherInput = document.getElementById('app-other-method');

    // Show/hide "Please specify" field based on "Other" checkbox selection
    otherCheckbox.addEventListener('change', function() {
        if (otherCheckbox.checked) {
            otherInputGroup.style.display = 'block'; // Show the "Please specify" field
            otherInput.setAttribute('required', 'required'); // Make "Please specify" required
        } else {
            otherInputGroup.style.display = 'none'; // Hide the "Please specify" field
            otherInput.removeAttribute('required'); // Remove required from "Please specify"
        }
    });
});

  document.addEventListener('DOMContentLoaded', function() {
    var vatSelect = document.getElementById('app-vat-registration');
    var vatInputGroup = document.getElementById('vat-number-group');
    var vatInput = document.getElementById('vat-number');

    vatSelect.addEventListener('change', function() {
        if (vatSelect.value === 'Yes') {
            vatInputGroup.style.display = 'block'; // Show the VAT input field
            vatInput.setAttribute('required', 'required'); // Make VAT number required
        } else {
            vatInputGroup.style.display = 'none'; // Hide the VAT input field
            vatInput.removeAttribute('required'); // Remove required from VAT number
        }
    });
});


  
  function submitForm(formId) {
    var form = $('#' + formId);
        
        // Serialize form data
        var formData = form.serializeArray();
        
        // Check if all fields except VAT number (if not required) are filled
        var allFieldsFilled = true;

        formData.forEach(function(field) {
            // Skip validation for the VAT number if VAT registration is "No"
            if (field.name === 'vat-number' && $('#app-vat-registration').val() !== 'Yes') {
                return;  // Skip VAT number validation when not required
            }
             // Skip validation for "Please specify" if "Other" is not checked
             if (field.name === 'app-other-method' && !$('#other').is(':checked')) {
                return;  // Skip "Please specify" validation when not required
            }
            if (!field.value) {
                allFieldsFilled = false;  // If any required field is empty
            }
        });

        // If any required field is missing, show SweetAlert warning
        if (!allFieldsFilled) {
            swal.fire({
                title: 'Missing Fields!',
                text: 'Please fill out all required fields.',
                icon: 'warning',
                timer: 3000,
                timerProgressBar: true
            });
            return;  // Stop form submission
        }

    // AJAX request
    $.ajax({
        type: 'POST',
        url: form.attr('action'),  // Use form's action attribute as the URL
        data: $.param(formData),  // Convert formData back to query string
        dataType: 'json',
        success: function(response) {
            swal.fire({
                title: 'Success!',
                text: 'Application submitted successfully!',
                icon: 'success',
                button: 'OK'
            }).then(() => {
                location.reload(true);  // Reload the page after successful submission
            });
        },
        error: function(xhr, errmsg, err) {
            var errorMessage = 'Failed to submit application: ' + errmsg;
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = 'Failed to submit application: ' + xhr.responseJSON.error;
            }
            
            Swal.fire({
                title: 'Error!',
                text: errorMessage,
                icon: 'error',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    location.reload(true);  // Reload the page when the user clicks "OK"
                }
            });
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
