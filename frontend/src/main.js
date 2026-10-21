import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './style.css';
import { useCourseStore } from './stores/courses';
import { useTestimonialStore } from './stores/testimonials';

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

// Global stores initialization
const courseStore = useCourseStore();
const testimonialStore = useTestimonialStore();

// Sync user data dynamically only if authenticated
if (courseStore.token) {
  Promise.all([
    courseStore.fetchUserMe(),
    courseStore.fetchCart(),
    courseStore.fetchOrders(),
    courseStore.fetchReferrals()
  ]).catch(err => console.error("Error pre-fetching user data:", err));
}

app.mount('#app');

