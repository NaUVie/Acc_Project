<template>
  <div class="team-view container">
    <div class="header-section">
      <div class="badge">TEAM PRODUCTIVITY</div>
      <h1>AI for <span class="gradient-text">Team</span></h1>
      <p class="subtitle">Chương trình huấn luyện thực chiến giúp nhóm phòng ban (Marketing, Sales, HR, Admin) tích hợp AI trực tiếp vào công việc hàng tuần để giải phóng sức lao động.</p>
    </div>

    <div class="departments-grid">
      <div class="dept-card glass-card">
        <h3>AI cho Marketing & Sales</h3>
        <p>Tạo ý tưởng chiến dịch, viết nội dung PR, tạo ảnh minh họa, tối ưu SEO và tự động hóa soạn thảo email chào hàng cá nhân hóa quy mô lớn.</p>
      </div>

      <div class="dept-card glass-card">
        <h3>AI cho HR & Training</h3>
        <p>Phân tích mô tả công việc, lọc hồ sơ ứng viên nhanh chóng, soạn thảo câu hỏi phỏng vấn chuẩn hóa và lên tài liệu onboarding tự động.</p>
      </div>

      <div class="dept-card glass-card">
        <h3>AI cho Admin & Operations</h3>
        <p>Tóm tắt các biên bản họp dài, dịch thuật tài liệu đa ngôn ngữ chuẩn xác, tự động hóa lập biểu mẫu Excel và làm báo cáo tiến độ dự án.</p>
      </div>
    </div>

    <div class="cta-box glass-card">
      <h2>Xây dựng năng lực AI cho đội ngũ của bạn</h2>
      <p>Chọn phòng ban cần đào tạo và chúng tôi sẽ thiết kế chương trình huấn luyện thực chiến riêng.</p>
      <router-link to="/contact" class="btn btn-primary">Liên hệ đăng ký khóa học</router-link>
    </div>
  </div>
</template>

<style scoped>
.team-view {
  padding: 60px 24px;
}

.header-section {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 60px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.badge {
  background: rgba(14, 165, 233, 0.15);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: var(--primary);
  padding: 6px 16px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.header-section h1 {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 800;
}

.subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.departments-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 60px;
}

.dept-card {
  padding: 30px;
  border-radius: var(--radius-md);
}

.dept-card h3 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
}

.dept-card p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.cta-box {
  padding: 50px;
  text-align: center;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.cta-box h2 {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 800;
}

.cta-box p {
  color: var(--text-secondary);
  max-width: 600px;
}

@media (max-width: 968px) {
  .departments-grid {
    grid-template-columns: 1fr;
  }
}
</style>
