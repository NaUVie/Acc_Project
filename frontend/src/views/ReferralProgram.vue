<template>
  <div class="referral-page">
    <!-- Hero Section -->
    <section class="referral-hero">
      <div class="referral-container">
        <div class="hero-grid">
          <!-- Left Info -->
          <div class="hero-content">
            <div class="hero-badge">
              <span>🎁 Chương Trình Giới Thiệu Học Viên ACC</span>
            </div>
            <h1 class="hero-title">
              Biến lời giới thiệu thành phần thưởng: Mỗi lời giới thiệu đều mang lại giá trị
            </h1>
            <p class="hero-subtitle">
              Nhận đến <strong>29.000.000 VNĐ</strong> cho mỗi học viên bạn giới thiệu nhập học thành công. 
              Chia sẻ mã giới thiệu của bạn để bạn bè nhận ưu đãi học phí cao nhất – lên tới 
              <strong>14.500.000 VNĐ</strong> hoặc một khóa học miễn phí.
            </p>
          </div>

          <!-- Right Referral Card Widget -->
          <div class="hero-widget">
            <div class="ref-card">
              <div v-if="courseStore.token" class="logged-in-widget">
                <div class="ref-card-header">Mã giới thiệu độc quyền của bạn</div>
                <div class="ref-code-box">
                  <span class="code-value">{{ userReferralCode || 'ACC-VIP' }}</span>
                  <button class="btn-copy" @click="copyCode">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    {{ copiedCode ? 'Đã chép!' : 'Sao chép mã' }}
                  </button>
                </div>

                <div v-if="userStoreCredit > 0" class="ref-hint">
                  💰 Số dư Ví tích lũy hiện tại của bạn: {{ formatPrice(userStoreCredit) }}
                </div>

                <div class="social-share-btns">
                  <button class="btn-share zalo" @click="shareLink('zalo')">
                    💬 Chia sẻ Zalo
                  </button>
                  <button class="btn-share facebook" @click="shareLink('facebook')">
                    🌐 Facebook
                  </button>
                </div>
              </div>

              <div v-else class="login-cta-box">
                <h3 class="login-cta-title">Bạn chưa đăng nhập?</h3>
                <p class="login-cta-desc">
                  Đăng nhập hoặc đăng ký tài khoản ACC Academy ngay để lấy mã giới thiệu độc quyền và bắt đầu tích lũy thưởng.
                </p>
                <router-link to="/login" class="btn-login-cta">
                  Đăng nhập để nhận mã ngay &rarr;
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Benefits Section (Split Two Column Layout) -->
    <section class="benefits-section referral-container">
      <div class="benefits-header-bar">
        <div>
          <div class="benefits-subtitle-tag">Những lợi ích</div>
          <h2 class="benefits-main-title">Chương trình cụ thể <span>Những lợi ích</span></h2>
        </div>

        <!-- Enrollment Toggle Switch -->
        <div class="enrollment-toggle">
          <span 
            class="toggle-label" 
            :class="{ active: !isEnrolledFilter }" 
            @click="isEnrolledFilter = false"
          >
            Chưa đăng ký
          </span>
          <button 
            class="switch-btn" 
            :class="{ on: isEnrolledFilter }" 
            @click="isEnrolledFilter = !isEnrolledFilter"
            aria-label="Toggle enrollment status"
          >
            <span class="switch-circle"></span>
          </button>
          <span 
            class="toggle-label" 
            :class="{ active: isEnrolledFilter }" 
            @click="isEnrolledFilter = true"
          >
            Đã đăng ký
          </span>
        </div>
      </div>

      <!-- Split Layout Container -->
      <div class="benefits-split-container">
        <!-- Left Sidebar: Category List -->
        <div class="category-sidebar">
          <button 
            v-for="cat in categoriesList" 
            :key="cat.id" 
            class="cat-item-btn"
            :class="{ active: selectedCategory === cat.id }"
            @click="selectedCategory = cat.id"
          >
            <span>{{ cat.name }}</span>
            <span class="cat-arrow">&rsaquo;</span>
          </button>
        </div>

        <!-- Right Container: Scrollable Table -->
        <div class="rewards-table-wrapper">
          <table class="rewards-table">
            <thead>
              <tr>
                <th style="width: 50%;">Chương trình</th>
                <th style="width: 25%;">Kiếm tối đa</th>
                <th style="width: 25%;">Giới thiệu bạn bè của bạn</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredProgramList" :key="item.id">
                <td>
                  <div class="uni-logo-box">
                    <img :src="item.logo || '/images/default.jpg'" :alt="item.university" class="uni-logo" />
                    <div>
                      <div class="program-title-text">{{ item.programTitle }}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="max-earn-text">VND {{ formatPriceNumber(item.maxEarn) }}</div>
                </td>
                <td>
                  <a class="cta-link-brand" @click.prevent="handleActionClick(item)">
                    Tham khảo ngay ↗
                  </a>
                </td>
              </tr>
              <tr v-if="filteredProgramList.length === 0">
                <td colspan="3" style="text-align: center; color: #64748b; padding: 40px;">
                  Chưa có chương trình nào thuộc mục này.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- Testimonials / Referral Stories -->
    <section class="stories-section referral-container">
      <h2 class="section-title">Chia sẻ từ người giới thiệu</h2>
      <p class="section-subtitle">Lắng nghe cảm nhận thực tế từ các học viên & đối tác liên kết của ACC Academy</p>

      <div class="stories-grid">
        <div v-for="story in referralStories" :key="story.id" class="story-card">
          <div class="user-info">
            <img :src="story.avatar" :alt="story.name" class="user-avatar" />
            <div class="user-meta">
              <h4>{{ story.name }}</h4>
              <span>{{ story.role }}</span>
            </div>
          </div>
          <div class="reward-badge">🎉 Khấu trừ thành công: {{ story.earned }}</div>
          <p class="story-text">"{{ story.content }}"</p>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section referral-container">
      <h2 class="section-title">Câu hỏi thường gặp</h2>
      <p class="section-subtitle">Giải đáp toàn bộ thắc mắc về chương trình Giới thiệu và nhận hoàn tiền</p>

      <div class="faq-list">
        <div 
          v-for="(faq, idx) in faqItems" 
          :key="idx" 
          class="faq-item"
          :class="{ active: openFaqIndex === idx }"
        >
          <button class="faq-question" @click="toggleFaq(idx)">
            <span>{{ idx + 1 }}. {{ faq.q }}</span>
            <span class="faq-toggle-icon">{{ openFaqIndex === idx ? '−' : '+' }}</span>
          </button>
          <div v-show="openFaqIndex === idx" class="faq-answer">
            <p>{{ faq.a }}</p>
          </div>
        </div>
      </div>

      <!-- Support & Legal Disclaimer -->
      <div class="support-box">
        <h3 class="support-title">Hỗ trợ chương trình Giới thiệu của ACC Academy</h3>
        <p style="color: #64748b; margin-bottom: 8px;">Nếu bạn có bất kỳ thắc mắc nào, vui lòng liên hệ bộ phận hỗ trợ khách hàng của chúng tôi:</p>
        <a href="mailto:referral@accacademy.vn" class="support-email">📧 referral@accacademy.vn</a>

        <div class="disclaimer-text">
          <strong>Tuyên bố miễn trừ trách nhiệm:</strong> ACC Academy cung cấp nền tảng học tập và chứng nhận năng lực thực chiến. Tiền thưởng giới thiệu sẽ được cộng trực tiếp vào Ví tài khoản cá nhân để trừ trực tiếp vào các học phí tiếp theo hoặc rút về tài khoản ngân hàng khi đáp ứng đủ tiêu chí theo đúng điều khoản chương trình. Khả năng thành công và mức thu nhập phụ thuộc vào sự đóng góp và nỗ lực cá nhân của người giới thiệu.
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { useRouter } from 'vue-router';

const courseStore = useCourseStore();
const router = useRouter();

const copiedCode = ref(false);
const isEnrolledFilter = ref(false);
const selectedCategory = ref('all');
const openFaqIndex = ref(0);

const userReferralCode = computed(() => courseStore.userMe?.referralCode || '');
const userStoreCredit = computed(() => courseStore.userMe?.storeCreditBalance || 0);

const copyCode = () => {
  const code = userReferralCode.value || 'ACC-VIP';
  navigator.clipboard.writeText(code);
  copiedCode.value = true;
  courseStore.showToast('Đã sao chép mã giới thiệu vào bộ nhớ tạm!', 'success');
  setTimeout(() => { copiedCode.value = false; }, 2000);
};

const shareLink = (platform) => {
  const code = userReferralCode.value || 'ACC-VIP';
  const port = window.location.port ? `:${window.location.port}` : '';
  const refUrl = `${window.location.protocol}//${window.location.hostname}${port}/register?ref=${code}`;
  
  if (platform === 'zalo') {
    window.open(`https://zalo.me/share?url=${encodeURIComponent(refUrl)}`, '_blank');
  } else if (platform === 'facebook') {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(refUrl)}`, '_blank');
  }
};

const formatPrice = (val) => {
  if (!val) return '0 VNĐ';
  return val.toLocaleString('vi-VN') + ' VNĐ';
};

const formatPriceNumber = (val) => {
  if (!val) return '0';
  return val.toLocaleString('vi-VN');
};

// Sidebar Categories List
const categoriesList = [
  { id: 'all', name: 'Tất cả sản phẩm' },
  { id: 'program', name: 'Chương trình đào tạo' },
  { id: 'course', name: 'Khóa học lẻ' },
  { id: 'bundle', name: 'Gói Combo' },
  { id: 'ai', name: 'Kỹ năng AI' },
  { id: 'chuyen-mon', name: 'Kỹ năng chuyên môn' },
  { id: 'mem', name: 'Kỹ năng mềm' }
];

// Dynamic Master Datasets (100% Real Database Items)
const masterRewardsList = computed(() => {
  const items = [];

  // 1. Map Master Programs from Database
  if (courseStore.programs && courseStore.programs.length > 0) {
    courseStore.programs.forEach(prog => {
      const childCourses = courseStore.courses.filter(c => c.programId === prog.id);
      const totalPrice = childCourses.reduce((sum, c) => sum + (c.price || 0), 0);
      const maxEarn = totalPrice > 0 ? Math.round(totalPrice * 0.15) : 0;
      
      const targetLink = childCourses.length > 0 && childCourses[0].handle 
        ? `/course/${childCourses[0].handle}` 
        : '/courses/category/ky-nang-ai';

      items.push({
        id: `prog-${prog.id}`,
        university: 'ACC Master Program',
        logo: prog.image || '/images/logo3.png',
        programTitle: prog.title,
        type: 'program',
        category: 'chuyen-mon',
        maxEarn: maxEarn,
        link: targetLink
      });
    });
  }

  // 2. Map Catalog Courses from Database
  if (courseStore.courses && courseStore.courses.length > 0) {
    courseStore.courses.forEach(c => {
      const commPct = c.defaultCommissionPercent || 10;
      const maxEarn = Math.round((c.price || 0) * (commPct / 100));

      let catKey = 'ai';
      if (c.category === 'ky-nang-chuyen-mon') catKey = 'chuyen-mon';
      if (c.category === 'ky-nang-mem') catKey = 'mem';

      items.push({
        id: `course-${c.id}`,
        university: 'ACC Academy',
        logo: c.image || '/images/logo3.png',
        programTitle: c.title,
        type: 'course',
        category: catKey,
        maxEarn: maxEarn,
        link: `/course/${c.handle || c.id}`
      });
    });
  }

  // 3. Map Bundles from Database
  if (courseStore.bundles && courseStore.bundles.length > 0) {
    courseStore.bundles.forEach(b => {
      const maxEarn = Math.round((b.price || 0) * 0.12);
      items.push({
        id: `bundle-${b.id}`,
        university: 'ACC Combo Package',
        logo: b.image || '/images/logo3.png',
        programTitle: b.title,
        type: 'bundle',
        category: 'bundle',
        maxEarn: maxEarn,
        link: '/bundles'
      });
    });
  }

  return items;
});

const filteredProgramList = computed(() => {
  if (selectedCategory.value === 'all') {
    return masterRewardsList.value;
  }
  return masterRewardsList.value.filter(item => {
    return item.type === selectedCategory.value || item.category === selectedCategory.value;
  });
});

const handleActionClick = (item) => {
  if (item && item.link) {
    router.push(item.link);
  } else {
    router.push('/courses/category/ky-nang-ai');
  }
};

// Testimonials Data
const referralStories = [
  {
    id: 1,
    name: 'Nguyễn Thanh Tùng',
    role: 'CEO & Founder TechAsia',
    avatar: 'https://i.pravatar.cc/150?img=11',
    earned: '35.000.000 VNĐ',
    content: 'Sau khi giới thiệu đồng nghiệp đăng ký khóa Tiến sĩ Generative AI, mình nhận ngay thưởng vào Ví ACC và dùng số tiền này để tài trợ khóa học AI for Team cho toàn bộ dàn quản lý của công ty!'
  },
  {
    id: 2,
    name: 'Trần Thị Mai Anh',
    role: 'Giám đốc Nhân sự (CHRO)',
    avatar: 'https://i.pravatar.cc/150?img=5',
    earned: '20.000.000 VNĐ',
    content: 'Chương trình giới thiệu rất minh bạch. Bạn bè mình khi nhập mã ref còn được hỗ trợ giảm trực tiếp 10% học phí, cả hai bên đều nhận được giá trị tuyệt vời.'
  },
  {
    id: 3,
    name: 'Phạm Đức Huy',
    role: 'Quản lý Dự án Senior',
    avatar: 'https://i.pravatar.cc/150?img=12',
    earned: '12.500.000 VNĐ',
    content: 'Chỉ cần chia sẻ link ref trên LinkedIn, các bạn đồng nghiệp cũ đăng ký là hệ thống tự động ghi nhận hoa hồng. Quy trình rút tiền và đối soát rất linh hoạt!'
  }
];

// FAQ Accordions Data
const faqItems = [
  {
    q: 'Điều kiện nào để nhận hoàn tiền sau khi giới thiệu bạn bè?',
    a: 'Bạn bè của bạn cần đăng ký tài khoản qua đường link giới thiệu của bạn (hoặc nhập Mã giới thiệu của bạn trong bước Đăng ký/Thanh toán) và hoàn tất thanh toán đơn hàng khóa học hợp lệ.'
  },
  {
    q: 'Khi nào tôi sẽ nhận được khoản hoàn tiền giới thiệu?',
    a: 'Tiền thưởng sẽ tự động được cộng vào Ví tài khoản Ví Store Credit của bạn ngay sau khi đơn hàng của người được giới thiệu chuyển sang trạng thái Đã thanh toán (Paid).'
  },
  {
    q: '“Người dùng chưa ghi danh” là ai?',
    a: 'Là những người dùng mới tạo tài khoản nhưng chưa từng đăng ký hoặc thanh toán bất kỳ khóa học nào trên hệ thống ACC Academy.'
  },
  {
    q: '“Người dùng đã ghi danh” là ai?',
    a: 'Là các học viên đã và đang tham gia ít nhất 01 khóa học tại ACC Academy.'
  },
  {
    q: 'Nếu bạn tôi quên nhập mã giới thiệu thì sao?',
    a: 'Đừng lo lắng! Hãy gửi email tới referral@accacademy.vn kèm Email tài khoản của bạn và bạn bè trong vòng 48h kể từ khi thanh toán, ban quản trị sẽ kiểm tra và đối soát thủ công giúp bạn.'
  }
];

const toggleFaq = (idx) => {
  openFaqIndex.value = openFaqIndex.value === idx ? -1 : idx;
};

onMounted(async () => {
  try {
    const tasks = [];
    if (courseStore.courses.length === 0) {
      tasks.push(courseStore.fetchCourses());
    }
    if (courseStore.programs.length === 0) {
      tasks.push(courseStore.fetchPrograms());
    }
    if (courseStore.token && !courseStore.userMe) {
      tasks.push(courseStore.fetchUserMe());
    }
    if (tasks.length > 0) {
      await Promise.all(tasks);
    }
  } catch (err) {
    console.error('Failed to load data for ReferralProgram page:', err);
  }
});
</script>

<style scoped src="@/styles/views/ReferralProgram.css"></style>
