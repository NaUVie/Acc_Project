<template>
  <div class="corporate-training-page">
    <!-- Header Section với nền xanh navy gradient nhạt dần -->
    <section class="corporate-hero-section">
      <div class="hero-backdrop-glow"></div>
      <div class="container hero-inner">
        <span class="hero-badge animate-fade-in">ĐÀO TẠO DOANH NGHIỆP</span>
        <h1 class="hero-title animate-fade-in">Giải pháp <span class="gradient-text">Đào tạo In-House & May đo</span></h1>
        <p class="hero-subtitle animate-fade-in">
          Chương trình đào tạo năng lực số, tư duy quản lý và công nghệ AI được thiết kế riêng theo thách thức thực tế và mục tiêu tăng trưởng dài hạn của doanh nghiệp
        </p>

        <!-- Filter Tabs / Navbar -->
        <div class="filter-tabs animate-fade-in">
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
      </div>
    </section>

    <div class="container corporate-content-container">
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
                <span class="arrow" style="display: inline-flex; align-items: center;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </span>
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

<style scoped src="@/styles/views/corporate/CorporateTraining.css"></style>
