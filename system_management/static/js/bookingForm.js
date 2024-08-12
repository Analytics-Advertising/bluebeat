///... NEW CODE ...///

document.addEventListener('DOMContentLoaded', function() {


    var disabilitySelect = document.getElementById('app-disability');
    var wheelchairGroup = document.getElementById('wheelchair-group');
    var specifyDisabilityGroup = document.getElementById('specify-disability-group');

    disabilitySelect.addEventListener('change', function() {
        if (disabilitySelect.value === 'Yes') {
            wheelchairGroup.style.display = 'block';
            specifyDisabilityGroup.style.display = 'block';
        } else {
            wheelchairGroup.style.display = 'none';
            specifyDisabilityGroup.style.display = 'none';
        }
    });


    var appointmentTimeSelect = document.getElementById('booking-time');
    var startTime = 8; // Start time in hours (08:00)
    var endTime = 19; // End time in hours (19:00)

    for (var hour = startTime; hour <= endTime; hour++) {
        var option = document.createElement('option');
        var timeString = hour.toString().padStart(2, '0') + ':00';
        option.value = timeString;
        option.textContent = timeString;
        appointmentTimeSelect.appendChild(option);
    }

    var flightTimeSelect = document.getElementById('flighttime');

    for (var hour = startTime; hour <= endTime; hour++) {
        var option = document.createElement('option');
        var timeString = hour.toString().padStart(2, '0') + ':00';
        option.value = timeString;
        option.textContent = timeString;
        flightTimeSelect.appendChild(option);
    }


    var agreeTCCheckbox = document.getElementById('agree-tc');
    var paymentMethods = document.getElementById('payment-methods');

    agreeTCCheckbox.addEventListener('change', function() {
        if (agreeTCCheckbox.checked) {
            paymentMethods.style.display = 'block';
        } else {
            paymentMethods.style.display = 'none';
        }
    });

    // Populate the flight time dropdown with hourly intervals from 08:00 to 19:00
    var flightTimeSelect = document.getElementById('flighttime');
    var startTime = 8; // Start time in hours (08:00)
    var endTime = 19; // End time in hours (19:00)

    for (var hour = startTime; hour <= endTime; hour++) {
        var option = document.createElement('option');
        var timeString = hour.toString().padStart(2, '0') + ':00';
        option.value = timeString;
        option.textContent = timeString;
        flightTimeSelect.appendChild(option);
    }

});






///... NEW CODE ...///



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
        document.getElementById("nextBtn").innerHTML = "<i class='fa-solid fa-angles-right'></i>";
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
        submitForm();
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


