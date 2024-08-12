function addPricing() {
    var departure = document.getElementById('departure').value;
    var destination = document.getElementById('destination').value;
    var passengerRange = document.getElementById('passenger-range').value;
    var price = document.getElementById('price').value;

    // Validate all fields are filled
    if (!departure || !destination || !passengerRange || !price) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Please fill out all fields.'
        });
        return;
    }

    // Prepare data object
    var data = {
        'departure': departure,
        'destination': destination,
        'passenger_range': passengerRange,
        'price': price,
        'csrfmiddlewaretoken': csrf_token
    };

    // Send data via AJAX POST request
    $.ajax({
        url: add_pricing_url,  // Replace with your Django URL
        method: 'POST',
        data: data,
        success: function(response) {
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Pricing added successfully!'
            }).then(function() {
                location.reload();  // Reload the page after successful addition
            });
            $('#addPricingModal').modal('hide');  // Close modal
        },
        error: function(xhr, status, error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to add pricing. Please try again.'
            });
        }
    });
}
