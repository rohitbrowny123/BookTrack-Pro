<template>
    <div class="section-books">
      <h2>Books in Section</h2>
      <button @click="goToMainDashboard" class="main-dashboard-button">
        Main Dashboard
      </button>
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search books by name, author, or status"
          @input="filterBooks"
        />
      </div>
      <div class="books-container">
        <div v-for="book in filteredBooks" :key="book.id" class="book-box">
          <h3>{{ book.name }}</h3>
          <p><strong>Author:</strong> {{ book.author }}</p>
          <p><strong>Status:</strong> {{ book.status }}</p>
          <p class="book-description">{{ book.description }}</p>
          <button @click="deleteBook(book.id)" class="delete-book-button">
          Delete Book
        </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SectionBooks',
    data() {
      return {
        books: [],
        filteredBooks: [],
        searchQuery: '',
        sectionId: this.$route.params.sectionId,
      };
    },
    mounted() {
      this.fetchBooks();
    },
    methods: {
      async fetchBooks() {
        try {
          const response = await axios.get(`http://localhost:5000/api/sections/${this.sectionId}/books`);
          this.books = response.data;
          this.filteredBooks = this.books;
        } catch (error) {
          console.error('Error fetching books:', error);
        }
      },
      filterBooks() {
        const query = this.searchQuery.toLowerCase();
        this.filteredBooks = this.books.filter(book => 
          book.name.toLowerCase().includes(query) ||
          book.author.toLowerCase().includes(query) ||
          book.status.toLowerCase().includes(query)
        );
      },
      goToMainDashboard() {
      this.$router.push({ name: 'LibrarianDashboard', params: { username: 'your-username' } });
    },
    async deleteBook(bookId) {
  try {
    const response = await axios.delete(`http://localhost:5000/api/books/${bookId}`);
    if (response.status === 200) {
      this.books = this.books.filter(book => book.id !== bookId);
      this.filteredBooks = this.filteredBooks.filter(book => book.id !== bookId);
      console.log('Book deleted successfully');
      // You can add a user-friendly notification here
    } else {
      console.error('Failed to delete book:', response.data.error);
      // You can add a user-friendly error message here
    }
  } catch (error) {
    console.error('Error deleting book:', error.response ? error.response.data.error : error.message);
    // You can add a user-friendly error message here
  }
}
    },
  };
  </script>
  
  <style scoped>
.delete-book-button {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.main-dashboard-button {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #7091E6;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  position: absolute; /* Position the button absolutely */
  top: 25px; /* Distance from the top */
  right: 25px; /* Distance from the right */
}

.main-dashboard-button:hover {
  background-color: #5671b5;
}


  .section-books {
    padding: 20px;
    background-color: #EDE8F5;
  }
  
  .search-bar {
    margin-bottom: 20px;
  }
  
  .search-bar input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 2px solid #7091E6;
    border-radius: 20px;
  }
  
  .books-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .book-box {
    background-color: white;
    border: 2px solid #7091E6;
    border-radius: 15px;
    padding: 15px;
    flex: 1 1 calc(33.333% - 20px);
    min-width: 250px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .book-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .book-box h3 {
    margin: 0 0 10px 0;
    font-size: 1.2rem;
    color: #333;
  }
  
  .book-box p {
    margin: 5px 0;
    color: #666;
  }
  .book-description {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #777;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  text-overflow: ellipsis;
  white-space: nowrap;
}

  </style>