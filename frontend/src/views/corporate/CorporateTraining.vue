<template>
  <div class="corporate-training-page">
    <div class="container">
      <!-- Header Section -->
      <div class="header-section">
        <span class="custom-ui-tag hero-tag">ĐÀO TẠO DOANH NGHIỆP</span>
        <h1 class="hero-title">Giải pháp <span class="gradient-text">Đào tạo In-House & May đo</span></h1>
        <p class="hero-subtitle">
          Chương trình đào tạo năng lực số, tư duy quản lý và công nghệ AI được thiết kế riêng theo thách thức thực tế và mục tiêu tăng trưởng dài hạn của doanh nghiệp.
        </p>
      </div>

      <!-- Filter Tabs / Navbar -->
      <div class="filter-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: activeFilter === 'all' }"
          @click="activeFilter = 'all'"
        >
          Tất cả chương trình
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeFilter === 'da-thuc-hien' }"
          @click="activeFilter = 'da-thuc-hien'"
        >
          Chương trình đã thực hiện
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeFilter === 'dang-thuc-hien' }"
          @click="activeFilter = 'dang-thuc-hien'"
        >
          Chương trình đang thực hiện
        </button>
      </div>

      <!-- Training Programs Grid -->
      <div class="programs-grid">
        <div 
          v-for="prog in filteredPrograms" 
          :key="prog.id" 
          class="program-card"
        >
          <div class="prog-image-wrapper">
            <img :src="prog.image" :alt="prog.title" class="prog-image" referrerpolicy="no-referrer" />
            <span class="status-badge" :class="prog.status">
              {{ prog.statusText }}
            </span>
          </div>

          <div class="prog-body">
            <div class="prog-client-tag">🏢 {{ prog.client }}</div>
            <h3 class="prog-title">{{ prog.title }}</h3>
            <p class="prog-desc">{{ prog.description }}</p>
            
            <div class="prog-highlights">
              <div v-for="(h, idx) in prog.highlights" :key="idx" class="highlight-item">
                <span class="check-icon">✓</span>
                <span>{{ h }}</span>
              </div>
            </div>

            <div class="prog-footer">
              <router-link to="/contact" class="btn-consult">
                <span>Đăng ký tư vấn In-House</span>
                <span class="arrow">&rarr;</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Core Value Process -->
      <div class="process-section">
        <h2 class="process-title">Quy trình 3 bước may đo chương trình đào tạo</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-num">01</div>
            <h3>Khảo sát & Đánh giá</h3>
            <p>Phối hợp cùng bộ phận L&D/HR khảo sát ma trận năng lực hiện tại và ghi nhận bài toán nghiệp vụ thực tế của tổ chức.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-num">02</div>
            <h3>May đo Giáo án</h3>
            <p>Thiết kế nội dung, bộ Prompt mẫu và bài tập dựa trên chính case study và dữ liệu thực tế của doanh nghiệp bạn.</p>
          </div>

          <div class="feature-card">
            <div class="feature-num">03</div>
            <h3>Đào tạo & Đồng hành</h3>
            <p>Đội ngũ giảng viên thực chiến trực tiếp cầm tay chỉ việc, theo sát và đánh giá kết quả áp dụng công việc sau đào tạo.</p>
          </div>
        </div>
      </div>

      <!-- Contact CTA -->
      <div class="cta-box">
        <h2>Bắt đầu nâng tầm năng lực đội ngũ của bạn</h2>
        <p>Nhận ngay đề xuất khung chương trình đào tạo in-house miễn phí phù hợp với quy mô và yêu cầu cụ thể của doanh nghiệp.</p>
        <router-link to="/contact" class="btn-cta-primary">Liên hệ tư vấn Doanh nghiệp ngay</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const activeFilter = ref('all');

const trainingPrograms = [
  {
    id: 1,
    status: 'da-thuc-hien',
    statusText: 'Đã thực hiện',
    client: 'Tập đoàn Tài chính ACB',
    title: 'Đào tạo AI & Automation cho Cán bộ Quản lý ACB',
    description: 'Lộ trình 4 tuần tự động hóa quy trình báo cáo, phân tích tài chính và tư vấn dịch vụ khách hàng bằng Generative AI.',
    image: 'https://drive.google.com/thumbnail?id=120WyoSixRMCuWCMFeNjFKxsDzt74filf&sz=w800',
    highlights: ['Huấn luyện 150+ quản lý cấp trung', 'Xây dựng bộ 100+ prompt chuyên biệt', 'Tiết kiệm 6-8h/tuần/nhân sự']
  },
  {
    id: 2,
    status: 'da-thuc-hien',
    statusText: 'Đã thực hiện',
    client: 'Bosch Việt Nam',
    title: 'Xây dựng Khung Năng lực Số & Kỹ năng Giải quyết Vấn đề',
    description: 'Chương trình huấn luyện tư duy 8D, phân tích nguyên nhân gốc rễ và tích hợp công cụ AI vào vận hành kỹ thuật.',
    image: 'https://drive.google.com/thumbnail?id=1ZININwRW94lavoqqoJ3eAArE5v6vsyZ5&sz=w800',
    highlights: ['May đo chuẩn ma trận Bosch Global', 'Huấn luyện 100% kỹ sư công nghệ', 'Ứng dụng thực hành 80% thời lượng']
  },
  {
    id: 3,
    status: 'dang-thuc-hien',
    statusText: 'Đang thực hiện',
    client: 'Ngân hàng SHB',
    title: 'Đào tạo AI Leadership & Tối ưu Vận hành Doanh nghiệp',
    description: 'Tư vấn chiến lược tích hợp Generative AI vào văn hóa doanh nghiệp và xây dựng Trung tâm năng lực AI (CoE).',
    image: 'https://drive.google.com/thumbnail?id=1CU6Pq9-wx_l2DPlb7uigkGIvCtcl921E&sz=w800',
    highlights: ['Tư vấn trực tiếp cho C-Level', 'Thiết lập khung bảo mật dữ liệu ngân hàng', 'Chuẩn hóa lộ trình chuyển đổi số']
  },
  {
    id: 4,
    status: 'dang-thuc-hien',
    statusText: 'Đang thực hiện',
    client: 'Amway Việt Nam',
    title: 'Đào tạo Ứng dụng GenAI cho Đội ngũ Sales & Marketing',
    description: 'Ứng dụng ChatGPT, Claude & Midjourney sáng tạo nội dung đa kênh, thiết kế hình ảnh truyền thông bứt phá hiệu suất.',
    image: 'https://drive.google.com/thumbnail?id=1miKA4icyQ_nAgwQe5vQge3bqg2W_f8zg&sz=w800',
    highlights: ['Tự động hóa 70% quy trình viết bài', 'Chuẩn hóa thiết kế thương hiệu', 'Cá nhân hóa chăm sóc khách hàng']
  }
];

const filteredPrograms = computed(() => {
  if (activeFilter.value === 'all') return trainingPrograms;
  return trainingPrograms.filter(p => p.status === activeFilter.value);
});
</script>

<style scoped>
.corporate-training-page {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.header-section {
  text-align: center;
  max-width: 860px;
  margin-inline: auto;
  margin-bottom: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.hero-tag {
  background: rgba(2, 43, 159, 0.08);
  color: #022b9f;
  font-weight: 800;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
}

.hero-title {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.gradient-text {
  background: linear-gradient(135deg, #022b9f 0%, #2563eb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 16px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  color: #475569;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.tab-btn:hover {
  border-color: #022b9f;
  color: #022b9f;
  background: #f0f4ff;
}

.tab-btn.active {
  background: #022b9f;
  color: #ffffff;
  border-color: #022b9f;
  box-shadow: 0 4px 14px rgba(2, 43, 159, 0.25);
}

.programs-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 32px;
  margin-bottom: 72px;
}

@media (min-width: 768px) {
  .programs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.program-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.program-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: #022b9f;
}

.prog-image-wrapper {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: #e2e8f0;
}

.prog-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.program-card:hover .prog-image {
  transform: scale(1.05);
}

.status-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  padding: 5px 14px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 0.5px;
}

.status-badge.da-thuc-hien {
  background: #022b9f;
}

.status-badge.dang-thuc-hien {
  background: #d97706;
}

.prog-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.prog-client-tag {
  font-size: 13px;
  font-weight: 700;
  color: #022b9f;
  margin-bottom: 8px;
}

.prog-title {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.prog-desc {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin-bottom: 18px;
}

.prog-highlights {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.check-icon {
  color: #059669;
  font-weight: 800;
}

.prog-footer {
  margin-top: auto;
}

.btn-consult {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 700;
  font-size: 14px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.btn-consult:hover {
  background: #1e40af;
}

.process-section {
  margin-bottom: 60px;
  text-align: center;
}

.process-title {
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 36px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 24px;
}

@media (min-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.feature-card {
  background: #ffffff;
  padding: 32px 24px;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  text-align: left;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.03);
}

.feature-num {
  font-size: 32px;
  font-weight: 900;
  color: #022b9f;
  margin-bottom: 12px;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
}

.feature-card p {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.cta-box {
  background: linear-gradient(135deg, #022b9f 0%, #1e40af 100%);
  border-radius: 24px;
  padding: 48px 32px;
  text-align: center;
  color: #ffffff;
}

.cta-box h2 {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 12px 0;
}

.cta-box p {
  font-size: 16px;
  opacity: 0.9;
  max-width: 680px;
  margin: 0 auto 28px auto;
  line-height: 1.6;
}

.btn-cta-primary {
  display: inline-block;
  padding: 14px 32px;
  background: #ffffff;
  color: #022b9f;
  font-weight: 800;
  font-size: 15px;
  border-radius: 12px;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-cta-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
}
</style>
