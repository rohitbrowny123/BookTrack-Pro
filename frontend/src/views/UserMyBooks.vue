<template>
  <div class="my-books-container">
    <h1 class="title">My Books</h1>
    <button @click="goToMainDashboard" class="main-dashboard-button">
      Main Dashboard
    </button>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="search-bar-container">
        <div class="search-bar">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search by book name or author..."
            @input="filterBooks"
          />
          <button @click="filterBooks">Search</button>
        </div>
      </div>

      <div v-for="book in filteredBooks" :key="book.id" class="book-card">
        <div class="book-info">
          <h2 class="book-title">{{ book.name }}</h2>
          <p class="book-author">Author: {{ book.author }}</p>
          <p class="book-status">Status: {{ book.status }}</p>
          <p class="book-section">Section: {{ book.section }}</p>
        </div>
        <div class="book-actions">
          <button @click="returnBook(book)" class="return-button">Return</button>
          <button @click="viewBook(book)" class="view-button">View</button>
          <div class="rating">
            <span v-for="star in 5" :key="star" @click="rateBook(book.id, star)">
              <i class="fas fa-star" :class="{'filled': star <= (book.rating || 0)}"></i>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedBook" class="modal">
      <div class="modal-content">
        <h2>{{ selectedBook.name }}</h2>
        <p><strong>Author:</strong> {{ selectedBook.author }}</p>
        <p><strong>Status:</strong> {{ selectedBook.status }}</p>
        <p><strong>Section:</strong> {{ selectedBook.section }}</p>
        <p><strong>Description:</strong> {{ selectedBook.description }}</p>
        <p><strong>Content Preview:</strong> {{ getContentPreview(selectedBook.content) }}</p>
        <div class="modal-buttons">
          <button @click="downloadBook(selectedBook)" class="download-button">Download</button>
          <button @click="closeModal" class="cancel-button">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: [],
      filteredBooks: [],
      searchQuery: '',
      loading: true,
      error: null,
      selectedBook: null,
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

      axios.get(`http://localhost:5000/api/user-books?user_id=${userId}`)
        .then(response => {
          this.books = response.data;
          this.filteredBooks = this.books;
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
          this.error = 'Failed to fetch books. Please try again.';
          this.loading = false;
        });
    },
    viewBook(book) {
      this.selectedBook = book;
    },
    downloadBook(book) {
      axios.get(`http://localhost:5000/api/download-book/${book.id}`, {
        responseType: 'blob',
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${book.name}.pdf`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        this.closeModal();
      })
      .catch(error => {
        console.error('Error downloading book:', error);
        alert('Failed to download book. Please try again.');
      });
    },
    closeModal() {
      this.selectedBook = null;
    },
    rateBook(bookId, rating) {
    const userId = localStorage.getItem('userId');
    axios.post('http://localhost:5000/api/rate-book', {
      user_id: parseInt(userId),
      book_id: bookId,
      rating: rating
    })
    .then(response => {
      console.log(response.data.message);
      // Update the local rating
      const bookIndex = this.filteredBooks.findIndex(b => b.id === bookId);
      if (bookIndex !== -1) {
        this.$set(this.filteredBooks[bookIndex], 'rating', rating);
      }
    })
    .catch(error => {
      console.error('Error rating book:', error);
      alert('Failed to rate book. Please try again.');
    });
  },
    returnBook(book) {
      const userId = localStorage.getItem('userId');
      axios.post(`http://localhost:5000/api/return-book`, {
        user_id: userId,
        book_id: book.id,
      })
      .then(() => {
        this.fetchBooks();
      })
      .catch(error => {
        console.error('Error returning book:', error);
        alert('Failed to return book. Please try again.');
      });
    },
    filterBooks() {
      const query = this.searchQuery.toLowerCase();
      this.filteredBooks = this.books.filter(book => 
        book.name.toLowerCase().includes(query) || 
        book.author.toLowerCase().includes(query)
      );
    },
    getContentPreview(content) {
      return content ? content.substring(0, 100) + '...' : 'No content available';
    },
  },
};
</script>


<style scoped>

.rating {
  display: flex;
  align-items: center;
}

.rating span {
  cursor: pointer;
  font-size: 1.5rem;
  color: #ccc;
  transition: color 0.2s;
}

.rating span:hover,
.rating span:hover ~ span {
  color: #ffd700;
}

.rating .filled {
  color: #ffd700;
}
.my-books-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background-color: #F5F5FA;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
}

.main-dashboard-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #7091E6;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: block;
  margin: 0 auto 30px;
  transition: background-color 0.3s ease;
}

.main-dashboard-button:hover {
  background-color: #5671b5;
}

.search-bar-container {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.search-bar input {
  width: 60%;
  padding: 12px 15px;
  border: 2px solid #7091E6;
  border-radius: 20px;
  font-size: 16px;
  background-color: #fff;
  color: #333;
  transition: border-color 0.3s ease;
}

.search-bar input:focus {
  border-color: #5671b5;
  outline: none;
}

.search-bar button {
  padding: 12px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #7091E6;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-bar button:hover {
  background-color: #5671b5;
}

.book-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: box-shadow 0.3s ease;
}

.book-card:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.book-info {
  flex-grow: 1;
}

.book-title {
  font-size: 1.6rem;
  color: #2c3e50;
  margin-bottom: 8px;
  font-weight: bold;
}

.book-author, .book-status {
  color: #34495e;
  margin-bottom: 5px;
  font-size: 1rem;
}

.book-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.view-button, .return-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: bold;
}

.view-button {
  background-color: #3498db;
  color: white;
}

.view-button:hover {
  background-color: #2980b9;
}

.return-button {
  background-color: #e74c3c;
  color: white;
}

.return-button:hover {
  background-color: #c0392b;
}

.rating {
  display: flex;
  align-items: center;
  gap: 5px;
}

.rating i {
  color: #ccc;
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.rating i.filled {
  color: #f1c40f;
}

.rating i:hover,
.rating i:hover ~ i {
  color: #f39c12;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.download-button,
.cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: bold;
}

.download-button {
  background-color: #2ecc71;
  color: white;
}

.download-button:hover {
  background-color: #27ae60;
}

.cancel-button {
  background-color: #e74c3c;
  color: white;
}

.cancel-button:hover {
  background-color: #c0392b;
}

.loading,
.error {
  text-align: center;
  font-size: 1.2rem;
  color: #e74c3c;
}
.rating {
  display: flex;
  align-items: center;
}

.rating span {
  cursor: pointer;
  font-size: 1.5rem;
  color: #ccc;
  transition: color 0.2s;
}

.rating span:hover,
.rating span:hover ~ span {
  color: #ffd700;
}

.rating .filled {
  color: #ffd700;
}
</style>