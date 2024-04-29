
console.log("Script loaded, adding event listener...");

document.body.addEventListener('click', function(event) {
    console.log("Click detected in body...");

    if (event.target && event.target.matches('.delete-trip-btn')) {
        console.log('Delete button clicked, attempting to delete trip with UUID:', event.target.getAttribute('data-trip-uuid'));

        const button = event.target; // The button that was clicked
        const tripUuid = button.getAttribute('data-trip-uuid');
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        if (confirm('Are you sure you want to delete this trip?')) {
            fetch(`delete-trip/${tripUuid}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({'trip_uuid': tripUuid}),
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log(data.message); // Log the success message
                button.closest('li').remove(); // Corrected to remove the entire list item
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }
});