<template>
  <div class="about-us-page">
    <!-- Hero Section with ACC Slogan -->
    <section class="about-hero-section reveal-on-scroll">
      <div class="container">
        <h1 class="hero-slogan-title">
          <span class="slogan-part">CONNECT TO LEARN</span>
          <span class="slogan-space"> </span>
          <span class="slogan-part">– LEARN TO LEAD</span>
        </h1>
        <p class="hero-subtext">
          <span class="subtext-line subtext-line-1">{{ $t('about.subtext1') }}</span>
          <span class="subtext-line subtext-line-2">{{ $t('about.subtext2') }}</span>
        </p>
      </div>
    </section>

    <!-- Vision & Mission + ACC Difference (Clean Minimalist Slide Style) -->
    <section class="vision-mission-section reveal-on-scroll">
      <div class="container">
        <div class="vm-banner-card">
          <!-- Left Media: Photo with people -->
          <div class="vm-bg-media">
            <img src="/images/TamNhinSuMenh.jpg" alt="Tầm nhìn & Sứ mệnh ACC" class="vm-bg-img" loading="lazy" decoding="async" />
            <div class="vm-gradient-overlay"></div>
          </div>

          <!-- Right Content: 2 Columns side-by-side matching reference image -->
          <div class="vm-inner-content">
            <div class="vm-columns-grid">
              <!-- Column 1: Logo ACC + Tầm nhìn & Sứ mệnh -->
              <div class="vm-col">
                <div class="vm-brand-top">
                  <img src="/images/logo3.png" alt="ACC Kết Nối Tri Thức" class="vm-acc-logo" />
                </div>
                <span class="vm-tag">{{ $t('about.tagOrientation') }}</span>
                <h3 class="vm-title">{{ $t('about.visionTitle') }}</h3>
                <p class="vm-text">
                  {{ $t('about.visionText') }}
                </p>
              </div>

              <!-- Column 2: Sự khác biệt của ACC (aligned with Column 1) -->
              <div class="vm-col">
                <div class="vm-brand-spacer" aria-hidden="true"></div>
                <span class="vm-tag">{{ $t('about.tagPractical') }}</span>
                <h3 class="vm-title">{{ $t('about.diffTitle') }}</h3>
                <p class="vm-text">
                  {{ $t('about.diffText') }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Core Values Section (A - C - C) - Open Minimalist Grid -->
    <section class="core-values-section">
      <div class="container">
        <div class="section-title-box reveal-on-scroll">
          <h2 class="section-title">{{ $t('about.coreValuesTitle') }}</h2>
          <p class="section-subtitle">{{ $t('about.coreValuesSubtitle') }}</p>
        </div>

        <div class="values-open-grid">
          <!-- A - Awareness -->
          <div class="value-item reveal-on-scroll" style="--reveal-delay: 0.1s;">
            <div class="value-header">
              <span class="value-letter">A</span>
              <div class="value-title-group">
                <h3 class="value-name">{{ $t('about.valueA') }}</h3>
                <p class="value-tagline">{{ $t('about.valueATagline') }}</p>
              </div>
            </div>
            <p class="value-desc">{{ $t('about.valueADesc') }}</p>

            <div class="action-box">
              <h4 class="action-title">{{ $t('about.actionTitle') }}</h4>
              <ul class="action-list">
                <li v-for="(item, i) in $tm('about.valueAActions')" :key="i">{{ $rt(item) }}</li>
              </ul>
            </div>
          </div>

          <!-- C - Connection -->
          <div class="value-item reveal-on-scroll" style="--reveal-delay: 0.25s;">
            <div class="value-header">
              <span class="value-letter">C</span>
              <div class="value-title-group">
                <h3 class="value-name">{{ $t('about.valueC1') }}</h3>
                <p class="value-tagline">{{ $t('about.valueC1Tagline') }}</p>
              </div>
            </div>
            <p class="value-desc">{{ $t('about.valueC1Desc') }}</p>

            <div class="action-box">
              <h4 class="action-title">{{ $t('about.actionTitle') }}</h4>
              <ul class="action-list">
                <li v-for="(item, i) in $tm('about.valueC1Actions')" :key="i">{{ $rt(item) }}</li>
              </ul>
            </div>
          </div>

          <!-- C - Change -->
          <div class="value-item reveal-on-scroll" style="--reveal-delay: 0.4s;">
            <div class="value-header">
              <span class="value-letter">C</span>
              <div class="value-title-group">
                <h3 class="value-name">{{ $t('about.valueChange') }}</h3>
                <p class="value-tagline">{{ $t('about.valueChangeTagline') }}</p>
              </div>
            </div>
            <p class="value-desc">{{ $t('about.valueChangeDesc') }}</p>

            <div class="action-box">
              <h4 class="action-title">{{ $t('about.actionTitle') }}</h4>
              <ul class="action-list">
                <li v-for="(item, i) in $tm('about.valueChangeActions')" :key="i">{{ $rt(item) }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Two Core Functions Section -->
    <section class="core-functions-section">
      <div class="container">
        <div class="manifesto-clean-box reveal-on-scroll">
          <h2 class="manifesto-title">{{ $t('about.coreFunctionsTitle') }}</h2>
          <blockquote class="manifesto-quote">
            "{{ $t('about.manifestoQuote1') }}<br />
            {{ $t('about.manifestoQuote2') }}<br />
            <strong>{{ $t('about.manifestoQuoteStrong') }}</strong>"
          </blockquote>
        </div>

        <div class="functions-open-grid">
          <div class="function-item reveal-on-scroll" style="--reveal-delay: 0.1s;">
            <span class="func-tag">{{ $t('about.func1Tag') }}</span>
            <h3 class="func-title">{{ $t('about.func1Title') }}</h3>
            <p class="func-desc">{{ $t('about.func1Desc') }}</p>
          </div>

          <div class="function-item reveal-on-scroll" style="--reveal-delay: 0.25s;">
            <span class="func-tag alt">{{ $t('about.func2Tag') }}</span>
            <h3 class="func-title">{{ $t('about.func2Title') }}</h3>
            <p class="func-desc">{{ $t('about.func2Desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Why ACC x Andrews Section -->
    <section class="why-andrews-section">
      <div class="container">
        <div class="section-title-box reveal-on-scroll">
          <h2 class="section-title">{{ $t('about.whyTitle') }}</h2>
        </div>

        <div class="andrews-clean-grid">
          <div class="andrews-item reveal-on-scroll" style="--reveal-delay: 0.1s;">
            <div class="card-num">01</div>
            <h3>{{ $t('about.why1Title') }}</h3>
            <p>{{ $t('about.why1Desc') }}</p>
          </div>

          <div class="andrews-item reveal-on-scroll" style="--reveal-delay: 0.2s;">
            <div class="card-num">02</div>
            <h3>{{ $t('about.why2Title') }}</h3>
            <p>{{ $t('about.why2Desc') }}</p>
          </div>

          <div class="andrews-item reveal-on-scroll" style="--reveal-delay: 0.3s;">
            <div class="card-num">03</div>
            <h3>{{ $t('about.why3Title') }}</h3>
            <p>{{ $t('about.why3Desc') }}</p>
          </div>

          <div class="andrews-item reveal-on-scroll" style="--reveal-delay: 0.4s;">
            <div class="card-num">04</div>
            <h3>{{ $t('about.why4Title') }}</h3>
            <p>{{ $t('about.why4Desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Leadership & Board of Executives Section -->
    <section class="leadership-section">
      <div class="container">
        <div class="section-title-box reveal-on-scroll">
          <h2 class="section-title">{{ $t('about.leadershipTitle') }}</h2>
          <p class="section-subtitle">{{ $t('about.leadershipSubtitle') }}</p>
        </div>

        <div class="leadership-rows-wrapper">
          <div 
            v-for="(row, rIdx) in boardRows" 
            :key="rIdx"
            class="leadership-grid"
            :class="`grid-cols-${boardColumns}`"
            :style="{ '--board-cols': boardColumns }"
          >
            <div 
              v-for="(member, idx) in row" 
              :key="member.id || `${rIdx}-${idx}`" 
              class="leader-card reveal-on-scroll"
              :style="{ '--reveal-delay': `${(idx % 5) * 0.1}s` }"
            >
              <div class="leader-avatar-wrapper">
                <img 
                  :src="member.avatar || '/images/1_6.png'" 
                  :alt="member.name" 
                  class="leader-avatar" loading="lazy" decoding="async" width="280" height="280"
                  @error="(e) => e.target.src = '/images/1_6.png'"
                  referrerpolicy="no-referrer"
                />
              </div>
              <div class="leader-info">
                <h3 class="leader-name">{{ member.name }}</h3>
                <p class="leader-main-role">{{ member.main_role || member.mainRole }}</p>
                <ul class="leader-bio-list">
                  <li v-for="(bio, bIdx) in parseBioList(member)" :key="bIdx">{{ bio }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
let scrollObserver = null;

onMounted(() => {
  if (!courseStore.contactSettings) {
    courseStore.fetchContactSettings().catch(() => {});
  }
  courseStore.fetchBoardMembers().catch(() => {}).finally(() => {
    nextTick(() => {
      if (scrollObserver) {
        document.querySelectorAll('.reveal-on-scroll').forEach(el => scrollObserver.observe(el));
      }
    });
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Scroll reveal animation observer
  scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal-on-scroll').forEach(el => scrollObserver.observe(el));
});

onUnmounted(() => {
  if (scrollObserver) {
    scrollObserver.disconnect();
    scrollObserver = null;
  }
});

const parseBioList = (member) => {
  if (Array.isArray(member.bioList)) return member.bioList;
  if (Array.isArray(member.bio_list)) return member.bio_list;
  if (typeof member.bio_list === 'string') {
    try {
      const parsed = JSON.parse(member.bio_list);
      if (Array.isArray(parsed)) return parsed;
    } catch {
      return member.bio_list.split('\n').map(s => s.trim()).filter(Boolean);
    }
  }
  return [];
};

const displayedBoardMembers = computed(() => {
  if (courseStore.boardMembers && courseStore.boardMembers.length > 0) {
    return [...courseStore.boardMembers].sort((a, b) => (Number(a.position) || 0) - (Number(b.position) || 0));
  }
  return defaultBoardMembers;
});

const boardColumns = computed(() => {
  const custom = Number(courseStore.contactSettings?.board_columns_desktop) 
    || Number(localStorage.getItem('acc_board_cols_cache'));
  if (custom) return custom;
  // Nếu có từ 9 người trở lên và chưa lưu cấu hình riêng thì mặc định 5 cột (để xếp 4 người trên, 5 người dưới)
  if (displayedBoardMembers.value && displayedBoardMembers.value.length >= 9) {
    return 5;
  }
  return 4;
});

const boardRows = computed(() => {
  const list = displayedBoardMembers.value;
  const cols = boardColumns.value;
  if (!list || list.length === 0) return [];
  if (list.length <= cols) return [list];

  const remainder = list.length % cols;
  if (remainder > 0) {
    const rows = [];
    // Hàng trên cùng chứa nhóm ít người hơn (phần dư) để xếp tầng kim tự tháp (ví dụ 9 người: 4 người hàng 1, 5 người hàng 2)
    rows.push(list.slice(0, remainder));
    for (let i = remainder; i < list.length; i += cols) {
      rows.push(list.slice(i, i + cols));
    }
    return rows;
  }

  const rows = [];
  for (let i = 0; i < list.length; i += cols) {
    rows.push(list.slice(i, i + cols));
  }
  return rows;
});

const defaultBoardMembers = [
  {
    name: 'Ông Nguyễn Tiến Điệp',
    mainRole: 'Chủ tịch HĐQT Công ty CP Kết Nối Tri Thức ACC',
    avatar: '/images/VeChungToi/TienDiep.webp',
    bioList: [
      'CEO Sadaco Tas',
      'Chủ tịch HĐQT CTY CP Tập đoàn Sài Gòn Tiến Đoàn',
      'Chủ tịch Alumni Andrews Việt Nam',
      'Thạc sĩ QTKD Đại học Andrews (Hoa Kỳ)'
    ]
  },
  {
    name: 'Ông Ngô Trí Thủy',
    mainRole: 'Tổng Giám đốc Công ty CP Kết Nối Tri Thức ACC',
    avatar: '/images/VeChungToi/NgoTriThuy.webp',
    bioList: [
      'Thành viên sáng lập - Phó Chủ tịch HĐQT Imap Logistics',
      'Thành viên sáng lập – Thành viên HĐQT Icom Trading',
      'Phó Chủ tịch Hội Doanh nhân Trẻ TPHCM (Chi Hội Chợ Lớn)',
      'Nguyên Giám đốc Marketing và Phát triển Sản phẩm các Ngân hàng'
    ]
  },
  {
    name: 'Bà Nguyễn Thị Thu Hoà',
    mainRole: 'Thành viên Hội Đồng Quản Trị ACC',
    avatar: '/images/VeChungToi/ThuHoa.webp',
    bioList: [
      'Tổng Giám Đốc của ADP Group',
      'Nguyên Giám Đốc Marketing của Tập Đội BĐS Khang Điền',
      'Quyền Giám Đốc Nhãn Hàng Tập Đoàn Cà phê Trung Nguyên'
    ]
  },
  {
    name: 'Ông Lê Nguyễn Ngọc Sơn',
    mainRole: 'Thành viên HĐQT Công ty CP Kết nối Tri thức ACC',
    avatar: '/images/VeChungToi/Ngocson.webp',
    bioList: [
      'Giám Đốc Andrews Alumni Việt Nam',
      'Phó Giám Đốc Phát Triển Đại Học Andrews Hoa Kỳ tại Việt Nam'
    ]
  },
  {
    name: 'TS. Nguyễn Tấn Bình',
    mainRole: 'Cố vấn Cao cấp Công ty CP Kết nối Tri thức ACC',
    avatar: '/images/VeChungToi/ThayBinh.webp',
    bioList: [
      'Viện trưởng Viện nghiên cứu Khoa học Lãnh đạo & Quản trị Doanh nghiệp – Leadman',
      'Giảng viên cao cấp Andrews University Hoa Kỳ tại Việt Nam',
      'Giảng viên thỉnh giảng chương trình Fulbright',
      'Giảng viên cao cấp, tác giả nhiều sách về Tài chính - Kế toán'
    ]
  },
  {
    name: 'Bà Nguyễn Thị Kim Anh',
    mainRole: 'Cố vấn Cao cấp Công ty CP Kết nối Tri thức ACC',
    avatar: '/images/VeChungToi/KimAnh.webp',
    bioList: [
      'Thạc sĩ Quản trị Kinh doanh, Andrews University, Hoa Kỳ',
      'Chủ tịch HĐQT Hệ thống Trường Việt Anh',
      'Quản lý chuỗi hệ thống 10 trường từ hệ Mầm non đến Trung học Phổ thông chuẩn quốc tế'
    ]
  },
  {
    name: 'Bà Nguyễn Thị Mỹ Dung',
    mainRole: 'Co-Founder Công ty CP Kết nối Tri thức ACC',
    avatar: '/images/VeChungToi/MYDUNG.webp',
    bioList: [
      'Nguyên Giám đốc chi nhánh Techcombank',
      'Thạc sĩ QTKD trường Đại học Andrews (ĐH Quốc tế, ĐHQG Tp.HCM)',
      'Giảng viên Đại học'
    ]
  },
  {
    name: 'Bà Ngô Vũ Ngọc Thảo',
    mainRole: 'Co-Founder Công ty CP Kết nối Tri thức ACC',
    avatar: '/images/VeChungToi/NgocThao.webp',
    bioList: [
      'Trưởng phòng Cao cấp Tập đoàn L’Oreal Việt Nam',
      'Trưởng ban Học Thuật – Trường ĐH Andrews (ĐH Quốc tế - ĐHQG Tp.HCM)',
      'Giảng viên Đại học & Thạc sĩ QTKD Đại học Andrews'
    ]
  }
];
</script>

<style scoped src="@/styles/views/AboutUs.css"></style>
