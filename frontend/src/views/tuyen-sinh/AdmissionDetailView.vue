<template>
  <div class="admission-detail-view" v-if="program">
    <!-- Breadcrumb -->
    <div class="container breadcrumb-container">
      <router-link to="/admissions" class="breadcrumb-link">&larr; Quay lại Trang Tuyển sinh</router-link>
    </div>

    <!-- Article Hero Banner -->
    <section class="article-hero">
      <div class="container">
        <span class="hero-category-tag">{{ program.category }}</span>
        <h1 class="hero-title">{{ program.title }}</h1>
        <p class="hero-subtitle">{{ program.subtitle }}</p>

        <!-- <div class="article-meta-row">
          <div class="meta-author">
            <div>
              <div class="author-name">Hội đồng Tuyển sinh ACC Academy & Đại học Andrews</div>
              <div class="publish-date">Cập nhật kỳ tuyển sinh 2026</div>
            </div>
          </div>
          <router-link :to="`/contact?program=${program.id}`" class="btn btn-consult">
            Đăng ký tư vấn ngay &rarr;
          </router-link>
        </div> -->
      </div>
    </section>

    <!-- Main Content Container -->
    <div class="container article-layout">
      <main class="article-main-body glass-card">
        <div class="cover-image-box">
          <img :src="program.image" :alt="program.title" class="cover-img" />
        </div>

        <!-- Article Sections / Dynamic Content -->
        <div class="content-sections">
          <div v-if="program.content" class="section-text" v-html="sanitizeHtml(program.content)"></div>
          <template v-else-if="program.sections">
            <div v-for="(sec, idx) in program.sections" :key="idx" class="section-block">
              <h2 class="section-heading">{{ sec.heading }}</h2>
              <div class="section-text" v-html="sanitizeHtml(sec.content)"></div>
            </div>
          </template>
        </div>

        <!-- Call to Action Banner inside article -->
        <!-- <div class="article-cta-box">
          <h3>Sẵn sàng trở thành nhà Lãnh đạo tương lai?</h3>
          <p>Nhận thông báo tuyển sinh, bộ đề thi mẫu và tư vấn học bổng trực tiếp từ Ban Tuyển sinh.</p>
          <div class="cta-actions">
            <router-link :to="`/contact?program=${program.id}`" class="btn btn-primary-large">
              Đăng ký Tuyển sinh Ngay
            </router-link>
            <a :href=" 'https://zalo.me/0938566700'" target="_blank" class="btn btn-zalo">
              Tư vấn qua Zalo Hotline
            </a>
          </div>
        </div> -->
      </main>

      <!-- Sidebar Sticky Widget -->
      <aside class="article-sidebar">
        <!-- Related Programs Widget -->
        <div class="sidebar-widget glass-card">
          <h4 class="widget-title">Chương trình Tuyển sinh khác</h4>
          <div class="related-list">
            <router-link 
              v-for="rel in otherPrograms" 
              :key="rel.slug || rel.id" 
              :to="`/admissions/detail/${rel.slug || rel.id}`" 
              class="related-item"
            >
              <span class="rel-title">{{ rel.title }}</span>
              <span class="rel-arrow" style="display: inline-flex; align-items: center;">
                <svg class="block-arrow-glow" width="32" height="14" viewBox="0 0 52 24" fill="none">
                  <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#022B9F" />
                </svg>
              </span>
            </router-link>
          </div>
        </div>

        <!-- Hotline Support Widget -->
        <div class="sidebar-widget glass-card style-mt" style="text-align: center; padding: 22px 18px;">
          <div style="font-size: 28px; margin-bottom: 8px;">📞</div>
          <h4 style="margin: 0 0 6px 0; font-size: 16px; color: #0f172a; font-weight: 700;">Hỗ trợ Tuyển sinh</h4>
          <p style="font-size: 13px; color: #64748b; margin-bottom: 14px; line-height: 1.45;">Giải đáp nhanh điều kiện dự tuyển & chính sách học bổng.</p>
          <a href="https://zalo.me/0938566700" target="_blank" class="btn btn-primary" style="width: 100%; display: block; text-align: center; padding: 10px; font-weight: 700;">
            Chat Zalo Ban Tuyển sinh
          </a>
        </div>
      </aside>
    </div>
  </div>

  <div v-else class="container not-found-state">
    <h2>Không tìm thấy bài viết tuyển sinh</h2>
    <router-link to="/admissions" class="btn btn-primary">Quay lại Trang Tuyển sinh</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { sanitizeHtml } from '@/utils/sanitize';

const route = useRoute();
const courseStore = useCourseStore();

const programsData = {
  'mba': {
    id: 'mba',
    title: 'MBA Andrews Hoa Kỳ: Học quản trị theo chuẩn Mỹ, phát triển sự nghiệp tại Việt Nam',
    category: 'BẰNG QUỐC TẾ HOA KỲ',
    subtitle: 'Chương trình Thạc sĩ Quản trị Kinh doanh Đại học Andrews Hoa Kỳ được bảo chứng học thuật toàn cầu, học tại Việt Nam, cấp bằng chính quy từ Hoa Kỳ.',
    image: '/images/andrew.jpg',
    officialLink: 'https://andrews.edu.vn/',
    meta: {
      target: 'Chủ doanh nghiệp, Quản lý cấp cao & C-Level',
      duration: '18 – 20 tháng',
      format: 'Cuối tuần (phù hợp người đi làm)',
      degree: 'Bằng Thạc sĩ do ĐH Andrews (Hoa Kỳ) trực tiếp cấp'
    },
    sections: [
      {
        heading: '1. Vì sao chọn Đại học Andrews?',
        content: '<p>Được thành lập năm 1874 tại bang Michigan, Đại học Andrews là một trường đại học lâu đời của Hoa Kỳ với cộng đồng sinh viên và cựu học viên quốc tế rộng lớn. Chương trình kinh doanh của trường được kiểm định chuyên ngành bởi IACBE; Đại học Andrews được kiểm định vùng bởi Higher Learning Commission (HLC) và được Bộ Giáo dục — Đào tạo Việt Nam chính thức công nhận.</p>'
      },
      {
        heading: '2. Cấu trúc Chương trình Đào tạo',
        content: '<p>Chương trình học tinh gọn, phù hợp người đi làm kéo dài khoảng 18–20 tháng, với lịch học tập trung vào cuối tuần. Học viên được trang bị kiến thức từ nền tảng đến chuyên sâu về quản trị kinh doanh, với nội dung đào tạo theo chương trình MBA của Đại học Andrews.</p><p>Các môn học có thể bao gồm lãnh đạo và hành vi tổ chức, quản trị tài chính, marketing chiến lược, quản trị nguồn nhân lực, kinh doanh quốc tế và quản trị chiến lược.</p>'
      },
      {
        heading: '3. Điều kiện tuyển sinh tham khảo',
        content: '<ul><li>Tốt nghiệp đại học; đáp ứng yêu cầu GPA của chương trình, thường từ 2.6/4.0, hoặc thỏa điều kiện về điểm GPA của ít nhất 50% số môn học.</li><li>Trình độ tiếng Anh tương đương IELTS 5.5; chứng chỉ VSTEP bậc 4 có thể được xem xét theo quy định tuyển sinh.</li><li>Điều kiện GMAT có thể được đáp ứng bằng điểm GMAT theo yêu cầu, hoặc theo phương án thay thế dành cho ứng viên đủ kinh nghiệm làm việc và hoàn thành các môn Thống kê, Đại số theo yêu cầu của chương trình.</li><li>Bằng Cử nhân Ngôn ngữ Anh được giảng dạy hoàn toàn bằng tiếng Anh có thể thuộc diện xét miễn chứng chỉ tiếng Anh.</li></ul><p><em>* Điều kiện cụ thể có thể khác theo hồ sơ và đợt tuyển sinh. Ứng viên nên liên hệ chương trình để được xác nhận yêu cầu hiện hành.</em></p>'
      }
    ]
  },
  'gei': {
    id: 'gei',
    title: 'Global Executive Institute (GEI): Chương trình phát triển năng lực lãnh đạo trong thời đại AI',
    category: 'LÃNH ĐẠO TOÀN CẦU',
    subtitle: 'Chương trình lãnh đạo cấp cao gắn kết AI với chiến lược quản trị, thực thi ESG và tối ưu hóa vận hành tổ chức bền vững.',
    image: '/images/GEL.jpg',
    meta: {
      target: 'Lãnh đạo doanh nghiệp & Khu vực công',
      duration: 'Linh hoạt theo chuyên đề & Thực tế',
      format: 'Đào tạo, Hội thảo & Tham quan thực tế',
      degree: 'Chứng nhận AUCORE – Đại học Andrews (Hoa Kỳ)'
    },
    sections: [
      {
        heading: '1. Giới thiệu về Global Executive Institute (GEI)',
        content: '<p>Global Executive Institute (GEI) là chương trình lãnh đạo cấp cao thuộc AUCORE – Trung tâm Năng lực Tổ chức và Xuất sắc của Đại học Andrews, Hoa Kỳ.</p><p>Chương trình dành cho lãnh đạo doanh nghiệp và khu vực công, tập trung vào các lĩnh vực như phát triển bền vững, ESG, chuyển đổi số, trí tuệ nhân tạo và năng lực tài chính. Thông qua đào tạo, nghiên cứu và hợp tác, GEI hướng đến việc trang bị cho người học tư duy và năng lực cần thiết để điều hành tổ chức trong môi trường kinh doanh biến đổi nhanh chóng.</p>'
      },
      {
        heading: '2. Kết nối kiến thức với thực tiễn quản trị',
        content: '<p>GEI không giới hạn việc học trong lớp học. Các hoạt động tham quan thực tế để tìm hiểu các mô hình vận hành trong những lĩnh vực khác nhau mở ra cơ hội quan sát trực tiếp các bài toán quản trị liên quan đến hiệu quả hoạt động, sử dụng nguồn lực, đầu tư, phát triển nhân lực và tính bền vững. Qua đó, người học có thể liên hệ các nội dung được thảo luận với bối cảnh tổ chức và ngành nghề của mình.</p><p>Chương trình cũng tạo không gian trao đổi giữa các nhà lãnh đạo đến từ nhiều lĩnh vực. Việc chia sẻ kinh nghiệm và góc nhìn giúp học viên mở rộng cách tiếp cận trước những thách thức chung, đồng thời xem xét khả năng vận dụng kiến thức vào thực tế điều hành.</p><p>Với sự kết hợp giữa nền tảng học thuật, nội dung quản trị và trải nghiệm thực tế, Global Executive Institute hướng đến việc giúp các nhà lãnh đạo hiểu rõ hơn tiềm năng của công nghệ mới, đưa ra quyết định có cơ sở và dẫn dắt đổi mới gắn với mục tiêu của tổ chức.</p>'
      }
    ]
  }
};

const programId = computed(() => {
  const param = route.params.id || route.path.split('/').pop();
  return param || 'mba';
});

const currentPost = ref(null);
const loading = ref(false);

const program = computed(() => {
  if (currentPost.value) return currentPost.value;
  if (courseStore.admissions && courseStore.admissions.length > 0) {
    const found = courseStore.admissions.find(p => p.slug === programId.value);
    if (found) return found;
  }
  return programsData[programId.value] || programsData['mba'];
});

const otherPrograms = computed(() => {
  if (courseStore.admissions && courseStore.admissions.length > 0) {
    return courseStore.admissions.filter(p => p.slug !== programId.value);
  }
  return Object.values(programsData).filter(p => p.id !== programId.value);
});

const loadAdmissionDetail = async () => {
  loading.value = true;
  try {
    // 1. Nạp tức thì từ store / cache nếu có
    if (courseStore.admissions && courseStore.admissions.length > 0) {
      const found = courseStore.admissions.find(p => p.slug === programId.value);
      if (found) currentPost.value = found;
    }
    // 2. Gọi API lấy bài viết thật mới nhất từ Database theo slug
    const post = await courseStore.fetchAdmissionBySlug(programId.value);
    if (post) {
      currentPost.value = post;
    }
    // 3. Đảm bảo danh sách các bài viết khác được nạp đủ từ Database
    if (!courseStore.admissions || courseStore.admissions.length === 0) {
      await courseStore.fetchAdmissions();
    }
  } catch (err) {
    console.error("Failed to load admission detail:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  window.scrollTo(0, 0);
  loadAdmissionDetail();
});

watch(programId, () => {
  window.scrollTo(0, 0);
  loadAdmissionDetail();
});
</script>

<style scoped src="@/styles/views/tuyen-sinh/AdmissionDetailView.css"></style>
