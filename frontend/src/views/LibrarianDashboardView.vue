<template>
  <div class="librarian-dashboard">
    <header class="header">
      <h1>Librarian's Dashboard</h1>
      <div class="header-actions">
        <div class="buttons">
          <button @click="goToRequests">Requests</button>
          <button @click="goToStats">Stats</button>
          <button @click="logout">Logout</button>
        </div>
        <div class="search-bar">
          <input 
          type="text" 
          placeholder="Search users or sections..." 
          v-model="searchQuery" 
          @keyup.enter="performSearch" 
          />
          <button @click="performSearch">Search</button>
        </div>
      </div>
    </header>
    <main class="content">
      <p class="welcome-message">Welcome {{ username }}</p>
      <h2>All Users</h2>
      <div v-if="loading">Loading users...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      <div v-else-if="filteredUsers.length" class="user-list">
        <div v-for="user in filteredUsers" :key="user.id" class="user-card">
  <h3>{{ user.username }}</h3>
  <p>Role: {{ user.roles.length ? user.roles[0].name : 'No role assigned' }}</p>
  <p>Email: {{ user.email }}</p>
  <div class="user-actions">
    <button @click="removeUser(user.id)" class="remove-button">Remove</button>
    <button @click="toggleBlacklist(user.id)" :class="['blacklist-button', { 'whitelist': user.is_blacklisted }]">
      {{ user.is_blacklisted ? 'Whitelist' : 'Blacklist' }}
    </button>
  </div>
</div>
      </div>
      <div class="section-header">
        <h2>Sections</h2>
        <button @click="goToAddSection" class="add-section-button">Add Section</button>
      </div>
      <div class="sections-container">
        <div v-if="sectionsLoading">Loading sections...</div>
        <div v-else-if="sectionsError" class="error-message">{{ sectionsError }}</div>
        <div v-else-if="filteredSections.length === 0">No sections available.</div>
        <div v-else v-for="section in filteredSections" :key="section.id" class="section-box" :style="{ backgroundImage: `url(${section.image || 'default-image-url.jpg'})` }">
          <div class="section-content">
            <h3>{{ section.title }}</h3>
            <p><strong>Date Created:</strong> {{ formatDate(section.date_created) }}</p>
            <p class="section-description">{{ section.description }}</p>
            <div class="section-actions">
              <button @click="viewBooks(section.id)" class="action-button">Books</button>
              <button @click="addBooks(section.id)" class="action-button">Add Books</button>
              <button @click="updateSection(section.id)" class="action-button">Update</button>
              <button @click="deleteSection(section.id)" class="action-button delete">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'LibrarianDashboardView',
  data() {
    return {
      username: '',
      searchQuery: '',
      users: [],
      loading: true,
      error: null,
      sections: [],
      sectionsLoading: true,
      sectionsError: null,
      searchResults: {
        users: [],
        sections: []
      }
    };
  },
  computed: {
    filteredUsers() {
    if (!this.searchQuery) {
      return this.users;
    }
    return this.searchResults.users;
  },
  filteredSections() {
    if (!this.searchQuery) {
      return this.sections;
    }
    return this.searchResults.sections;
  },
},
  methods: {
    removeUser(userId) {
    if (confirm('Are you sure you want to remove this user?')) {
      fetch(`http://localhost:5000/api/users/${userId}`, {
        method: 'DELETE',
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
          this.users = this.users.filter(user => user.id !== userId);
          alert('User removed successfully');
        } else {
          alert(data.message || 'Failed to remove user');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while removing the user');
      });
    }
  },

  toggleBlacklist(userId) {
    fetch(`http://localhost:5000/api/users/${userId}/toggle-blacklist`, {
      method: 'POST',
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.success) {
        const user = this.users.find(u => u.id === userId);
        if (user) {
          user.is_blacklisted = !user.is_blacklisted;
        }
        alert(data.message);
      } else {
        alert(data.message || 'Failed to update blacklist status');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while updating blacklist status');
    });
  },
    
    goToStats() {
      this.$router.push({ name: 'LiStat' });
    },
    goToRequests() {
      this.$router.push({ name: 'Requests' }); // Navigation to Requests page
    },
    addBooks(sectionId) {
      this.$router.push({ name: 'AddBooks', params: { sectionId: sectionId } });
    },
    viewBooks(sectionId) {
      this.$router.push({ name: 'SectionBooks', params: { sectionId: sectionId } });
    },
    updateSection(sectionId) {
      this.$router.push({ name: 'UpdateSection', params: { sectionId: sectionId } });
    },
    deleteSection(sectionId) {
      this.$router.push({ name: 'DeleteSection', params: { sectionId: sectionId } });
    },
    goToBooks() {
      this.$router.push({ name: 'Books' });
    },
    logout() {
      // Implement logout logic here
      this.$router.push({ name: 'Login' });
    },
    performSearch() {
    const query = this.searchQuery.toLowerCase();
    this.searchResults.users = this.users.filter(user => 
      user.username.toLowerCase().includes(query)
    );
    this.searchResults.sections = this.sections.filter(section => 
      section.title.toLowerCase().includes(query)
    );
    },
    fetchUsers() {
      this.loading = true;
      this.error = null;
      fetch('http://localhost:5000/api/users')
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log('Fetched users:', data);
          this.users = data;
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching users:', error);
          this.error = `Failed to load users: ${error.message}`;
          this.loading = false;
        });
    },
    goToAddSection() {
      this.$router.push({ name: 'AddNewSection', params: { username: this.username } });
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    fetchSections() {
  this.sectionsLoading = true;
  this.sectionsError = null;
  fetch('http://localhost:5000/api/sections')
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error('Error response:', data);
        throw new Error(data.message || data.error);
      }
      console.log('Fetched sections:', data);
      this.sections = data;
      this.sectionsLoading = false;
    })
    .catch(error => {
      console.error('Error fetching sections:', error);
      this.sectionsError = `Failed to load sections: ${error.message}`;
      this.sectionsLoading = false;
    });
}
  },
  watch: {
    searchQuery() {
      this.performSearch();
    }
  },
  mounted() {
    console.log('LibrarianDashboardView mounted');
    this.username = this.$route.params.username || 'Librarian';
    this.fetchUsers();
    this.fetchSections();
  },
};
</script>


<style scoped>
.user-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.remove-button, .blacklist-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s;
}

.remove-button {
  background-color: #ff4d4d;
  color: white;
}

.remove-button:hover {
  background-color: #ff3333;
  transform: scale(1.05);
}

.blacklist-button {
  background-color: #4d4dff;
  color: white;
}

.blacklist-button:hover {
  background-color: #3333ff;
  transform: scale(1.05);
}

.blacklist-button.whitelist {
  background-color: #4dff4d;
  color: black;
}

.blacklist-button.whitelist:hover {
  background-color: #33ff33;
}
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

.welcome-message {
  font-size: 34px;
  margin: 0 20px;
  color: #3d52a0;
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

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 20px;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  flex: 1;
  border: 2px solid #7091E6;
  border-radius: 20px;
  background-color: #7091E6;
  color: black;
}

.search-bar button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #7091E6;
  color: black;
  border: none;
  border-radius: 20px;
}

.user-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.user-card {
  background-color: white;
  border: 2px solid #7091E6;
  border-radius: 20px;
  padding: 20px;
  flex: 1 1 calc(33.333% - 40px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.user-card h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  color: #333;
}

.user-card p {
  margin: 5px 0;
  color: #666;
}

.error-message {
  color: red;
  font-weight: bold;
}

.sections-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px 0;
}
.section-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.4rem;
}

.section-content p {
  margin: 5px 0;
  font-size: 0.9rem;
}

.section-description {
  max-height: 60px;          /* Adjust as needed */
  overflow: hidden;
  text-overflow: ellipsis;
  display: flex;
  flex-direction: column;
  line-clamp: 3;
  box-orient: vertical;
  line-height: 20px;         /* Adjust according to your line height */
  height: calc(3 * 20px);    /* number of lines * line height */
}


.section-box {
  flex: 1 1 calc(33.333% - 20px);
  min-width: 300px;
  height: 250px;
  border-radius: 15px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-size: cover;
  background-position: center;
}

.section-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.section-content {
  position: absolute;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 0 10px;
}

.add-section-button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #7091E6;
  color: black;
  border: none;
  border-radius: 20px;
}

.add-section-button:hover {
  background-color: #6589e5;
}
.section-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.action-button {
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
  background-color: #50c569;
  color: white;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}
</style>
