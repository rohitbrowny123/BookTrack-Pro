<template>
  <div class="li-user-request">
    <header class="request-header">
      <h1 class="header-title">Book Requests</h1>
      <button @click="goToMainDashboard" class="main-dashboard-button">
        Main Dashboard
      </button>
    </header>
    <main>
      <div v-if="requests.length">
        <table class="table-style">
          <thead>
            <tr>
              <th>Book Name</th>
              <th>Requested By</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.book.name }}</td>
              <td>{{ request.user.username }}</td>
              <td>{{ request.status }}</td>
              <td>
                <button 
                  class="custom-button" 
                  @click="updateRequestStatus(request, 'granted')"
                  :disabled="request.status !== 'pending'"
                >
                  Grant
                </button>
                <button 
                  class="custom-button reject-button" 
                  @click="updateRequestStatus(request, 'rejected')"
                  :disabled="request.status !== 'pending'"
                >
                  Reject
                </button>
                <button 
                  class="custom-button user-button" 
                  @click="showUserDetails(request.user.id)"
                >
                  User
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No pending requests.</p>
      </div>
    </main>

    <!-- User Details Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>User Details</h2>
        <div v-if="selectedUser">
          <p><strong>Username:</strong> {{ selectedUser.username }}</p>
          <p><strong>Email:</strong> {{ selectedUser.email }}</p>
          <h3>Book Requests:</h3>
          <div v-if="selectedUser.requests.length">
            <div v-for="request in selectedUser.requests" :key="request.id" class="request-item">
              <p><strong>Book Title:</strong> {{ request.book_title }}</p>
              <p><strong>Section Title:</strong> {{ request.section_title }}</p>
              <p><strong>Created At:</strong> {{ formatDate(request.created_at) }}</p>
              <p><strong>Days Requested:</strong> {{ request.days_requested }}</p>
              <p><strong>Status:</strong> {{ request.status }}</p>
              <button @click="removeRequest(request.id)" class="custom-button remove-button">Remove Request</button>
            </div>
          </div>
          <p v-else>No book requests found.</p>
        </div>
        <button @click="closeModal" class="custom-button close-button">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      requests: [],
      showModal: false,
      selectedUser: null,
    };
  },
  methods: {
    goToMainDashboard() {
      this.$router.push({ name: 'LibrarianDashboard', params: { username: 'your-username' } });
    },
    fetchRequests() {
      const userId = this.$route.params.userId;
      this.$router.push({ name: 'Requests', params: { userId: userId } });

      axios.get('/api/book-requests', { params: { user_id: userId } })
        .then(response => {
          console.log('Fetched requests:', response.data);
          this.requests = response.data;
        })
        .catch(error => {
          console.error("Error fetching requests:", error);
        });
    },
    updateRequestStatus(request, status) {
      console.log('Updating request:', request, 'to status:', status);
      axios.patch(`/api/book-requested/${request.id}`, { status })
        .then(() => {
          console.log('Request status updated successfully');
          request.status = status;
        })
        .catch(error => {
          console.error("Error updating request status:", error);
        });
    },
    showUserDetails(userId) {
      axios.get(`/api/users/${userId}`)
        .then(response => {
          this.selectedUser = response.data;
          this.showModal = true;
        })
        .catch(error => {
          console.error("Error fetching user details:", error);
        });
    },
    closeModal() {
      this.showModal = false;
      this.selectedUser = null;
    },
    formatDate(date) {
      if (!date) return '';
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    removeRequest(requestId) {
      axios.delete(`/api/book-requests/${requestId}`)
        .then(() => {
          // Remove the request from the local data
          this.selectedUser.requests = this.selectedUser.requests.filter(req => req.id !== requestId);
          // Update the main requests list
          this.fetchRequests();
        })
        .catch(error => {
          console.error("Error removing request:", error);
        });
    }
  },
  mounted() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
.li-user-request {
  padding: 20px;
  background-color: #f0f0f0;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-title {
  font-size: 24px;
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
}

.main-dashboard-button:hover {
  background-color: #5671b5;
}

.table-style {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.table-style th, .table-style td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.table-style th {
  background-color: #607d8b;
  color: #fff;
}

.table-style tbody tr:nth-child(even) {
  background-color: #f5f5f5;
}

.table-style tbody tr:hover {
  background-color: #e0e7ff;
}

.custom-button {
  padding: 8px 16px;
  margin-right: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.custom-button:hover {
  background-color: #0056b3;
}

.custom-button:disabled {
  background-color: #b0b0b0;
  cursor: not-allowed;
}

.reject-button {
  background-color: #f44336;
}

.reject-button:hover {
  background-color: #d32f2f;
}

.user-button {
  background-color: #4CAF50;
}

.user-button:hover {
  background-color: #45a049;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  border-radius: 5px;
}

.request-item {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.remove-button {
  background-color: #f44336;
  color: white;
  margin-top: 10px;
}

.remove-button:hover {
  background-color: #d32f2f;
}

.close-button {
  background-color: #6c757d;
  color: white;
  margin-top: 20px;
}

.close-button:hover {
  background-color: #5a6268;
}
</style>