// NEW CODE //



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

    // Fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }

    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").style.display = "none"; // Hide the Next button on the last step
    } else {
        document.getElementById("nextBtn").style.display = "inline"; // Show the Next button on other steps
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
