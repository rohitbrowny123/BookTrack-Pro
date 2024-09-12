<template>
  <div class="add-books">
    <h2>Add Books to Section</h2>
    <button @click="goToMainDashboard" class="main-dashboard-button">
        Main Dashboard
      </button>
    <form @submit.prevent="addBook">
      <div class="form-group">
        <label for="name">Book Name:</label>
        <input type="text" id="name" v-model="book.name" required>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="book.description" required></textarea>
      </div>
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea id="content" v-model="book.content" required></textarea>
      </div>
      <div class="form-group">
        <label for="author">Author:</label>
        <input type="text" id="author" v-model="book.author" required>
      </div>
      <div class="form-group">
        <label for="status">Status:</label>
        <select id="status" v-model="book.status">
          <option value="available">Available</option>
          <option value="unavailable">Unavailable</option>
        </select>
      </div>
      <button type="submit" :disabled="isSubmitting">{{ isSubmitting ? 'Adding Book...' : 'Add Book' }}</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddBooksLi',
  data() {
    return {
      book: {
        name: '',
        description: '',
        content: '',
        author: '',
        status: 'available',
        section_id: null
      },
      isSubmitting: false
    };
  },
  
  created() {
    this.book.section_id = this.$route.params.sectionId;
  },
  methods: {
    goToMainDashboard() {
      this.$router.push({ name: 'LibrarianDashboard', params: { username: 'your-username' } });
    },
    async addBook() {
      this.isSubmitting = true;
      try {
        const response = await axios.post('http://localhost:5000/api/books', this.book);
        console.log('Book added successfully:', response.data);
        alert('Book added successfully!');
        this.$router.push({ name: 'LibrarianDashboard', params: { username: 'librarian' } });
      } catch (error) {
        console.error('Error adding book:', error);
        if (error.response) {
          alert(`Error adding book: ${error.response.data.error || 'Please try again.'}`);
        } else if (error.request) {
          alert('Error adding book: No response received from server. Please try again.');
        } else {
          alert(`Error adding book: ${error.message}`);
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>


<style scoped>

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

.add-books {
  background-color: #EDE8F5;
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, textarea, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background-color: #7091E6;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #5A7DD1;
}
</style>