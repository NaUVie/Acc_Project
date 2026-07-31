<template>
  <div class="case-studies-view container">
    <div class="header-section">
      <div class="badge">CASE STUDIES</div>
      <h1>Câu chuyện <span class="gradient-text">Thành công</span></h1>
      <p class="subtitle">Khám phá các dự án đào tạo In-house tiêu biểu và phản hồi từ các doanh nghiệp đối tác hàng đầu cùng đồng hành với ACC Academy.</p>
    </div>

    <div class="cases-grid">
      <div class="case-card glass-card">
        <span class="partner">Tập đoàn Tài chính ACB</span>
        <h2>Đào tạo ứng dụng Generative AI cho 150+ nhân sự quản lý</h2>
        <p>Giúp bộ phận nhân sự và kinh doanh ứng dụng ChatGPT nâng cao hiệu suất viết báo cáo và phân tích dữ liệu, tiết kiệm trung bình 8 giờ làm việc mỗi tuần.</p>
      </div>

      <div class="case-card glass-card">
        <span class="partner">Công ty Công nghệ Bosch Việt Nam</span>
        <h2>Chương trình kỹ năng giải quyết vấn đề phức tạp (Problem Solving)</h2>
        <p>Huấn luyện phương pháp tư duy 8D và kỹ năng phản biện giúp đội ngũ kỹ sư giải quyết hiệu quả các sự cố vận hành kỹ thuật quy mô lớn.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.case-studies-view {
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

.cases-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
}

.case-card {
  padding: 40px;
  border-radius: var(--radius-lg);
}

.partner {
  color: var(--primary);
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.case-card h2 {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  margin: 12px 0 16px 0;
  line-height: 1.35;
}

.case-card p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.65;
}

@media (max-width: 768px) {
  .cases-grid {
    grid-template-columns: 1fr;
  }
}
</style>
