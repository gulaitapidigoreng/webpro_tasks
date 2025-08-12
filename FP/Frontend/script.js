document.addEventListener('DOMContentLoaded', () => {
    fetchGames();

    // --- ALL EVENT LISTENERS ---
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');
    const authMessage = document.getElementById('auth-message');
    const addGameForm = document.getElementById('add-game-form');

    // Listener for the registration form
    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault(); 
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Registration failed');
            }

            const result = await response.json();
            authMessage.textContent = `User '${result.username}' registered successfully! Please log in.`;
            authMessage.style.color = 'green';
            registerForm.reset();
        } catch (error) {
            authMessage.textContent = error.message;
            authMessage.style.color = 'red';
        }
    });

    // Listener for the login form
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed');
            }

            const result = await response.json();
            localStorage.setItem('token', result.access_token);
            authMessage.textContent = 'Login successful!';
            authMessage.style.color = 'green';
            loginForm.reset();
        } catch (error) {
            authMessage.textContent = error.message;
            authMessage.style.color = 'red';
        }
    });

    // Listener for the logout button
    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('token');
        authMessage.textContent = 'You have been successfully logged out.';
        authMessage.style.color = 'blue';
    });

    // Listener for the "Add Game" form
    addGameForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const token = localStorage.getItem('token');
        if (!token) {
            alert('You must be logged in to add a game.');
            return;
        }

        const title = document.getElementById('game-title').value;
        const genre = document.getElementById('game-genre').value;
        const platform = document.getElementById('game-platform').value;
        const release_year = document.getElementById('game-release-year').value;
        const description = document.getElementById('game-description').value;

        try {
            const response = await fetch('http://127.0.0.1:8000/api/games/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    title,
                    genre,
                    platform,
                    release_year: parseInt(release_year),
                    description,
                    cover: "default.jpg"
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to add game.');
            }
            
            addGameForm.reset();
            fetchGames();
        } catch (error) {
            alert(error.message);
        }
    });
});

// --- Function to fetch all games and their reviews ---
async function fetchGames() {
    const gamesContainer = document.getElementById('games-container');
    try {
        const gamesResponse = await fetch('http://127.0.0.1:8000/api/games', { cache: 'no-cache' });
        if (!gamesResponse.ok) throw new Error('Failed to load games.');
        
        const games = await gamesResponse.json();
        gamesContainer.innerHTML = ''; 

        for (const game of games) {
            const reviewsResponse = await fetch(`http://127.0.0.1:8000/api/reviews/game/${game.id}`);
            const reviews = await reviewsResponse.json();

            let reviewsHtml = '<p class="text-muted small">No reviews yet.</p>';
            if (reviews.length > 0) {
                reviewsHtml = '<ul class="reviews-list">' + reviews.map(review => 
                    `<li>
                        <strong>${review.owner.username} (${review.rating}/10):</strong> ${review.review_text}
                        <button class="btn btn-sm btn-outline-danger float-end delete-review-btn" data-review-id="${review.id}">X</button>
                    </li>`
                ).join('') + '</ul>';
            }

            const gameCardWrapper = document.createElement('div');
            gameCardWrapper.className = 'col-lg-4 col-md-6 mb-4';
            gameCardWrapper.innerHTML = `
                <div class="card h-100 game-card">
                    <div class="card-body d-flex flex-column">
                        <h3 class="card-title h5">${game.title}</h3>
                        <p class="card-text text-muted small">${game.genre} | ${game.platform}</p>
                        <p class="card-text flex-grow-1">${game.description || 'No description available'}</p>
                        <div class="mt-auto">
                            <h4 class="h6">Reviews</h4>
                            ${reviewsHtml}
                            <div class="review-section mt-3">
                                <form class="review-form" data-game-id="${game.id}">
                                    <div class="input-group">
                                        <input type="number" class="form-control rating-input" min="1" max="10" placeholder="Rating" required>
                                        <input type="text" class="form-control comment-input" placeholder="Write a review..." required>
                                        <button type="submit" class="btn btn-primary">Submit</button>
                                    </div>
                                </form>
                                <div class="review-message small mt-2"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            gamesContainer.appendChild(gameCardWrapper);
        }
        
        addReviewFormListeners();
        addDeleteReviewListeners();

    } catch (error) {
        console.error("Could not fetch games:", error);
    }
}

// --- Function to add listeners for all review submission forms ---
function addReviewFormListeners() {
    const reviewForms = document.querySelectorAll('.review-form');
    reviewForms.forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to submit a review.');
                return;
            }

            const gameId = form.dataset.gameId;
            const rating = form.querySelector('.rating-input').value;
            const comment = form.querySelector('.comment-input').value;
            const messageDiv = form.nextElementSibling;

            try {
                const response = await fetch('http://127.0.0.1:8000/api/reviews/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        game_id: parseInt(gameId),
                        rating: parseInt(rating),
                        review_text: comment
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    messageDiv.style.color = 'red';
                    throw new Error(errorData.detail || 'Failed to submit review.');
                }
                
                messageDiv.style.color = 'green';
                messageDiv.textContent = 'Review submitted successfully!';
                form.reset();
                fetchGames();
            } catch (error) {
                messageDiv.textContent = error.message;
            }
        });
    });
}

// --- Function to add listeners for all review delete buttons ---
function addDeleteReviewListeners() {
    const deleteButtons = document.querySelectorAll('.delete-review-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const reviewId = button.dataset.reviewId;
            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to delete a review.');
                return;
            }

            if (confirm('Are you sure you want to delete this review?')) {
                try {
                    const response = await fetch(`http://127.0.0.1:8000/api/reviews/${reviewId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to delete review.');
                    }
                    
                    fetchGames();
                } catch (error) {
                    alert(error.message);
                }
            }
        });
    });
}