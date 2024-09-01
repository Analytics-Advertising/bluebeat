function generateRandomPassword(length) {
    var charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    var password = "";
    for (var i = 0; i < length; i++) {
        var randomIndex = Math.floor(Math.random() * charset.length);
        password += charset[randomIndex];
    }
    return password;
}


function registerNewUser() {
    // Get input values
    var firstName = $('#first-name').val();
    var lastName = $('#last-name').val();
    var email = $('#email').val();
    var phoneNumber = $('#PhoneNumber').val();
    var userType = $('#user-type').val();
    // Generate random password
    var password = generateRandomPassword(10);

    // Check if any field is empty
    if (!firstName || !lastName || !email || !phoneNumber ||  !userType ) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'All fields are required. Please fill out all fields.'
        });
        return;
    }

    // Send AJAX request to register user
    $.ajax({
        url: register_user_url,
        method: 'POST',
        data: {
            'first-name': firstName,
            'last-name': lastName,
            'email': email,
            'PhoneNumber': phoneNumber,
            'user-type': userType,
            'password': password,
            'csrfmiddlewaretoken': csrf_token
        },
        success: function(response) {
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'User registered successfully'
            }).then(() => {
                // Close the modal
                $('#addUserModal').modal('hide');
                location.reload();  // Optionally reload the page or update the UI
            });
        },
        error: function(xhr, status, error) {
            var errorMessage = 'Failed to register user. Please try again.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: errorMessage
            });
        }
    });
}

function viewUser(userId) {
    var url = get_user_details_url.replace('/0/', '/' + userId + '/'); // Replace the placeholder ID with the actual userId
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            $('#userFirstName').text(data.first_name);
            $('#userLastName').text(data.last_name);
            $('#userEmail').text(data.email);
            $('#userModal').modal('show');
        },
        error: function(error) {
            console.log("Error:", error);
        }
    });
  }


function deactivateUser(userId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "Do you really want to deactivate this user?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, deactivate!'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: deactivate_user_url,  // Update with your deactivate user URL
                method: 'POST',
                data: {
                    'user_id': userId,
                    'csrfmiddlewaretoken': csrf_token
                },
                success: function(response) {
                    Swal.fire(
                        'Deactivated!',
                        'User has been deactivated.',
                        'success'
                    ).then(() => {
                        location.reload();  // Optionally reload the page or update the UI
                    });
                },
                error: function(xhr, status, error) {
                    Swal.fire(
                        'Error!',
                        'Failed to deactivate user.',
                        'error'
                    );
                }
            });
        }
    });
}
