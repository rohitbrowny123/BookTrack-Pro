<template>
  <div class="user-dashboard">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-top">
        <h1 class="dashboard-heading">User's Dashboard</h1>
        <div class="header-buttons">
          <button class="button" @click="goToRate">Rates</button>
          <button class="button" @click="goToMyBooks">Granted Books</button>
          <button class="button" @click="goToStats">Stats</button>
          <button class="button" @click="logout">Logout</button>
        </div>
        <div class="search-bar">
          <input 
            type="text" 
            placeholder="Search books by title, author, or section..." 
            v-model="searchQuery" 
            @keyup.enter="performSearch" 
          />
          <button @click="performSearch">Search</button>
        </div>
      </div>
    </header>

    <!-- User Info Section -->
    <main class="user-info">
      <p v-if="user" class="welcome-message">Welcome {{ user.username }}</p>
      <h2>Profile</h2>
      <div v-if="user">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Role:</strong> {{ user.roles && user.roles.length ? user.roles[0].name : 'No role assigned' }}</p>
      </div>
      <div v-else>
        <p>Loading user information...</p>
      </div>
      <button @click="showUpdateForm = true" class="update-button">Update</button>
      
      <!-- Update User Info Form -->
      <div v-if="showUpdateForm" class="update-form">
        <h3>Update Profile</h3>
        <form @submit.prevent="updateUserInfo">
          <div class="form-group">
            <label for="newUsername">Username:</label>
            <input type="text" v-model="newUsername" :placeholder="user.username" required />
          </div>
          <div class="form-group">
            <label for="newEmail">Email:</label>
            <input type="email" v-model="newEmail" :placeholder="user.email" required />
          </div>
          <div class="form-group">
            <label for="newPassword">Password:</label>
            <input type="password" v-model="newPassword" placeholder="New password" />
          </div>
          <div class="form-buttons">
            <button type="submit" class="submit-button">Update</button>
            <button type="button" @click="showUpdateForm = false" class="cancel-button">Cancel</button>
          </div>
        </form>
      </div>

    </main>

    <!-- Books Section -->
    <section class="books-section">
      <h2>All Books</h2>
      <div v-if="filteredBooks.length">
        <table class="books-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Author</th>
              <th>Section</th>
              <th>Status</th>
              <th>Description</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in filteredBooks" :key="book.id">
              <td>{{ book.name }}</td>
              <td>{{ book.author }}</td>
              <td>{{ book.section }}</td>
              <td>{{ book.status }}</td>
              <td>{{ book.description }}</td>
              <td>
                <button 
                  class="request-button" 
                  :disabled="isLoading || requestedBooks.has(book.id)"
                  @click="requestBook(book)"
                >
                  {{ isLoading ? 'Loading...' : (requestedBooks.has(book.id) ? 'Requested' : 'Request') }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No Books Available...</p>
      </div>
    </section>

    <!-- Popup Modal for Book Request -->
    <div v-if="showRequestModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeRequestModal">&times;</span>
        <h2>Request Book</h2>
        <p>{{ selectedBook ? selectedBook.name : '' }}</p>
        <form @submit.prevent="submitBookRequest">
          <div>
            <label for="duration">Duration (days):</label>
            <input type="number" v-model="form.duration" required />
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:5000';  // Flask server's address
axios.defaults.withCredentials = true;

export default {
  data() {
    return {
      searchQuery: '',
      user: null,
      books: [],
      requestedBooks: new Set(),
      isLoading: true,
      showRequestModal: false,
      selectedBook: null,
      form: {
        duration: 7,
      },
      showUpdateForm: false,
      newUsername: '',
      newEmail: '',
      newPassword: '',
    };
  },
  computed: {
    filteredBooks() {
      return this.books.filter(book => {
        const query = this.searchQuery.toLowerCase();
        return (
          book.name.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.section.toLowerCase().includes(query)
        );
      });
    }
  },
  methods: {
    goToMyBooks() {
      const username = this.user ? this.user.username : null;
      if (username) {
        this.$router.push({ name: 'UserMyBooks', params: { username } });
      } else {
        alert('User information is not available.');
      }
    },
    goToStats() {
    this.$router.push({ name: 'UserStats' });
  },
  goToRate() {
    this.$router.push({ name: 'RateBooks' });
  },
    logout() {
      this.$router.push({ name: 'Login' });
    },
    performSearch() {
      console.log('Searching for:', this.searchQuery);
      // Fetch books based on the search criteria
      axios.get('/api/books', {
        params: {
          query: this.searchQuery
        }
      })
      .then(response => {
        this.books = response.data;
      })
      .catch(error => {
        console.error('Error fetching books:', error);
      });
    },
    fetchUserInfo() {
      this.isLoading = true;
      const username = this.$route.params.username;
      console.log('Fetching user info for:', username);
      return axios.get(`/api/users/${username}`)
        .then(response => {
          console.log('User data received:', response.data);
          this.user = response.data;
          this.isLoading = false;
        })
        .catch(error => {
          console.error('Error fetching user information:', error);
          this.isLoading = false;
        });
    },
    fetchBooks() {
      const userId = this.user ? this.user.id : null;
      Promise.all([
        axios.get('/api/books'),
        axios.get('/api/requested-books', { params: { user_id: userId } })
      ])
        .then(([booksResponse, requestedBooksResponse]) => {
          this.books = booksResponse.data;
          const requestedBooks = new Set(requestedBooksResponse.data.map(request => request.book_id));
          this.requestedBooks = requestedBooks;
        })
        .catch(error => {
          console.error("Error fetching books or requested books:", error);
        });
    },
    requestBook(book) {
      if (this.isLoading) {
        alert("Please wait for user information to load before requesting a book.");
        return;
      }
      if (!this.user || !this.user.id) {
        console.warn("User information not yet available for book request.");
        alert("Please wait for user information to load before requesting a book.");
        return;
      }
      if (this.requestedBooks.size >= 5) {
        alert("You can only request a maximum of 5 books.");
        return;
      }
      this.selectedBook = book;
      this.showRequestModal = true;
    },
    closeRequestModal() {
      this.showRequestModal = false;
      this.selectedBook = null;
      this.form.duration = 7;
    },
    submitBookRequest() {
      const { duration } = this.form;
      const bookId = this.selectedBook.id;
      const userId = this.user.id;

      axios.post('/api/book-requested', {
        book_id: bookId,
        user_id: userId,
        days_requested: duration,
      })
      .then(response => {
        if (response.status === 201) {
          this.requestedBooks.add(bookId);
          alert('Request submitted successfully!');
          this.closeRequestModal();
        } else {
          alert('An error occurred. Please try again.');
        }
      })
      .catch(error => {
        console.error("Error submitting book request:", error);
        alert('An error occurred. Please try again.');
      });
    },
    updateUserInfo() {
      const updatedData = {
        username: this.newUsername || this.user.username,
        email: this.newEmail || this.user.email,
        password: this.newPassword || undefined
      };
      
      axios.put(`/api/users/${this.user.username}`, updatedData)
        .then(response => {
          alert('User information updated successfully!');
          this.user = response.data;
          this.showUpdateForm = false;
        })
        .catch(error => {
          console.error('Error updating user information:', error);
          alert('An error occurred while updating your information.');
        });
    }
  },
  mounted() {
    this.fetchUserInfo()
      .then(() => {
        this.fetchBooks();
      });
  }
};
</script>



<style scoped>
.update-button {
  background-color: #a8e167;
  color: rgb(27, 26, 26);
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}

.update-button:hover {
  background-color: #aed383;
}

/* Style for the update form container */
.update-form {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Style for form headings */
.update-form h3 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

/* Style for form groups */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

/* Style for buttons */
.form-buttons {
  display: flex;
  justify-content: space-between;
}

.submit-button,
.cancel-button {
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  color: white;
}

.submit-button {
  background-color: #28a745;
}

.submit-button:hover {
  background-color: #218838;
}

.cancel-button {
  background-color: #dc3545;
}

.cancel-button:hover {
  background-color: #c82333;
}

.modal {
  display: block; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgba(0, 0, 0, 0.5); /* Black w/ opacity */
  padding-top: 50px; /* Space at the top */
}

/* Modal content */
.modal-content {
  background-color: #ffffff; /* White background for the content */
  margin: auto; /* Center horizontally */
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 15px; /* Rounded corners */
  width: 80%; /* Width of the modal */
  max-width: 500px; /* Max width for the modal */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
  animation: fadeIn 0.3s; /* Fade-in animation */
}

/* Close button */
.close {
  color: #aaa;
  float: right;
  font-size: 24px;
  font-weight: bold;
}

/* Hover effects for close button */
.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}

/* Fade-in animation */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Form styles inside modal */
.modal-content form {
  display: grid;
  gap: 15px;
}

.modal-content label {
  font-weight: bold;
}

.modal-content input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.modal-content button {
  padding: 10px;
  background-color: #7091E6; /* Main color */
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.modal-content button:hover {
  background-color: #4a74d3; /* Darker shade on hover */
}

.user-dashboard {
  padding: 20px;
  background-color: #EDE8F5;
}

.dashboard-header {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-heading {
  font-size: 32px;
  font-weight: bold;
  color: #000;
}

.welcome-message {
  font-size: 34px;
  margin: 0 20px;
  color: #3d52a0;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #7091E6;
  color: #fff;
  border: none;
  border-radius: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  flex: 1;
  border: 2px solid #7091E6;
  border-radius: 20px;
  background-color: #fff;
  color: #333;
}

.search-bar button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #7091E6;
  color: #fff;
  border: none;
  border-radius: 20px;
}

.user-info {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.user-info h2 {
  margin-bottom: 15px;
  color: #333;
}

.user-info p {
  margin: 10px 0;
  color: #666;
}

.books-section {
  margin-top: 20px;
}

.books-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.books-table th, .books-table td {
  padding: 10px;
  text-align: left;
}

.books-table th {
  background-color: #7091E6;
  color: #fff;
}

.books-table tbody tr:nth-child(even) {
  background-color: #f5f5f5;
}

.books-table tbody tr:hover {
  background-color: #e0e7ff;
}

.request-button {
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
  background-color: #ff7f50;
  color: #fff;
  border: none;
  border-radius: 5px;
}
</style>