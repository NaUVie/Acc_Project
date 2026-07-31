<template>
  <div class="login-view container">
    <div class="login-card glass-card">
      <div class="card-header">
        <h1>Đăng nhập học tập</h1>
        <p>Hệ thống Quản lý Học tập (LMS) - ACC Academy</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Tài khoản Email</label>
          <input type="email" id="email" placeholder="name@domain.com" required>
        </div>

        <div class="form-group">
          <label for="password">Mật khẩu</label>
          <input type="password" id="password" placeholder="••••••••" required>
        </div>

        <button type="submit" class="btn btn-primary w-full">Đăng nhập</button>
      </form>
      
      <div class="card-footer">
        <a href="#">Quên mật khẩu?</a>
      </div>
    </div>
  </div>
</template>

<script setup>
const handleLogin = () => {
  alert('Đăng nhập thành công! Chào mừng đến với hệ thống LMS.');
};
</script>

<style scoped>
.login-view {
  padding: 80px 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 160px);
}

.login-card {
  width: 100%;
  max-width: 440px;
  padding: 40px;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.card-header h1 {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 8px;
}

.card-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-group input {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-color);
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  color: white;
  font-family: inherit;
  transition: var(--transition);
}

.form-group input:focus {
  border-color: var(--primary);
  outline: none;
  background-color: rgba(255, 255, 255, 0.05);
}

.w-full {
  width: 100%;
  margin-top: 10px;
}

.card-footer {
  text-align: center;
  font-size: 14px;
}

.card-footer a {
  color: var(--primary);
}
</style>
