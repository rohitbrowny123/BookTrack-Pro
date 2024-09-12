import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import axios from './axios' 
// import './axios-config';

const app = createApp(App)

app.config.globalProperties.$axios = axios

app.use(router)
app.mount('#app')
