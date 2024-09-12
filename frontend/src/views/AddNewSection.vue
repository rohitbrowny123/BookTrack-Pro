<template>
  <div class="librarian-dashboard">
    <header class="header">
      <h1>Librarian's Dashboard</h1>
      <div class="header-actions">
        <div class="buttons">
          <button @click="goToStats">Stats</button>
          <button @click="goToBooks">Books</button>
          <button @click="logout">Logout</button>
        </div>
      </div>
    </header>
    <div class="content">
      <h2>Add New Section</h2>
      <div class="add-section-container">
        <form @submit.prevent="addSection" class="section-form">
          <div class="form-group">
            <label for="title">Title:</label>
            <input type="text" id="title" v-model="newSection.title" required>
          </div>
          <div class="form-group">
            <label for="dateCreated">Date Created:</label>
            <input type="date" id="dateCreated" v-model="newSection.dateCreated" required>
          </div>
          <div class="form-group">
            <label for="image">Image (optional):</label>
            <input type="file" id="image" @change="handleImageUpload" accept="image/*">
          </div>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" v-model="newSection.description" required></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-add">Add</button>
            <button type="button" class="btn-cancel" @click="cancel">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      newSection: {
        title: '',
        dateCreated: '',
        image: null,
        description: ''
      }
    };
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.newSection.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async addSection() {
      try {
        const response = await axios.post('http://localhost:5000/api/sections', this.newSection);
        console.log('Section added:', response.data);
        this.$router.push({ name: 'LibrarianDashboard', params: { username: this.$route.params.username } });
      } catch (error) {
        console.error('Error adding section:', error);
        // Handle error (e.g., show an error message to the user)
      }
    },
    logout() {
      // Implement logout logic here
      this.$router.push({ name: 'Login' });
    },
    goToStats() {
      // Redirect to the stats page
      this.$router.push({ name: 'StatsPage' });
    },
    goToBooks() {
      // Redirect to the books page
      this.$router.push({ name: 'BooksPage' });
    },
    cancel() {
      const username = this.$route.params.username;
      if (username) {
        this.$router.push({ name: 'LibrarianDashboard', params: { username } });
      } else {
        console.error('Username parameter is missing!');
        // Handle the case where username is missing (e.g., redirect to a default route)
        this.$router.push({ name: 'Login' });
      }
    }
  },
  mounted() {
    // If username is not in the route params, you may want to handle it here
    const username = this.$route.params.username;
    if (username) {
      console.log('Received username:', username);
    } else {
      console.error('Username parameter is missing!');
    }
  }
};
</script>


<style scoped>
.librarian-dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #EDE8F5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #EDE8F5;
  border-bottom: 10px solid #f6f3f3;
}

.header h1 {
  font-size: 32px;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

.buttons {
  display: flex;
  gap: 0.5rem;
}

.buttons button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #7091E6;
  color: black;
  border: none;
  border-radius: 20px;
}

.buttons button:hover {
  background-color: #6589e5;
}

.content {
  flex-grow: 1;
  padding: 1rem;
}

.add-section-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px 30px;
  background-color: #EDE8F5;
  border-radius: 20px;
  border: 2px solid #7091E6;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #3d52a0;
  font-size: 34px;
}

.section-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #3d52a0;
}

input[type="text"],
input[type="date"],
textarea {
  width: 100%;
  padding: 10px;
  border: 2px solid #7091E6;
  border-radius: 20px;
  background-color: #7091E6;
  color: black;
  font-size: 16px;
}

textarea {
  height: 100px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn-add,
.btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
}

.btn-add {
  background-color: #63e163;
  color: black;
}

.btn-cancel {
  background-color: #f44336;
  color: white;
}
</style>
