<template>
  <div class="admissions-view">
    <!-- Hero Banner Section -->
    <section class="admissions-hero">
      <div class="container hero-container">

        <h1 class="hero-title animate-fade-in">
          Nâng tầm Lãnh đạo <br />
          & Khai phá <span class="gradient-text">Tiềm năng Quản trị</span>
        </h1>
        <p class="hero-subtitle animate-fade-in">
          Tổng hợp các chương trình đào tạo Thạc sĩ Quản trị Kinh doanh và Đào tạo Lãnh đạo cấp cao Quốc tế<br />
          hợp tác cùng Đại học Andrews (Hoa Kỳ).
        </p>

        <!-- Quick Jump Pills -->
        <div class="jump-pills">
          <button @click="scrollToSection('mba')" class="jump-pill active">
           MBA Andrews
          </button>
          <!-- <button @click="scrollToSection('mini-mba')" class="jump-pill">
            ⚡ Mini MBA
          </button> -->
          <button @click="scrollToSection('gei')" class="jump-pill">
          GEI (GOLBAL EXECUTIVE INSTITUTE)
          </button>
        </div>
      </div>
    </section>

    <!-- Admission Programs Section -->
    <section class="programs-section container">
      
      <!-- Program 1: MBA Andrews -->
      <div id="mba" class="program-card glass-card animate-slide-up">
        <div class="program-grid">
          <div class="program-media">
            <img src="/images/andrew.jpg" alt="MBA Andrews Hoa Kỳ" class="program-img" />
            <div class="program-tag-overlay">Bằng Quốc tế Hoa Kỳ</div>
          </div>
          <div class="program-content">
            <span class="program-category">THẠC SĨ QUẢN TRỊ KINH DOANH</span>
            <h2 class="program-title">MBA Andrews (Hoa Kỳ)</h2>
            <p class="program-desc">
              Chương trình Thạc sĩ Quản trị Kinh doanh chính quy do Đại học Andrews (Hoa Kỳ) trực tiếp cấp bằng. 
              Được bảo chứng chất lượng bởi Bộ Giáo dục & Đào tạo Việt Nam, mang đến hệ tư duy quản trị hiện đại, 
              mạng lưới kết nối cựu học viên là các CEO, Nhà sáng lập hàng đầu.
            </p>

            <div class="program-highlights">
              <div class="highlight-item">
                <span>Đại học Top đầu Hoa Kỳ (Thành lập từ 1874)</span>
              </div>
              <div class="highlight-item">
                <span>Bằng có giá trị toàn cầu & Bộ GD&ĐT Việt Nam công nhận</span>
              </div>
              <div class="highlight-item">
                <span>Thời gian học: 18 tháng (Cuối tuần & Online linh hoạt)</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link to="/tuyen-sinh/detail/mba" class="btn btn-primary">
                Xem chi tiết bài viết MBA Andrews &rarr;
              </router-link>
              <router-link to="/contact?program=mba" class="btn btn-outline">
                Đăng ký tư vấn tuyển sinh
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Program 2: Mini MBA -->
      <!-- <div id="mini-mba" class="program-card glass-card animate-slide-up">
        <div class="program-grid reverse">
          <div class="program-media">
            <img src="/images/Service_card_2.png" alt="Mini MBA Thực chiến" class="program-img" />
            <div class="program-tag-overlay badge-teal">Quản trị Tinh gọn</div>
          </div>
          <div class="program-content">
            <span class="program-category">QUẢN TRỊ THỰC CHUYÊN SÂU</span>
            <h2 class="program-title">Mini MBA Practical</h2>
            <p class="program-desc">
              Chương trình tinh gọn cô đọng những giá trị cốt lõi nhất của MBA trong 3-6 tháng. 
              Dành riêng cho các Giám đốc bộ phận, Quản lý cấp trung và Chủ doanh nghiệp SME 
              muốn tối ưu năng lực vận hành, tài chính, nhân sự và chiến lược tăng trưởng tức thì.
            </p>

            <div class="program-highlights">
              <div class="highlight-item">
                <span class="icon">⚡</span>
                <span>Tập trung 100% vào bài tập & case study thực tế</span>
              </div>
              <div class="highlight-item">
                <span class="icon">👨‍🏫</span>
                <span>Giảng dạy bởi đội ngũ Chuyên gia & C-Level thực chiến</span>
              </div>
              <div class="highlight-item">
                <span class="icon">📈</span>
                <span>Áp dụng ngay giải pháp vào doanh nghiệp của học viên</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link to="/tuyen-sinh/detail/mini-mba" class="btn btn-primary">
                Xem chi tiết bài viết Mini MBA &rarr;
              </router-link>
              <router-link to="/contact?program=mini-mba" class="btn btn-outline">
                Đăng ký tư vấn tuyển sinh
              </router-link>
            </div>
          </div>
        </div>
      </div> -->

      <!-- Program 3: GEI (GOLBAL EXECUTIVE INSTITUTE) -->
      <div id="gei" class="program-card glass-card animate-slide-up">
        <div class="program-grid">
          <div class="program-media">
            <img src="/images/GEL.jpg" alt="GOLBAL EXECUTIVE INSTITUTE (GEI)" class="program-img" />
            <div class="program-tag-overlay badge-gold">Lãnh đạo Cấp cao</div>
          </div>
          <div class="program-content">
            <span class="program-category">VIỆN LÃNH ĐẠO TOÀN CẦU</span>
            <h2 class="program-title">GEI (GOLBAL EXECUTIVE INSTITUTE)</h2>
            <p class="program-desc">
              Chương trình Đào tạo Lãnh đạo Cấp cao và Study Tour quốc tế tại Michigan (Hoa Kỳ). 
              Thiết kế dành riêng cho Lãnh đạo Tổng công ty, Tập đoàn và Doanh nghiệp lớn 
              nhằm hội nhập tư duy toàn cầu, quản trị biến động và thiết lập liên minh chiến lược.
            </p>

            <div class="program-highlights">
              <div class="highlight-item">
                <span>Trải nghiệm trực tiếp tại trụ sở các tập đoàn tại Hoa Kỳ</span>
              </div>
              <div class="highlight-item">
                <span>Giao lưu & kết nối với mạng lưới Lãnh đạo Doanh nghiệp quốc tế</span>
              </div>
              <div class="highlight-item">
                <span>Chứng nhận Lãnh đạo Toàn cầu từ Viện LEADMAN & Andrews</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link to="/tuyen-sinh/detail/gei" class="btn btn-primary">
                Xem chi tiết bài viết GEI &rarr;
              </router-link>
              <router-link to="/contact?program=gei" class="btn btn-outline">
                Đăng ký tư vấn tuyển sinh
              </router-link>
            </div>
          </div>
        </div>
      </div>

    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

const scrollToSection = (id) => {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

onMounted(() => {
  window.scrollTo(0, 0);
});
</script>

<style scoped>
.admissions-view {
  padding-top: 100px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.admissions-hero {
  text-align: center;
  padding: 40px 20px 60px;
  max-width: 960px;
  margin: 0 auto;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #eff6ff;
  color: #022B9F;
  font-size: 13px;
  font-weight: 800;
  padding: 8px 18px;
  border-radius: 30px;
  border: 1px solid #bfdbfe;
  margin-bottom: 20px;
  letter-spacing: 0.5px;
}

.bell-icon-pulse {
  display: inline-block;
  animation: bellShake 1.5s infinite ease-in-out;
}

@keyframes bellShake {
  0%, 100% { transform: rotate(0deg); }
  15% { transform: rotate(14deg); }
  30% { transform: rotate(-14deg); }
  45% { transform: rotate(10deg); }
  60% { transform: rotate(-10deg); }
  75% { transform: rotate(4deg); }
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.25;
  margin-bottom: 16px;
}

.gradient-text {
  background: linear-gradient(135deg, #022B9F 0%, #0284c7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 17px;
  color: #475569;
  line-height: 1.6;
  margin-bottom: 32px;
}

.jump-pills {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.jump-pill {
  padding: 10px 20px;
  border-radius: 30px;
  background-color: #ffffff;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.jump-pill:hover, .jump-pill.active {
  background-color: #022B9F;
  color: #ffffff;
  border-color: #022B9F;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(2, 43, 159, 0.25);
}

.programs-section {
  display: flex;
  flex-direction: column;
  gap: 40px;
  margin-top: 20px;
}

.program-card {
  background-color: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 36px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.program-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
}

.program-grid {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 40px;
  align-items: center;
}

.program-grid.reverse {
  grid-template-columns: 1fr 420px;
}

.program-grid.reverse .program-media {
  grid-column: 2;
}
.program-grid.reverse .program-content {
  grid-column: 1;
  grid-row: 1;
}

.program-media {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  height: 280px;
}

.program-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.program-card:hover .program-img {
  transform: scale(1.05);
}

.program-tag-overlay {
  position: absolute;
  top: 16px;
  left: 16px;
  background-color: #022B9F;
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 20px;
  text-transform: uppercase;
}

.program-tag-overlay.badge-teal {
  background-color: #0d9488;
}

.program-tag-overlay.badge-gold {
  background-color: #d97706;
}

.program-category {
  font-size: 12px;
  font-weight: 800;
  color: #022B9F;
  letter-spacing: 1.5px;
  display: block;
  margin-bottom: 8px;
}

.program-title {
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 14px;
}

.program-desc {
  font-size: 15px;
  color: #475569;
  line-height: 1.65;
  margin-bottom: 24px;
}

.program-highlights {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 28px;
  background-color: #f8fafc;
  padding: 16px 20px;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.highlight-item .icon {
  font-size: 16px;
}

.program-footer {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border-radius: 30px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
  cursor: pointer;
}

.btn-primary {
  background-color: #022B9F;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #0284c7;
  box-shadow: 0 6px 20px rgba(2, 43, 159, 0.3);
}

.btn-outline {
  background-color: transparent;
  border: 2px solid #cbd5e1;
  color: #334155;
}

.btn-outline:hover {
  border-color: #022B9F;
  color: #022B9F;
}

@media (max-width: 992px) {
  .program-grid, .program-grid.reverse {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  .program-grid.reverse .program-media {
    grid-column: 1;
  }
  .program-grid.reverse .program-content {
    grid-column: 1;
    grid-row: 2;
  }
  .program-media {
    height: 220px;
  }
  .hero-title {
    font-size: 30px;
  }
}
</style>
