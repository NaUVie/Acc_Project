<template>
  <footer class="custom-footer">
    <div class="custom-footer-container">
      <div class="custom-footer-top">
        <div class="custom-footer-col">
          <router-link to="/" class="custom-footer-logo" style="max-width: 100px;">
            <img src="/fonts/SB_White.svg" alt="ACC Academy" srcset="/fonts/SB_White_1.svg 352w, /fonts/SB_White.svg 400w" width="400" height="178" loading="lazy">
          </router-link>
          <div class="custom-footer-text">
            <p>ACC Academy cung cấp các chương trình đào tạo giúp cá nhân và doanh nghiệp nâng cao kỹ năng chuyên môn, phát triển năng lực lãnh đạo, và xây dựng tổ chức vững mạnh.</p>
            <p>Các chuyên gia giàu kinh nghiệm của chúng tôi chia sẻ những phương pháp và công cụ thực tế, có thể áp dụng ngay vào công việc hằng ngày để tạo ra kết quả rõ ràng.</p>
          </div>
          <div class="custom-footer-gcn">
            <p>CÔNG TY TNHH SKILLS BRIDGE (ACC ACADEMY)</p>
            <p>Ngày cấp GCNĐKDN: 26/07/2022</p>
            <p>Nơi cấp GCNĐKDN: Sở KH&amp;ĐT TP. HCM (nay là Sở Tài Chính TP. HCM)</p>
            <p>MST: 0317402205</p>
            <p>Địa chỉ: Tầng lửng, Tòa nhà Fideco Riverview, Số 14 Đường Thảo Điền, Phường An Khánh, Thành phố Hồ Chí Minh, Việt Nam</p>
            <p>Văn phòng làm việc nội bộ - <strong>ACC Academy không tiếp nhận tư vấn trực tiếp tại văn phòng.</strong> Để được hỗ trợ, vui lòng liên hệ qua <strong>Zalo OA, Facebook Fanpage</strong> hoặc Hotline: 0909 77 00 85.</p>
          </div>
          <div class="custom-footer-social-heading">Theo dõi chúng tôi tại</div>
          <div class="custom-footer-socials">
            <ul class="social-media" role="list">
              <li>
                <a href="https://www.facebook.com/skillsbridgevn" class="tap-area" target="_blank" rel="noopener" aria-label="Follow on Facebook">
                  <svg role="presentation" focusable="false" width="27" height="27" class="icon icon-facebook" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M10.183 21.85v-8.868H7.2V9.526h2.983V6.982a4.17 4.17 0 0 1 4.44-4.572 22.33 22.33 0 0 1 2.667.144v3.084h-1.83a1.44 1.44 0 0 0-1.713 1.68v2.208h3.423l-.447 3.456h-2.97v8.868h-3.57Z" fill="currentColor"></path>
                  </svg>
                </a>
              </li>
              <li>
                <a href="https://www.tiktok.com/@skillsbridgevn" class="tap-area" target="_blank" rel="noopener" aria-label="Follow on TikTok">
                  <svg role="presentation" focusable="false" width="27" height="27" class="icon icon-tiktok" viewBox="0 0 24 24">
                    <path d="M20.027 10.168a5.125 5.125 0 0 1-4.76-2.294v7.893a5.833 5.833 0 1 1-5.834-5.834c.122 0 .241.011.361.019v2.874c-.12-.014-.237-.036-.36-.036a2.977 2.977 0 0 0 0 5.954c1.644 0 3.096-1.295 3.096-2.94L12.56 2.4h2.75a5.122 5.122 0 0 0 4.72 4.573v3.195" fill="currentColor"></path>
                  </svg>
                </a>
              </li>
              <li>
                <a href="https://www.linkedin.com/company/skillsbridgevn/" class="tap-area" target="_blank" rel="noopener" aria-label="Follow on LinkedIn">
                  <svg role="presentation" focusable="false" width="27" height="27" class="icon icon-linkedin" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M7.349 5.478a1.875 1.875 0 1 0-3.749 0 1.875 1.875 0 1 0 3.749 0ZM7.092 19.2H3.857V8.78h3.235V19.2ZM12.22 8.78H9.121V19.2h3.228v-5.154c0-1.36.257-2.676 1.94-2.676 1.658 0 1.68 1.554 1.68 2.763V19.2H19.2v-5.715c0-2.806-.605-4.963-3.877-4.963-1.573 0-2.629.863-3.06 1.683h-.044V8.78Z" fill="currentColor"></path>
                  </svg>
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="custom-footer-col">
          <h3 class="custom-footer-heading">Giới thiệu</h3>
          <ul class="custom-footer-linklist">
            <li><router-link to="/about-us">Về chúng tôi</router-link></li>
            <li><router-link to="/courses/ai">Đào tạo cá nhân</router-link></li>
            <li><router-link to="/corporate/dao-tao">Đào tạo doanh nghiệp</router-link></li>
            <li><router-link to="/library/blog">Bài viết chuyên gia</router-link></li>
          </ul>
        </div>
        <div class="custom-footer-col">
          <h3 class="custom-footer-heading">Điều khoản và Chính sách</h3>
          <ul class="custom-footer-linklist">
            <li><router-link to="/">Điều khoản sử dụng và Điều kiện chung</router-link></li>
            <li><router-link to="/">Chính sách thanh toán</router-link></li>
            <li><router-link to="/">Chính sách quyền riêng tư</router-link></li>
            <li><router-link to="/">Quy định xuất VAT</router-link></li>
          </ul>
        </div>
        <div class="custom-footer-col">
          <h3 class="custom-footer-heading">Liên hệ</h3>
          <div class="custom-footer-linklist">
            <p>Email: info@skillsbridge.vn</p>
            <p>Tư vấn khách hàng: 090.977.0085</p>
          </div>
        </div>
      </div>
      <div class="custom-footer-bottom">
        <div class="custom-footer-copyright">
          © 2026 - Bản quyền của Công ty TNHH Skills Bridge (ACC Academy)
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Footer component
</script>

<style scoped>
#shopify-section-sections--26112955253047__custom_footer_WzYrda {
  --footer-bg: #101828;
  --footer-text: #99a1af;
  --footer-heading: #ffffff;
  --footer-border: #ffffff1a;
}

.custom-footer {
  background-color: #101828;
  color: #99a1af;
  padding-top: 60px;
  padding-bottom: 40px;
  font-size: 14px;
  line-height: 1.6;
  font-family: inherit;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  width: 100%;
}

@media (min-width: 1000px) {
  .custom-footer {
    padding-top: 80px;
    padding-bottom: 80px;
  }
}

.custom-footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding-inline: 16px;
}

@media (min-width: 1000px) {
  .custom-footer-container {
    padding-inline: 0;
  }
}

.custom-footer-top {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

@media (min-width: 768px) {
  .custom-footer-top {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1000px) {
  .custom-footer-top {
    grid-template-columns: 3.5fr 2fr 2fr 2.5fr;
    gap: 60px;
  }
}

.custom-footer-col {
  display: flex;
  flex-direction: column;
}

.custom-footer-heading {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 20px 0;
}

.custom-footer-logo {
  display: block;
  margin-bottom: 24px;
}

.custom-footer-logo img {
  max-width: 100px;
  height: auto;
  display: block;
}

.custom-footer-text {
  color: #99a1af;
  margin-bottom: 24px;
  font-size: 16px;
  line-height: 1.6;
  opacity: 0.8;
}

.custom-footer-text p {
  margin: 0 0 12px 0;
}

.custom-footer-text p:last-child {
  margin-bottom: 0;
}

.custom-footer-linklist {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-size: 16px;
}

.custom-footer-linklist a {
  color: #99a1af;
  text-decoration: none;
  transition: opacity 0.2s ease, color 0.2s ease;
  opacity: 0.8;
}

.custom-footer-linklist a:hover {
  color: #ffffff;
  opacity: 1;
}

.custom-footer-social-heading {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 12px 0 16px 0;
}

.custom-footer-gcn {
  color: #99a1af;
  font-size: 16px;
  line-height: 1.5;
  opacity: 0.8;
  margin: 0 0 16px 0;
}

.custom-footer-gcn p {
  margin: 0 0 6px 0;
}

.custom-footer-gcn p:last-child {
  margin-bottom: 0;
}

.custom-footer-socials {
  display: flex;
  gap: 16px;
  align-items: center;
}

.custom-footer-socials ul {
  display: flex;
  gap: 16px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.custom-footer-socials a {
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s ease;
}

.custom-footer-socials a:hover {
  opacity: 0.7;
}

.custom-footer-socials svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

/* Bottom Bar */
.custom-footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  text-align: center;
}

@media (min-width: 768px) {
  .custom-footer-bottom {
    flex-direction: row;
    text-align: left;
  }
}

.custom-footer-copyright {
  color: #99a1af;
  font-size: 16px;
  opacity: 0.7;
}
</style>
