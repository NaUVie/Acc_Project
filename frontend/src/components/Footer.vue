<template>
  <footer class="custom-footer">
    <div class="custom-footer-container">
      <div class="custom-footer-top">
        <!-- Col 1: Brand & Social -->
        <div class="custom-footer-col">
          <router-link to="/" class="custom-footer-logo">
            <img src="/images/logo3.png" alt="ACC Academy" style="max-height: 40px; width: auto; filter: brightness(0) invert(1);" loading="lazy">
          </router-link>
          <p class="custom-footer-slogan">
            Hệ thống đào tạo trực tuyến nâng cao năng lực thực chiến, kỹ năng quản trị và ứng dụng công nghệ AI hàng đầu cho cá nhân & doanh nghiệp.
          </p>
          <div class="custom-footer-socials mt-3">
            <ul>
              <li>
                <a href="https://www.facebook.com/skillsbridgevn" target="_blank" rel="noopener" aria-label="Facebook">
                  <svg width="22" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H7.5v-3H10V9.69c0-2.47 1.47-3.83 3.72-3.83 1.08 0 2.21.19 2.21.19v2.43h-1.25c-1.23 0-1.61.76-1.61 1.54V12h2.74l-.44 3h-2.3v6.8c4.56-.93 8-4.96 8-9.8z"/></svg>
                </a>
              </li>
              <li>
                <a href="https://www.tiktok.com/@skillsbridgevn" target="_blank" rel="noopener" aria-label="TikTok">
                  <svg width="22" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 1 1-5.2-1.74 2.89 2.89 0 0 1 2.31-2.22V8.2a6.34 6.34 0 0 0-5.11 6.2 6.34 6.34 0 1 0 11.45-3.8v-4.5a8.27 8.27 0 0 0 3.77.94v-3.35z"/></svg>
                </a>
              </li>
              <li>
                <a href="https://www.linkedin.com/company/skillsbridgevn/" target="_blank" rel="noopener" aria-label="LinkedIn">
                  <svg width="22" height="22" viewBox="0 0 24 24"><path fill="currentColor" d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Col 2: Navigation -->
        <div class="custom-footer-col">
          <h3 class="custom-footer-heading">Khám phá</h3>
          <ul class="custom-footer-linklist">
            <li><router-link to="/about-us">Về ACC Academy</router-link></li>
            <li><router-link to="/courses/ai">Khóa học AI & Tự động hóa</router-link></li>
            <li><router-link to="/corporate/dao-tao">Đào tạo Doanh nghiệp</router-link></li>
            <li><router-link to="/library/blog">Bài viết chuyên gia</router-link></li>
          </ul>
        </div>

        <!-- Col 3: Policy -->
        <div class="custom-footer-col">
          <h3 class="custom-footer-heading">Chính sách</h3>
          <ul class="custom-footer-linklist">
            <li><router-link to="/">Điều khoản sử dụng</router-link></li>
            <li><router-link to="/">Chính sách bảo mật</router-link></li>
            <li><router-link to="/">Quy định thanh toán & xuất VAT</router-link></li>
          </ul>
        </div>

        <!-- Col 4: Contact -->
        <div class="custom-footer-col">
          <h3 class="custom-footer-heading">Liên hệ</h3>
          <div class="custom-footer-contact-info">
            <p><strong>Hotline:</strong> 090 977 0085</p>
            <p><strong>Email:</strong> support@accacademy.vn</p>
            <p><strong>Địa chỉ:</strong> Tòa nhà Fideco, 14 Thảo Điền, TP. Thủ Đức, TP. HCM</p>
            <p><strong>MST:</strong> 0317402205</p>
          </div>
        </div>
      </div>

      <div class="custom-footer-bottom">
        <div class="custom-footer-copyright">
          © 2026 ACC Academy. Tất cả quyền được bảo lưu.
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped src="@/styles/components/Footer.css"></style>
