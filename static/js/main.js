// Martin Faith - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length > 0) {
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-sm');
                navbar.classList.add('bg-white');
            } else {
                navbar.classList.remove('shadow-sm');
                if (!navbar.classList.contains('always-solid')) {
                    navbar.classList.remove('bg-white');
                }
            }
        });
    }

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
    if (alerts.length > 0) {
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    // Add animation to elements with data-animate attribute
    const animatedElements = document.querySelectorAll('[data-animate]');
    if (animatedElements.length > 0) {
        const checkVisibility = function() {
            animatedElements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const elementBottom = element.getBoundingClientRect().bottom;
                const isVisible = elementTop < window.innerHeight && elementBottom >= 0;

                if (isVisible && !element.classList.contains('animated')) {
                    const animation = element.getAttribute('data-animate');
                    element.classList.add('animated', animation);
                }
            });
        };

        // Check on scroll
        window.addEventListener('scroll', checkVisibility);

        // Check on page load
        checkVisibility();
    }

    // Like functionality
    const likeButtons = document.querySelectorAll('.like-button');
    if (likeButtons.length > 0) {
        likeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const contentType = this.dataset.contentType;
                const objectId = this.dataset.objectId;

                // Get CSRF token
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/like/${contentType}/${objectId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the like count
                        const likeCountElement = document.getElementById('like-count');
                        if (likeCountElement) {
                            likeCountElement.textContent = data.likes;
                        }

                        // Update button state
                        const heartIcon = button.querySelector('i');
                        if (data.liked) {
                            heartIcon.classList.remove('far');
                            heartIcon.classList.add('fas', 'text-danger');
                            button.innerHTML = `<i class="fas fa-heart me-1"></i> ${gettext("Unlike")}`;
                        } else {
                            heartIcon.classList.remove('fas', 'text-danger');
                            heartIcon.classList.add('far');
                            button.innerHTML = `<i class="far fa-heart me-1"></i> ${gettext("Like")}`;
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }
});