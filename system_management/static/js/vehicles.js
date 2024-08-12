function addVehicle() {
    // Retrieve form data
    var make = document.getElementById('make').value;
    var model = document.getElementById('model').value;
    var year = document.getElementById('year').value;
    var registration = document.getElementById('registration').value;
    var group = document.getElementById('group').value;
    var wheelchairSafe = document.getElementById('wheelchair-safe').value;
    var capacity = document.getElementById('capacity').value;

    // Retrieve image file
    var imageFile = document.getElementById('image').files[0];

    // Validate all fields are filled
    if (!make || !model || !year || !registration || !group || !wheelchairSafe || !capacity || !imageFile) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Please fill out all fields.'
        });
        return;
    }

    // Convert image to base64
    var reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onload = function () {
        var imageBase64 = reader.result.split(',')[1];  // Get base64 part of the result
        document.getElementById('imageBase64').value = imageBase64;  // Set hidden input value


    // Create data object
    var data = {
        'make': make,
        'model': model,
        'year': year,
        'registration': registration,
        'group': group,
        'wheelchair_safe': wheelchairSafe,
        'capacity': capacity,
        'imageBase64': imageBase64,
        'csrfmiddlewaretoken': csrf_token 
    };

    // Send data via AJAX POST request
    $.ajax({
        url: add_vehicle_url,
        method: 'POST',
        data: data,
        success: function(response) {
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Vehicle added successfully!'
            }).then(function() {
                location.reload();  // Reload the page after successful addition
            });
            $('#addVehicleModal').modal('hide');  // Close modal
        },
        error: function(xhr, status, error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to add vehicle. Please try again.'
            });
        }
    });
}
}
