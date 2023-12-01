document.getElementById('submitBtn').addEventListener('click', function (event) {
  // Prevent the default form submission
  event.preventDefault();

  // Get input values
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;

  // Create FormData object
  var formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  // Send a POST request to the Flask backend
  fetch('/login', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (response.ok) {
          // Redirect to the main page after successful login
          window.location.href = '/'; // Change this if your main route is different
      } else {
          // Handle other response statuses, e.g., display an error message
          console.error('Error:', response.statusText);
      }
  })
  .catch(error => {
      console.error('Error:', error);
      // Handle errors, if any
  });
});
