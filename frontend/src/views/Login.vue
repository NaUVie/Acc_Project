<template>
  <div class="login-view container">
    <div class="auth-wrapper">
      <div class="auth-card glass-card">
        <div class="auth-tabs">
          <button class="tab-btn active">Đăng nhập</button>
          <router-link to="/register" class="tab-btn">Đăng ký</router-link>
        </div>

        <div class="form-container">
          <div class="form-header">
            <h2>Chào mừng quay trở lại</h2>
            <p>Đăng nhập để tiếp tục học tập và quản lý ưu đãi giới thiệu.</p>
          </div>
          
          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label for="login-email">Tài khoản Email</label>
              <input 
                v-model="loginData.email" 
                type="email" 
                id="login-email" 
                placeholder="name@domain.com" 
                required
              />
            </div>

            <div class="form-group">
              <label for="login-password">Mật khẩu</label>
              <input 
                v-model="loginData.password" 
                type="password" 
                id="login-password" 
                placeholder="••••••••" 
                required
              />
            </div>

            <button type="submit" class="btn btn-primary w-full" :disabled="loading">
              {{ loading ? 'Đang xác thực...' : 'Đăng nhập' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

// Import separated stylesheet
import '@/styles/auth.css';

const router = useRouter();
const courseStore = useCourseStore();

const loading = ref(false);

const loginData = ref({
  email: '',
  password: ''
});

onMounted(() => {
  // If user is already logged in, redirect to dashboard
  if (courseStore.token) {
    router.push('/dashboard');
  }
});

const handleLogin = async () => {
  loading.value = true;
  try {
    await courseStore.login(loginData.value.email, loginData.value.password);
    alert('Đăng nhập thành công! Chào mừng quay trở lại hệ thống học tập.');
    router.push('/dashboard');
  } catch (err) {
    alert('Đăng nhập thất bại: ' + err.message);
  } finally {
    loading.value = false;
  }
};
</script>
