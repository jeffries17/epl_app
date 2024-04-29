document.addEventListener("DOMContentLoaded", function() {
  // Add item
  const addItemForm = document.getElementById('add-item-form');
  addItemForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch(`add-item-url/${packingListUniqueId}/`, {  // Replace with your actual URL
      method: 'POST',
      body: formData,
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Update UI to show the new item
        // Placeholder: Append to items list
      } else {
        // Handle errors
      }
    });
  });

  // Toggle item packed status
  document.querySelectorAll('.toggle-packed-btn').forEach(button => {
    button.addEventListener('click', function() {
      const itemId = this.dataset.itemId;
      fetch(`toggle-item-packed-status-url/${itemId}/`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCSRFToken(), // Implement getCSRFToken function or use 'csrftoken' cookie
        },
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Toggle item's packed status in UI
          // Placeholder: Update item element's class or content
        }
      });
    });
  });
});

function getCSRFToken() {
  // Implement CSRF token retrieval
}
