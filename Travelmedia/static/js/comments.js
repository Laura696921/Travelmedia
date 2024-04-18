document.addEventListener('DOMContentLoaded', function() {
    let commentForms = document.querySelectorAll('.add-comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            let photoId = form.dataset.photoId;
            let formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                }
            })
            .then(response => response.json())
            .then(data => {
                let commentsContainer = document.querySelector(`#comments-container-${photoId}`);
                let commentText = document.createElement('p');
                commentText.textContent = data.text;
                commentsContainer.appendChild(commentText);
                form.reset(); // Clear the form after adding comment
                location.reload(); // Reload the page to display the added comment
            })
            .catch(error => {
                console.error('Error adding comment:', error);
            });
        });
    });

    // Event listener for "Show more" buttons
    let showMoreButtons = document.querySelectorAll('[id^="show-more-comments-"]');
    showMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            let photoId = button.id.split('-')[3];
            let additionalComments = document.querySelector(`#additional-comments-${photoId}`);
            additionalComments.style.display = 'block';
            button.style.display = 'none';  // Hide the "Show more" button

            // Append the "Hide" button if it doesn't exist
            if (!additionalComments.querySelector('.hide-button')) {
                let hideButton = document.createElement('button');
                hideButton.textContent = 'Hide';
                hideButton.className = 'btn btn-primary hide-button'; // Add a class to identify the Hide button
                hideButton.addEventListener('click', function() {
                    additionalComments.style.display = 'none';  // Hide additional comments
                    button.style.display = 'block';  // Show the "Show more" button again
                    hideButton.remove(); // Remove the Hide button
                });
                additionalComments.appendChild(hideButton);  // Append the "Hide" button
            }
        });
    });
});


document.addEventListener('submit', function(event) {
        if (event.target.classList.contains('add-comment-form')) {
            event.preventDefault();
            setTimeout(function() {
                window.location.reload();
            }, 1);  // Reload the page after 1 second
        }
    });

 document.addEventListener('submit', function(event) {
        if (event.target.classList.contains('add-comment-form') || event.target.classList.contains('delete-comment-form')) {
            event.preventDefault();
            setTimeout(function() {
                window.location.reload();
            }, 1000);  // Reload the page after 1 second
        }
    });

document.addEventListener('DOMContentLoaded', function() {
    let deleteForms = document.querySelectorAll('.delete-comment-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            let formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                }
            })
            .then(response => {
                if (response.ok) {
                    // Reload the page after successful deletion
                    window.location.reload();
                } else {
                    console.error('Error deleting comment:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error deleting comment:', error);
            });
        });
    });
});