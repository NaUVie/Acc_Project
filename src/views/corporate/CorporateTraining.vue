<template>
  <div class="corporate-view container">
    <div class="header-section">
      <div class="badge">ĐÀO TẠO DOANH NGHIỆP</div>
      <h1>Giải pháp <span class="gradient-text">Đào tạo In-House</span></h1>
      <p class="subtitle">Chương trình đào tạo năng lực số, tư duy quản lý và công nghệ số được may đo riêng theo thách thức thực tế và mục tiêu tăng trưởng của doanh nghiệp bạn.</p>
    </div>

    <!-- Core Features -->
    <div class="features-grid">
      <div class="feature-card glass-card">
        <h3>1. Khảo sát & Đánh giá</h3>
        <p>Phối hợp cùng bộ phận L&D/HR khảo sát năng lực đội ngũ hiện tại và ghi nhận bài toán nghiệp vụ của tổ chức để đề xuất nội dung đào tạo phù hợp nhất.</p>
      </div>
      
      <div class="feature-card glass-card">
        <h3>2. May đo Chương trình</h3>
        <p>Thiết kế giáo án, bài tập thực hành dựa trên chính case study và dữ liệu giả lập của doanh nghiệp để học viên dễ dàng áp dụng trực tiếp sau khóa học.</p>
      </div>

      <div class="feature-card glass-card">
        <h3>3. Đội ngũ Giảng viên</h3>
        <p>Các chuyên gia hàng đầu có kinh nghiệm thực tế sâu sắc trong lĩnh vực Trí tuệ nhân tạo, Quản trị số, Lean, Agile và Tối ưu vận hành doanh nghiệp.</p>
      </div>
    </div>

    <!-- Contact CTA -->
    <div class="cta-box glass-card">
      <h2>Bắt đầu nâng tầm năng lực đội ngũ của bạn</h2>
      <p>Nhận ngay đề xuất khung chương trình đào tạo in-house miễn phí phù hợp với quy mô và yêu cầu doanh nghiệp.</p>
      <router-link to="/contact" class="btn btn-primary">Liên hệ tư vấn Doanh nghiệp</router-link>
    </div>
  </div>
</template>

<style scoped>
.corporate-view {
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

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 60px;
}

.feature-card {
  padding: 30px;
  border-radius: var(--radius-md);
}

.feature-card h3 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
}

.feature-card p {
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
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
