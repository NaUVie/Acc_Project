<template>
  <footer class="custom-footer">
    <div class="custom-footer-container">
      <div class="custom-footer-top">
        <!-- Col 1: Brand -->
        <div class="custom-footer-col brand-col">
          <router-link to="/" class="custom-footer-logo" aria-label="Trang chủ ACC Academy">
            <img src="/images/logo3.png" alt="ACC Academy" class="footer-logo-img" loading="lazy">
          </router-link>
          <p class="custom-footer-slogan">
            Học viện đào tạo thực chiến về Quản trị, Năng lực số và Ứng dụng AI cho cá nhân &amp; doanh nghiệp.
          </p>
        </div>

        <!-- Col 2: Đào tạo -->
        <div class="custom-footer-col">
          <h4 class="custom-footer-heading">Đào tạo</h4>
          <ul class="custom-footer-linklist">
            <li><router-link to="/courses/category/dao-tao-ca-nhan">Khóa học cá nhân</router-link></li>
            <li><router-link to="/courses/category/dao-tao-doanh-nghiep">Đào tạo doanh nghiệp</router-link></li>
            <li><router-link to="/tuyen-sinh">Tuyển sinh MBA Andrews</router-link></li>
          </ul>
        </div>

        <!-- Col 3: Về ACC -->
        <div class="custom-footer-col">
          <h4 class="custom-footer-heading">Về ACC</h4>
          <ul class="custom-footer-linklist">
            <li><router-link to="/about-us">Giới thiệu</router-link></li>
            <li><router-link to="/doi-ngu-giang-vien">Đội ngũ giảng viên</router-link></li>
            <li><router-link to="/library/blog">Tin tức &amp; Bài viết</router-link></li>
            <li><router-link to="/contact">Liên hệ tư vấn</router-link></li>
          </ul>
        </div>

        <!-- Col 4: Liên hệ & QR Zalo -->
        <div class="custom-footer-col contact-col">
          <h4 class="custom-footer-heading">Liên hệ</h4>
          <div class="contact-details">
            <p class="contact-row">
              <span class="contact-label">Địa chỉ:</span>
              <span>156 Nam Kỳ Khởi Nghĩa, Quận 1, TP. HCM</span>
            </p>
            <p class="contact-row">
              <span class="contact-label">Hotline:</span>
              <a href="tel:0938566700">0938 566 700</a>
            </p>
            <p class="contact-row">
              <span class="contact-label">Email:</span>
              <a href="mailto:info@acc-edu.vn">info@acc-edu.vn</a>
            </p>
          </div>

          <div class="footer-qr-zalo">
            <div class="qr-zalo-img-wrapper">
              <img src="/images/QR_Zalo.jpg" alt="QR Zalo ACC Academy" class="qr-zalo-img" loading="lazy" />
            </div>
            <div class="qr-zalo-info">
              <span class="qr-zalo-title">Kết nối Zalo OA</span>
              <span class="qr-zalo-desc">Quét mã QR để được hỗ trợ &amp; tư vấn nhanh nhất</span>
            </div>
          </div>
        </div>
      </div>

      <div class="custom-footer-bottom">
        <p class="copyright-text">
          &copy; 2026 ACC Academy. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped src="@/styles/components/Footer.css"></style>
