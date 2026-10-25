<template>
  <footer class="custom-footer">
    <div class="custom-footer-container">
      <div class="custom-footer-top">
        <!-- Col 1: Brand & Doanh nghiệp -->
        <div class="custom-footer-col brand-col">
          <router-link to="/" class="custom-footer-logo" aria-label="Trang chủ ACC Academy">
            <img src="/images/logo3.png" alt="ACC Academy" class="footer-logo-img" loading="lazy">
          </router-link>
          <p class="custom-footer-company">
            <strong>CÔNG TY CỔ PHẦN KẾT NỐI TRI THỨC ACC</strong>
          </p>
          <p class="custom-footer-slogan">
            Học viện đào tạo thực chiến về Quản trị, Năng lực số và Ứng dụng AI cho cá nhân &amp; doanh nghiệp.
          </p>
          <div class="contact-compact-list">
            <div class="compact-row">
              <span class="compact-label">Địa chỉ:</span>
              <span class="compact-text">{{ contactInfo.address }}</span>
            </div>
            <div class="compact-row">
              <span class="compact-label">Hotline:</span>
              <span class="compact-text"><a :href="'tel:' + rawPhone">{{ contactInfo.hotline }}</a></span>
            </div>
            <div class="compact-row">
              <span class="compact-label">Email:</span>
              <span class="compact-text"><a :href="'mailto:' + contactInfo.email">{{ contactInfo.email }}</a></span>
            </div>
          </div>
        </div>

        <!-- Col 2: Về ACC & Đào tạo -->
        <div class="custom-footer-col nav-col">
          <h4 class="custom-footer-heading">Chương trình Đào tạo</h4>
          <ul class="custom-footer-linklist">
            <li><router-link to="/courses/category/dao-tao-ca-nhan">Khóa học cá nhân</router-link></li>
            <li><router-link to="/courses/category/dao-tao-doanh-nghiep">Đào tạo Doanh nghiệp Inhouse</router-link></li>
            <li><router-link to="/tuyen-sinh">Chương trình Thạc sĩ MBA Andrews</router-link></li>
            <li><router-link to="/bundles">Gói Combo Khóa học Ưu đãi</router-link></li>
            <li><router-link to="/doi-ngu-giang-vien">Đội ngũ Giảng viên & Chuyên gia</router-link></li>
          </ul>
        </div>

        <!-- Col 3: Chính sách & Pháp lý (Chuẩn VNPAY) -->
        <div class="custom-footer-col nav-col">
          <h4 class="custom-footer-heading">Chính sách & Quy định</h4>
          <ul class="custom-footer-linklist">
            <li><router-link to="/terms-of-service">Điều khoản dịch vụ</router-link></li>
            <li><router-link to="/privacy-policy">Chính sách bảo mật thông tin</router-link></li>
            <li><router-link to="/refund-policy">Chính sách hoàn tiền & Đổi khóa</router-link></li>
            <li><router-link to="/payment-guide">Hướng dẫn thanh toán (VNPAY)</router-link></li>
            <li><router-link to="/delivery-policy">Truy cập & Giao nhận khóa học</router-link></li>
          </ul>
        </div>

        <!-- Col 4: Kết nối Zalo OA & Hỗ trợ -->
        <div class="custom-footer-col connect-col">
          <h4 class="custom-footer-heading">Hỗ trợ Học viên</h4>
          
          <div class="footer-qr-zalo">
            <div class="qr-zalo-img-wrapper">
              <img src="/images/QR_Zalo.jpg" alt="QR Zalo ACC Academy" class="qr-zalo-img" loading="lazy" />
            </div>
            <div class="qr-zalo-info">
              <span class="qr-zalo-title">Zalo Official Account</span>
              <span class="qr-zalo-desc">Hỗ trợ 24/7 trực tuyến</span>
              <a :href="contactInfo.zalo" target="_blank" rel="noopener" class="btn-chat-zalo">Chat Zalo ngay &rarr;</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="custom-footer-bottom">
        <p class="copyright-text">
          &copy; 2026 <strong>ACC Academy</strong>. Bản quyền thuộc về Công ty Cổ phần Kết nối Tri thức ACC.
        </p>
        <div class="footer-bottom-links">
          <router-link to="/privacy-policy">Bảo mật</router-link>
          <span class="dot">•</span>
          <router-link to="/terms-of-service">Điều khoản</router-link>
          <span class="dot">•</span>
          <router-link to="/contact">Liên hệ</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

onMounted(() => {
  if (!courseStore.contactSettings) {
    courseStore.fetchContactSettings();
  }
});

const contactInfo = computed(() => {
  const s = courseStore.contactSettings;
  return {
    address: s?.address || '156 Nam Kỳ Khởi Nghĩa, Phường Bến Nghé, Quận 1, TP. HCM',
    hotline: s?.hotline || '0938 566 700',
    email: s?.email || 'info@acc-edu.vn',
    zalo: s?.zalo || 'https://zalo.me/0938566700'
  };
});

const rawPhone = computed(() => {
  return contactInfo.value.hotline.replace(/\s+/g, '');
});
</script>

<style scoped src="@/styles/components/Footer.css"></style>
