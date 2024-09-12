<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const router = useRouter();

const login = async () => {
  try {
    const response = await axios.post('http://localhost:5000/login', {
      username: username.value, 
      password: password.value,
    });

    if (response.status === 200) {
      localStorage.setItem('userId', response.data.user_id);
      localStorage.setItem('username', response.data.username);
      successMessage.value = 'Login successful!';
      errorMessage.value = '';

      const { role, username: loggedInUsername } = response.data;
      
      const route = role === 'Librarian' 
        ? `/librarian-dashboard/${loggedInUsername}` 
        : `/user-dashboard/${loggedInUsername}`;
      router.push(route);

      resetForm();
    } else {
      errorMessage.value = response.data.message || 'Login failed. Please try again.';
      successMessage.value = '';
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'An error occurred. Please try again later.';
    successMessage.value = '';
    console.error('Login error:', error);
  }
};

const resetForm = () => {
  username.value = '';
  password.value = '';
};
</script>

<template>
  <div class="container">
    <div class="form_area">
      <p class="title">Login</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <form @submit.prevent="login">
        <div class="form_group">
          <label class="sub_title" for="username">Username</label>
          <input v-model="username" placeholder="Enter your Username" class="form_style" type="text">
        </div>
        <div class="form_group">
          <label class="sub_title" for="password">Password</label>
          <input v-model="password" placeholder="Enter your password" id="password" class="form_style" type="password">
        </div>
        <div>
          <button class="btn" type="submit">Login</button>
          <p>Don't have an Account? <router-link to="/register">Register Here!</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
}

.form_area {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: #f5f5f5;
  height: auto;
  width: auto;
  border: 2px solid #333;
  border-radius: 20px;
  box-shadow: 3px 4px 0px 1px #ccc;
}

.title {
  color: #333;
  font-weight: 900;
  font-size: 1.5em;
  margin-top: 20px;
}

.sub_title {
  font-weight: 600;
  margin: 5px 0;
  color: #555;
}

.form_group {
  display: flex;
  flex-direction: column;
  align-items: baseline;
  margin: 10px;
}

.form_style {
  outline: none;
  border: 2px solid #333;
  box-shadow: 3px 4px 0px 1px #ccc;
  width: 290px;
  padding: 12px 10px;
  border-radius: 4px;
  font-size: 15px;
}

.form_style:focus,
.btn:focus {
  transform: translateY(4px);
  box-shadow: 1px 2px 0px 0px #ccc;
}

.btn {
  padding: 15px;
  margin: 25px 0px;
  width: 290px;
  font-size: 15px;
  background: #4caf50;
  color: #fff;
  border-radius: 10px;
  font-weight: 800;
  box-shadow: 3px 3px 0px 0px #ccc;
}

.btn:hover {
  opacity: 0.9;
}

.link {
  font-weight: 800;
  color: #333;
  padding: 5px;
}

.error-message {
  color: #ff0000;
  font-weight: bold;
}

.success-message {
  color: #4caf50;
  font-weight: bold;
}
</style>
