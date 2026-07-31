<template>
  <div class="coe-view container">
    <div class="header-section">
      <div class="badge">AI SOLUTION</div>
      <h1>AI <span class="gradient-text">Center of Excellence</span></h1>
      <p class="subtitle">Hỗ trợ doanh nghiệp xây dựng trung tâm năng lực AI nội bộ để dẫn đầu xu thế, làm chủ công nghệ và thúc đẩy chuyển đổi số thực chất.</p>
    </div>

    <div class="content-grid">
      <div class="glass-card info-card">
        <h2>AI CoE là gì?</h2>
        <p>AI Center of Excellence (CoE) là mô hình tập trung hóa kiến thức, năng lực và tài nguyên AI của doanh nghiệp nhằm hướng dẫn, triển khai và mở rộng quy mô các giải pháp AI một cách có hệ thống, an toàn và tối ưu chi phí.</p>
      </div>

      <div class="glass-card info-card">
        <h2>Giải pháp của chúng tôi</h2>
        <p>Chúng tôi đồng hành cùng hội đồng quản trị và ban điều hành xây dựng năng lực AI cốt lõi thông qua: tư vấn khung chính sách ứng dụng AI an toàn (AI Governance), đào tạo nâng cao kỹ năng cho đội ngũ hạt nhân, và hỗ trợ phát triển các dự án AI Proof-of-Concept (POC) ban đầu.</p>
      </div>
    </div>

    <div class="cta-box glass-card">
      <h2>Tư vấn xây dựng mô hình AI CoE</h2>
      <p>Bắt đầu hành trình chuyển đổi số toàn diện và định hình tương lai ứng dụng AI trong doanh nghiệp của bạn ngay hôm nay.</p>
      <router-link to="/contact" class="btn btn-primary">Đặt lịch hẹn với Chuyên gia</router-link>
    </div>
  </div>
</template>

<style scoped>
.coe-view {
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

.content-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-bottom: 60px;
}

.info-card {
  padding: 40px;
  border-radius: var(--radius-md);
}

.info-card h2 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
}

.info-card p {
  color: var(--text-secondary);
  line-height: 1.7;
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

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
