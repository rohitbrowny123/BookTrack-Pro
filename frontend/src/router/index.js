import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import RegisterView from '@/views/RegisterView.vue';

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/user-dashboard/:username',
      name: 'UserDashboard',
      component: () => import('@/views/UserDashboardView.vue')
    },
    {
      path: '/librarian-dashboard/:username',
      name: 'LibrarianDashboard',
      component: () => import('@/views/LibrarianDashboardView.vue')
    },
    {
      path: '/add-section/:username',
      name: 'AddNewSection',
      component: () => import('@/views/AddNewSection.vue')
    },
    {
      path: '/add-books/:sectionId',
      name: 'AddBooks',
      component: () => import('@/views/AddBooksLi.vue')
    },
    {
      path: '/update-section/:sectionId',
      name: 'UpdateSection',
      component: () => import('@/views/UpdateSection.vue')
    },
    {
      path: '/delete-section/:sectionId',
      name: 'DeleteSection',
      component: () => import('@/views/DeleteSection.vue')
    },
    {
      path: '/section-books/:sectionId',
      name: 'SectionBooks',
      component: () => import('@/views/SectionBooks.vue')
    },
    {
      path: '/librarian/stats',
      name: 'LiStat',
      component: () => import('@/views/LiStat.vue')
    },
    {
      path: '/my-books',
      name: 'UserMyBooks',
      component: () => import('@/views/UserMyBooks.vue')
    },
    {
      path: '/user/:username/stats',
      name: 'UserStats',
      component: () => import('@/views/UserStatPart.vue')
    },
    {
      path: '/requests',
      name: 'Requests',
      component: () => import('@/views/LiUserRequest.vue')
    },
    {
      path: '/rate',  
      name: 'RateBooks',
      component: () => import('@/views/RateBooks.vue')
    },
  ]
});

router.beforeEach((to, from, next) => {
  if (to.name === 'LibrarianDashboard') {
    console.log('Entering LibrarianDashboard');
  }
  next();
});

export default router;