import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/courses/ai',
    name: 'CourseKyNangAI',
    component: () => import('../views/courses/KyNangAI.vue')
  },
  {
    path: '/courses/mem',
    name: 'CourseKyNangMem',
    component: () => import('../views/courses/KyNangMem.vue')
  },
  {
    path: '/courses/chuyen-mon',
    name: 'CourseKyNangChuyenMon',
    component: () => import('../views/courses/KyNangChuyenMon.vue')
  },
  {
    path: '/bundles',
    name: 'Bundles',
    component: () => import('../views/Bundles.vue')
  },
  {
    path: '/corporate/dao-tao',
    name: 'CorporateDaoTao',
    component: () => import('../views/corporate/DaoTao.vue')
  },
  {
    path: '/corporate/coe',
    name: 'CorporateCoe',
    component: () => import('../views/corporate/Coe.vue')
  },
  {
    path: '/corporate/for-team',
    name: 'CorporateForTeam',
    component: () => import('../views/corporate/ForTeam.vue')
  },
  {
    path: '/corporate/case-studies',
    name: 'CorporateCaseStudies',
    component: () => import('../views/corporate/CaseStudies.vue')
  },
  {
    path: '/library/blog',
    name: 'LibraryBlog',
    component: () => import('../views/library/Blog.vue')
  },
  {
    path: '/library/recipes',
    name: 'LibraryRecipes',
    component: () => import('../views/library/Recipes.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue')
  },
  {
    path: '/about-us',
    name: 'AboutUs',
    component: () => import('../views/AboutUs.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

export default router;
