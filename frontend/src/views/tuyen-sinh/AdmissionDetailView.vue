<template>
  <div class="admission-detail-view" v-if="program">
    <!-- Breadcrumb -->
    <div class="container breadcrumb-container">
      <router-link to="/tuyen-sinh" class="breadcrumb-link">&larr; Quay lại Trang Tuyển sinh</router-link>
    </div>

    <!-- Article Hero Banner -->
    <section class="article-hero">
      <div class="container">
        <span class="hero-category-tag">{{ program.category }}</span>
        <h1 class="hero-title">{{ program.title }}</h1>
        <p class="hero-subtitle">{{ program.subtitle }}</p>

        <div class="article-meta-row">
          <div class="meta-author">
            <span class="avatar-icon">🏛️</span>
            <div>
              <div class="author-name">Hội đồng Tuyển sinh ACC Academy & Đại học Andrews</div>
              <div class="publish-date">Cập nhật kỳ tuyển sinh 2026</div>
            </div>
          </div>
          <router-link :to="`/contact?program=${program.id}`" class="btn btn-consult">
            Đăng ký tư vấn ngay &rarr;
          </router-link>
        </div>
      </div>
    </section>

    <!-- Main Content Container -->
    <div class="container article-layout">
      <main class="article-main-body glass-card">
        <div class="cover-image-box">
          <img :src="program.image" :alt="program.title" class="cover-img" />
        </div>

        <!-- Article Sections -->
        <div class="content-sections">
          <div v-for="(sec, idx) in program.sections" :key="idx" class="section-block">
            <h2 class="section-heading">{{ sec.heading }}</h2>
            <div class="section-text" v-html="sec.content"></div>
          </div>
        </div>

        <!-- Call to Action Banner inside article -->
        <div class="article-cta-box">
          <h3>Sẵn sàng trở thành nhà Lãnh đạo tương lai?</h3>
          <p>Nhận thông báo tuyển sinh, bộ đề thi mẫu và tư vấn học bổng trực tiếp từ Ban Tuyển sinh.</p>
          <div class="cta-actions">
            <router-link :to="`/contact?program=${program.id}`" class="btn btn-primary-large">
              Đăng ký Tuyển sinh Ngay
            </router-link>
            <a :href="program.officialLink || 'https://zalo.me/0901234567'" target="_blank" class="btn btn-zalo">
              Tư vấn qua Zalo Hotline
            </a>
          </div>
        </div>
      </main>

      <!-- Sidebar Sticky Widget -->
      <aside class="article-sidebar">
        <div class="sidebar-widget glass-card">
          <h4 class="widget-title">📌 Thông tin Tuyển sinh</h4>
          <div class="info-list">
            <div class="info-item">
              <span class="label">Đối tượng:</span>
              <span class="val">{{ program.meta.target }}</span>
            </div>
            <div class="info-item">
              <span class="label">Thời gian:</span>
              <span class="val">{{ program.meta.duration }}</span>
            </div>
            <div class="info-item">
              <span class="label">Hình thức:</span>
              <span class="val">{{ program.meta.format }}</span>
            </div>
            <div class="info-item">
              <span class="label">Bằng cấp:</span>
              <span class="val">{{ program.meta.degree }}</span>
            </div>
          </div>
          <router-link :to="`/contact?program=${program.id}`" class="btn btn-block-primary">
            Nhận Đề án Tuyển sinh (PDF)
          </router-link>
        </div>

        <!-- Related Programs Widget -->
        <div class="sidebar-widget glass-card style-mt">
          <h4 class="widget-title">Chương trình Tuyển sinh khác</h4>
          <div class="related-list">
            <router-link 
              v-for="rel in otherPrograms" 
              :key="rel.id" 
              :to="`/tuyen-sinh/detail/${rel.id}`" 
              class="related-item"
            >
              <span class="rel-title">{{ rel.title }}</span>
              <span class="rel-arrow">&rarr;</span>
            </router-link>
          </div>
        </div>
      </aside>
    </div>
  </div>

  <div v-else class="container not-found-state">
    <h2>Không tìm thấy bài viết tuyển sinh</h2>
    <router-link to="/tuyen-sinh" class="btn btn-primary">Quay lại Trang Tuyển sinh</router-link>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const programsData = {
  'mba': {
    id: 'mba',
    title: 'Chương trình Thạc sĩ Quản trị Kinh doanh (MBA Andrews Hoa Kỳ)',
    category: 'BẰNG QUỐC TẾ HOA KỲ',
    subtitle: 'Tấm bằng MBA bảo chứng toàn cầu từ đại học lâu đời nước Mỹ, chuẩn hóa năng lực lãnh đạo thời kỳ chuyển đổi số.',
    image: '/images/service_card_2.webp',
    officialLink: 'https://andrews.edu.vn/',
    meta: {
      target: 'Chủ doanh nghiệp, Quản lý cấp cao & C-Level',
      duration: '18 tháng',
      format: 'Cuối tuần & Kết hợp Trực tuyến',
      degree: 'Bằng Thạc sĩ do ĐH Andrews (Hoa Kỳ) trực tiếp cấp'
    },
    sections: [
      {
        heading: '1. Giới thiệu về Đại học Andrews (Hoa Kỳ)',
        content: '<p>Được thành lập vào năm 1874 tại bang Michigan (Hoa Kỳ), Đại học Andrews là một trong những trường đại học lâu đời và uy tín hàng đầu tại Mỹ. Trường đạt kiểm định chất lượng vùng Higher Learning Commission (HLC) – kiểm định uy tín nhất tại Hoa Kỳ.</p><p>Chương trình MBA Andrews tại Việt Nam mang đến chương trình học nguyên bản được thiết kế phù hợp với bối cảnh kinh tế Châu Á – TBD.</p>'
      },
      {
        heading: '2. Cấu trúc Chương trình Đào tạo',
        content: '<p>Chương trình gồm 12 môn học trọng yếu bao gồm: Quản trị Chiến lược, Tài chính Doanh nghiệp, Đổi mới Sáng tạo, Marketing Toàn cầu và Lãnh đạo Đa văn hóa. Mọi môn học được chuẩn hóa theo hệ thống giáo trình của Hoa Kỳ.</p>'
      },
      {
        heading: '3. Điều kiện Tuyển sinh & Hồ sơ',
        content: '<p>Ứng viên cần tốt nghiệp Đại học ngành bất kỳ, có tối thiểu 2 năm kinh nghiệm làm việc và đạt yêu cầu kiểm tra trình độ tiếng Anh đầu vào của nhà trường.</p>'
      }
    ]
  },
  'mini-mba': {
    id: 'mini-mba',
    title: 'Chương trình Mini MBA Practical – Quản trị Tinh gọn Thực chiến',
    category: 'QUẢN TRỊ TINH GỌN',
    subtitle: 'Cô đọng tinh hoa quản trị MBA trong 3-6 tháng dành cho Quản lý cấp trung và Chủ doanh nghiệp SMEs.',
    image: '/images/Service_card_2.png',
    meta: {
      target: 'Quản lý phòng ban, Giám đốc chức năng & SMEs',
      duration: '3 - 6 tháng',
      format: 'Thực chiến 100% tại lớp',
      degree: 'Chứng nhận hoàn thành chương trình Mini MBA'
    },
    sections: [
      {
        heading: '1. Tại sao lựa chọn Mini MBA Practical?',
        content: '<p>Mini MBA Practical là mô hình đào tạo tinh gọn được tối ưu hóa nhằm giải quyết trực tiếp các điểm nghẽn trong vận hành, nhân sự và tài chính của doanh nghiệp Việt Nam.</p>'
      },
      {
        heading: '2. Nội dung huấn luyện trọng tâm',
        content: '<p>Học viên sẽ làm chủ 5 trụ cột: Xây dựng Ma trận Năng lực phòng ban, Tối ưu Dòng tiền, Ứng dụng AI trong vận hành tự động, Thiết lập KPI/OKR thực chiến và Tư duy Lãnh đạo tạo tác động.</p>'
      }
    ]
  },
  'gel': {
    id: 'gel',
    title: 'Viện Lãnh đạo Toàn cầu GEL (Global Executive Leadership)',
    category: 'LÃNH ĐẠO TOÀN CẦU',
    subtitle: 'Chương trình Huấn luyện Lãnh đạo Cấp cao & Study Tour Quốc tế tại Michigan (Hoa Kỳ).',
    image: '/images/service_card.webp',
    meta: {
      target: 'Chủ tịch, CEO, Tổng giám đốc Tập đoàn',
      duration: 'Theo khóa & Study Tour 10 ngày',
      format: 'Hội thảo & Trải nghiệm thực tế tại Mỹ',
      degree: 'Chứng nhận Lãnh đạo Toàn cầu từ LEADMAN & Andrews'
    },
    sections: [
      {
        heading: '1. Định vị Chương trình GEL',
        content: '<p>GEL được thiết kế dành riêng cho các nhà lãnh đạo kiệt xuất hướng tới mục tiêu vươn tầm thế giới. Chương trình kết hợp giữa các buổi hội thảo cấp cao và chuyến đi khảo sát thực địa tại các tập đoàn Fortune 500 tại Mỹ.</p>'
      },
      {
        heading: '2. Đặc quyền Học viên GEL',
        content: '<p>Kết nối trực tiếp với hội đồng cố vấn quốc tế, mở rộng quan hệ đối tác chiến lược và trải nghiệm môi trường học thuật hàng đầu tại Đại học Andrews (Michigan, USA).</p>'
      }
    ]
  }
};

const programId = computed(() => {
  const param = route.params.id || route.path.split('/').pop();
  if (param === 'mba' || param.includes('mba')) return 'mba';
  if (param === 'mini-mba' || param.includes('mini')) return 'mini-mba';
  if (param === 'gei' || param === 'gel' || param.includes('gel')) return 'gel';
  return 'mba';
});

const program = computed(() => {
  return programsData[programId.value] || programsData['mba'];
});

const otherPrograms = computed(() => {
  return Object.values(programsData).filter(p => p.id !== programId.value);
});

onMounted(() => {
  window.scrollTo(0, 0);
});
</script>

<style scoped>
.admission-detail-view {
  padding-top: 100px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.breadcrumb-container {
  margin-bottom: 24px;
}

.breadcrumb-link {
  color: #022B9F;
  font-weight: 700;
  text-decoration: none;
  font-size: 14px;
}

.article-hero {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 40px 0;
  margin-bottom: 40px;
}

.hero-category-tag {
  font-size: 12px;
  font-weight: 800;
  color: #022B9F;
  letter-spacing: 1.5px;
  display: block;
  margin-bottom: 12px;
}

.hero-title {
  font-size: 36px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.3;
  margin-bottom: 16px;
  max-width: 900px;
}

.hero-subtitle {
  font-size: 18px;
  color: #475569;
  line-height: 1.6;
  max-width: 850px;
  margin-bottom: 28px;
}

.article-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  border-top: 1px solid #f1f5f9;
  padding-top: 20px;
}

.meta-author {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-icon {
  font-size: 28px;
}

.author-name {
  font-weight: 700;
  color: #1e293b;
  font-size: 14px;
}

.publish-date {
  font-size: 12px;
  color: #64748b;
}

.article-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 36px;
}

.article-main-body {
  background: #ffffff;
  border-radius: 20px;
  padding: 36px;
  border: 1px solid rgba(0,0,0,0.06);
}

.cover-image-box {
  width: 100%;
  height: 380px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 36px;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.content-sections {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-heading {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 12px;
}

.section-text {
  font-size: 16px;
  color: #334155;
  line-height: 1.75;
}

.article-cta-box {
  margin-top: 48px;
  background: linear-gradient(135deg, #022B9F 0%, #0369a1 100%);
  color: #ffffff;
  padding: 36px;
  border-radius: 16px;
  text-align: center;
}

.article-cta-box h3 {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 10px;
}

.article-cta-box p {
  font-size: 15px;
  opacity: 0.9;
  margin-bottom: 24px;
}

.cta-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border-radius: 30px;
  font-weight: 700;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-consult {
  background-color: #022B9F;
  color: #ffffff;
}

.btn-primary-large {
  background-color: #ffffff;
  color: #022B9F;
}

.btn-zalo {
  background-color: #0068ff;
  color: #ffffff;
}

.article-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar-widget {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(0,0,0,0.06);
}

.widget-title {
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 10px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
}

.info-item .val {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
}

.btn-block-primary {
  width: 100%;
  background-color: #022B9F;
  color: #ffffff;
  text-align: center;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: #f8fafc;
  border-radius: 10px;
  text-decoration: none;
  color: #334155;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.related-item:hover {
  background: #022B9F;
  color: #ffffff;
}

@media (max-width: 992px) {
  .article-layout {
    grid-template-columns: 1fr;
  }
  .hero-title {
    font-size: 26px;
  }
}
</style>
