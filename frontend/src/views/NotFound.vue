<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f8fafc; text-align: center; padding: 40px 20px;">
    <div>
      <div style="font-size: 80px; margin-bottom: 16px;">🔍</div>
      <h1 style="font-size: 36px; font-weight: 900; color: #0f172a; margin-bottom: 12px;">404 – Không tìm thấy trang</h1>
      <p style="font-size: 16px; color: #64748b; max-width: 420px; margin: 0 auto 32px;">Trang bạn đang tìm kiếm không tồn tại hoặc đã bị di chuyển sang địa chỉ khác.</p>
      <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
        <router-link to="/" style="padding: 12px 28px; background: #0284c7; color: #fff; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px;">
          🏠 Về Trang chủ
        </router-link>
        <router-link to="/courses/ai" style="padding: 12px 28px; background: #f1f5f9; color: #0f172a; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px; border: 1px solid #e2e8f0;">
          📚 Xem Khóa học
        </router-link>
      </div>
    </div>
  </div>
</template>
