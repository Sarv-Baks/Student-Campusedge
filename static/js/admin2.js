document.getElementById('course-form').addEventListener('submit', function (event) {
    event.preventDefault();

    // Get form data
    const courseName = document.getElementById('courseName').value;
    const section = document.getElementById('section').value;

    // Send the form data to the server (Assuming you are using fetch API)
    fetch('/add_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            courseName: courseName,
            section: section
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Course added successfully!');
        } else {
            alert('Failed to add course. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
