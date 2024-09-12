<template>
  <div class="delete-section">
    <h2>Delete Section</h2>
    <p>Are you sure you want to delete this section? This action cannot be undone.</p>
    <div class="section-info" v-if="section">
      <h3>{{ section.title }}</h3>
      <p>{{ section.description }}</p>
    </div>
    <div class="actions">
      <button @click="confirmDelete" class="delete" :disabled="isDeleting">
        {{ isDeleting ? 'Deleting...' : 'Delete' }}
      </button>
      <button @click="cancel" class="cancel" :disabled="isDeleting">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeleteSection',
  data() {
    return {
      section: null,
      isDeleting: false,
    };
  },
  async mounted() {
    const sectionId = this.$route.params.sectionId;
    try {
      const response = await axios.get(`http://localhost:5000/api/sections/${sectionId}`);
      this.section = response.data;
    } catch (error) {
      console.error('Error fetching section:', error);
      // Handle error (e.g., show error message to user)
    }
  },
  methods: {
    async confirmDelete() {
      this.isDeleting = true;
      const sectionId = this.$route.params.sectionId;
      try {
        await axios.delete(`http://localhost:5000/api/sections/${sectionId}`);
        console.log('Section deleted successfully');
        this.$router.push({ 
          name: 'LibrarianDashboard', 
          params: { username: this.$route.params.username } 
        });
      } catch (error) {
        console.error('Error deleting section:', error);
        // Handle error (e.g., show error message to user)
      } finally {
        this.isDeleting = false;
      }
    },
    cancel() {
  const username = 'someUsername'; // Get this from your component data or Vuex store
  this.$router.push({ name: 'LibrarianDashboard', params: { username: username } });
},
  },
};
</script>
  
  <style scoped>
  .delete-section {
    background-color: #EDE8F5;
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    
  }
  
  .section-info {
    background-color: #ADBBDA;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    
  }
  
  .actions {
    display: flex;
    justify-content: space-between;
  }
  
  button {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .delete {
    background-color: #E67070;
    color: white;
  }
  
  .delete:hover {
    background-color: #D15A5A;
  }
  
  .cancel {
    background-color: #7091E6;
    color: white;
  }
  
  .cancel:hover {
    background-color: #5A7DD1;
  }
  </style>