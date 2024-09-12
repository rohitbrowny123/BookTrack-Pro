<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const name = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const userType = ref('User');
const errorMessage = ref('');
const successMessage = ref('');
const passwordMatch = ref(true);
const passwordStrength = ref('');

// Password strength checker function
const checkPasswordStrength = (password) => {
  if (password.length === 0) {
    return '';
  }
  if (password.length < 6) {
    return 'weak';
  }
  if (password.length >= 6 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
    return 'strong';
  }
  return 'medium';
};

const router = useRouter();

const validateForm = () => {
  if (!name.value || !email.value || !password.value || !confirmPassword.value || !userType.value) {
    errorMessage.value = 'All fields are required.';
    successMessage.value = '';
    return false;
  }
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.';
    successMessage.value = '';
    return false;
  }
  return true;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  try {
    const response = await axios.post('http://localhost:5000/api/users', {
      username: name.value,
      email: email.value,
      password: password.value,
      userType: userType.value,
    });

    if (response.status === 201) {
      successMessage.value = 'Registration successful!';
      errorMessage.value = '';
      
      resetForm();
      if (response.data.redirect === 'LibrarianDashboard') {
        router.push(`/librarian-dashboard/${response.data.username}`);
      } else {
        router.push(`/user-dashboard/${response.data.username}`);
      }
    } else {
      errorMessage.value = 'Registration failed. Please try again.';
      successMessage.value = '';
    }
  } catch (error) {
    errorMessage.value = 'An error occurred. Please try again later.';
    successMessage.value = '';
    console.error('Registration error:', error);
  }
};

const resetForm = () => {
  name.value = '';
  email.value = '';
  password.value = '';
  confirmPassword.value = '';
  userType.value = 'User';
};

// Watchers for live validation
watch(password, (newPassword) => {
  passwordStrength.value = checkPasswordStrength(newPassword);
  passwordMatch.value = newPassword === confirmPassword.value;
});

watch(confirmPassword, (newConfirmPassword) => {
  passwordMatch.value = newConfirmPassword === password.value;
});
</script>

<template>
  <div class="container">
    <div class="form_area">
      <p class="title">REGISTER</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <form @submit.prevent="handleSubmit">
        <div class="form_group">
          <label class="sub_title" for="name">Name</label>
          <input v-model="name" placeholder="Enter your full name" class="form_style" type="text">
        </div>
        <div class="form_group">
          <label class="sub_title" for="email">Email</label>
          <input v-model="email" placeholder="Enter your email" class="form_style" type="email">
        </div>
        <div class="form_group">
          <label class="sub_title" for="password">Password</label>
          <input v-model="password" placeholder="Enter your password" id="password" class="form_style" type="password">
          <div v-if="passwordStrength" :class="`strength-bar ${passwordStrength}`"></div>
        </div>
        <div class="form_group">
          <label class="sub_title" for="confirmPassword">Confirm Password</label>
          <input v-model="confirmPassword" placeholder="Confirm your password" id="confirmPassword" class="form_style" type="password">
          <p v-if="!passwordMatch" class="match-error">Passwords do not match</p>
        </div>
        <div class="form_group">
          <label class="sub_title" for="userType">User Type</label>
          <select v-model="userType">
            <option value="User">User</option>
            <option value="Librarian">Librarian</option>
          </select>
        </div>
        <button class="form_button" type="submit">Register</button>
      </form>
    </div>
  </div>
</template>

<style>
/* Container styling */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
}

/* Form area styling */
.form_area {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  max-width: 500px;
  width: 100%;
}

/* Title styling */
.title {
  font-size: 2em;
  color: #333;
  margin-bottom: 20px;
}

/* Form group styling */
.form_group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
  width: 100%;
}

/* Label styling */
.sub_title {
  font-size: 0.9em;
  color: #555;
  margin-bottom: 5px;
  text-align: left;
}

/* Input styling */
.form_style {
  outline: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 1em;
  width: 100%;
  box-sizing: border-box;
}

/* Select styling */
select {
  outline: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  font-size: 1em;
  width: 100%;
  box-sizing: border-box;
}

/* Button styling */
.form_button {
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.form_button:hover {
  background-color: #45a049;
}

/* Error and success messages */
.error-message {
  color: #ff4d4d;
  font-weight: bold;
  margin-bottom: 10px;
}

.success-message {
  color: #4caf50;
  font-weight: bold;
  margin-bottom: 10px;
}

/* Password strength bar */
.strength-bar {
  height: 5px;
  border-radius: 4px;
  margin-top: 5px;
  width: 100%;
  background-color: #e0e0e0;
}

.strength-bar.weak {
  background-color: #ff4d4d;
}

.strength-bar.medium {
  background-color: #ffcc00;
}

.strength-bar.strong {
  background-color: #4caf50;
}

/* Password match error */
.match-error {
  color: #ff4d4d;
  font-size: 0.9em;
  margin-top: 5px;
}
</style>
