<template>
  <div class="rate-books-container">
    <h1>Rate & Give Feedback</h1>
    <button @click="goToMainDashboard" class="main-dashboard-button">
      Main Dashboard
    </button>
    <div v-if="grantedBooks.length > 0" class="books-list">
      <div v-for="book in grantedBooks" :key="book.book_id" class="book-item">
        <h2>{{ book.name }}</h2>
        <p><strong>Author:</strong> {{ book.author }}</p>
        <p><strong>Average Rating:</strong> {{ book.rating }} Star(s)</p>
        <div class="rating">
          <label for="rating">Rating:</label>
          <select v-model="book.rating" id="rating">
            <option disabled value="">Select Rating</option>
            <option v-for="n in 5" :key="n" :value="n">{{ n }} Star(s)</option>
          </select>
        </div>
        <div class="feedback">
          <label for="feedback">Feedback:</label>
          <textarea v-model="book.feedback" id="feedback" rows="3" placeholder="Write your feedback here..."></textarea>
        </div>
        <button @click="submitRating(book)" :disabled="!book.rating || !book.feedback">
          Submit
        </button>
      </div>
    </div>
    <div v-else class="no-books">
      <p>No granted books available for rating.</p>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "RateBooks",
  data() {
    return {
      grantedBooks: [],
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    goToMainDashboard() {
      const username = localStorage.getItem('username');
      this.$router.push({ name: 'UserDashboard', params: { username } });
    },
    fetchBooks() {
  const userId = localStorage.getItem('userId');
  if (!userId) {
    this.error = 'User not authenticated';
    this.loading = false;
    return;
  }

  axios.get(`http://localhost:5000/api/user-bookss?user_id=${userId}`)
    .then(response => {
      // Directly use the average rating from the backend
      this.grantedBooks = response.data;
      this.loading = false;
    })
    .catch(error => {
      console.error('Error fetching books:', error);
      this.error = 'Failed to fetch books. Please try again.';
      this.loading = false;
    });
},



submitRating(book) {
  if (!book.rating || !book.feedback) {
    alert('Please provide both rating and feedback.');
    return;
  }
  const userId = localStorage.getItem('userId');
  axios.post('http://localhost:5000/api/rate-book', {
    user_id: userId,
    book_id: book.id,
    rating: book.rating,
    feedback: book.feedback
  })
  .then(() => {
    alert('Rating and feedback submitted successfully!');
    // Clear local values
    book.rating = '';
    book.feedback = '';
    // Refresh book list to update average ratings
    this.fetchBooks();
  })
  .catch(error => {
    console.error('Error submitting rating and feedback:', error);
    alert('Failed to submit rating and feedback. Please try again.');
  });
}
  }
};
</script>

<style scoped>
.main-dashboard-button {
  padding: 10px 20px;
  font-size: 16px;
  color: #ffffff;
  background-color: #7091E6; /* Primary color */
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: block;
  margin: 0 auto 30px;
  transition: background-color 0.3s ease;
}

.main-dashboard-button:hover {
  background-color: #4a74d3; /* Darker shade */
}

.rate-books-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #EDE8F5; /* White background for contrast */
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.rate-books-container h1 {
  text-align: center;
  font-size: 2rem;
  color: #333333; /* Darker text for readability */
  margin-bottom: 20px;
}

.books-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.book-item {
  padding: 15px;
  background-color: #f9f9f9; /* Light grey background */
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.book-item h2 {
  font-size: 1.5rem;
  color: #333333;
  margin-bottom: 10px;
}

.book-item p {
  color: #666666;
  margin-bottom: 15px;
}

.rating,
.feedback {
  margin-bottom: 15px;
}

.rating label,
.feedback label {
  display: block;
  font-size: 1rem;
  color: #4a4a4a; /* Slightly darker for better readability */
  margin-bottom: 5px;
}

select,
textarea {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ddd;
  box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.05);
}

textarea {
  resize: vertical; /* Allow vertical resize only */
}

button {
  padding: 10px;
  font-size: 1.1rem;
  color: #ffffff;
  background-color: #28a745; /* Green color for the submit button */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  background-color: #218838; /* Darker green on hover */
}

.no-books {
  text-align: center;
  font-size: 1.2rem;
  color: #999999;
}
</style>
