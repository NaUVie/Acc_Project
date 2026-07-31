import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './style.css';
import { useCourseStore } from './stores/courses';

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

// Pre-fetch catalogs and sync cart/profile dynamically
const courseStore = useCourseStore();
courseStore.fetchCourses();
courseStore.fetchBlogs();
if (courseStore.token) {
  courseStore.fetchUserMe();
  courseStore.fetchCart();
}

app.mount('#app');

