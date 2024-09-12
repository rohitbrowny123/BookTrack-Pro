<template>
    <div class="update-section">
      <h2>Update Section</h2>
      <button @click="goToMainDashboard" class="main-dashboard-button">
        Main Dashboard
      </button>
      <form @submit.prevent="updateSection">
        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model="section.title" required>
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="section.description" required></textarea>
        </div>
        <div class="form-group">
          <label for="date_created">Date Created:</label>
          <input type="date" id="date_created" v-model="section.date_created" required>
        </div>
        <div class="form-group">
          <label for="image">Image (optional):</label>
          <input type="file" id="image" @change="handleImageUpload" accept="image/*">
        </div>
        <button type="submit" :disabled="isSubmitting">{{ isSubmitting ? 'Updating Section...' : 'Update Section' }}</button>
      </form>
    </div>
  </template>
  
  <script>
import axios from 'axios';

export default {
  name: 'UpdateSection',
  data() {
    return {
      section: {
        title: '',
        description: '',
        date_created: '',
        image: null,
      },
      isSubmitting: false
    };
  },
  
  async mounted() {
    const sectionId = this.$route.params.sectionId;
    try {
      const response = await axios.get(`http://localhost:5000/api/sections/${sectionId}`);
      this.section = response.data;
      this.section.date_created = new Date(this.section.date_created).toISOString().split('T')[0];
    } catch (error) {
      console.error('Error fetching section data:', error);
      alert('Error fetching section data. Please try again.');
    }
  },
  methods: {
    goToMainDashboard() {
      this.$router.push({ name: 'LibrarianDashboard', params: { username: 'your-username' } });
    },
    handleImageUpload(event) {
      this.section.image = event.target.files[0];
    },
    async updateSection() {
      this.isSubmitting = true;
      try {
        const formData = new FormData();
        formData.append('title', this.section.title);
        formData.append('description', this.section.description);
        formData.append('date_created', this.section.date_created);
        if (this.section.image) {
          formData.append('image', this.section.image);
        }

        const response = await axios.put(
          `http://localhost:5000/api/sections/${this.$route.params.sectionId}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        console.log('Section updated successfully:', response.data);
        alert('Section updated successfully!');
        this.$router.push({ name: 'LibrarianDashboard', params: { username: 'librarian' } });
      } catch (error) {
        console.error('Error updating section:', error);
        if (error.response) {
          alert(`Error updating section: ${error.response.data.error || 'Please try again.'}`);
        } else if (error.request) {
          alert('Error updating section: No response received from server. Please try again.');
        } else {
          alert(`Error updating section: ${error.message}`);
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
  
  <style scoped>
  .update-section {
    background-color: #EDE8F5;
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
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
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input, textarea {
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