<template>
  <div class="login-view container">
    <div class="auth-wrapper">
      <div class="auth-card glass-card">
        <div class="auth-tabs">
          <router-link to="/login" class="tab-btn">Đăng nhập</router-link>
          <button class="tab-btn active">Đăng ký</button>
        </div>

        <div class="form-container">
          <div class="form-header">
            <h2>Tạo tài khoản mới</h2>
            <p>Khám phá lộ trình học tập tối ưu cùng ACC Academy</p>
          </div>

          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label for="reg-name">Họ và tên</label>
              <input 
                type="text" 
                id="reg-name" 
                v-model="registerData.fullname" 
                placeholder="Nguyễn Văn A" 
                required 
              />
            </div>
            
            <div class="form-group">
              <label for="reg-email">Email</label>
              <input 
                type="email" 
                id="reg-email" 
                v-model="registerData.email" 
                placeholder="example@gmail.com" 
                required 
              />
            </div>

            <div class="form-group">
              <label for="reg-password">Mật khẩu</label>
              <input 
                type="password" 
                id="reg-password" 
                v-model="registerData.password" 
                placeholder="••••••••" 
                required 
              />
            </div>

            <div class="form-group">
              <label for="reg-ref">Mã giới thiệu (Nếu có)</label>
              <input 
                type="text" 
                id="reg-ref" 
                v-model="registerData.referralCodeUsed" 
                placeholder="Nhập mã giới thiệu" 
              />
              <span class="input-helper" v-if="registerData.referralCodeUsed">
                Bạn sẽ được giảm giá 10% cho đơn hàng đầu tiên!
              </span>
            </div>

            <button type="submit" class="btn btn-primary w-full mt-4" :disabled="loading">
              {{ loading ? 'Đang tạo tài khoản...' : 'Đăng ký ngay' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

// Import separated stylesheet
import '@/styles/auth.css';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const loading = ref(false);

const registerData = ref({
  fullname: '',
  email: '',
  password: '',
  referralCodeUsed: ''
});

onMounted(() => {
  // If user is already logged in, redirect to dashboard
  if (courseStore.token) {
    router.push('/dashboard');
    return;
  }

  // Pre-fill referral code from URL if present
  if (route.query.ref) {
    registerData.value.referralCodeUsed = route.query.ref;
  }
});

const handleRegister = async () => {
  loading.value = true;
  try {
    await courseStore.register(
      registerData.value.fullname,
      registerData.value.email,
      registerData.value.password,
      registerData.value.referralCodeUsed
    );
    
    // Auto login after registration
    await courseStore.login(registerData.value.email, registerData.value.password);
    alert('Đăng ký tài khoản thành công! Chào mừng bạn đến với ACC Academy.');
    router.push('/dashboard');
  } catch (err) {
    alert('Đăng ký thất bại: ' + err.message);
  } finally {
    loading.value = false;
  }
};
</script>
