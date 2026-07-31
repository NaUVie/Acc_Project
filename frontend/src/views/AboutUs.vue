<template>
  <div class="about-us-page">
    <!-- Section 1: Intro -->
    <section class="cai-section">
      <div class="cai-container">
        <div class="cai-top">
          <div class="cai-col-left">
            <h2 class="cai-heading">
              <magic-text-animate animation="blur-in" split-by="word" stagger="0.05">
                <span class="cai-heading-1">Từ niềm tin</span>
                <span class="cai-heading-2">Đến tương lai</span>
              </magic-text-animate>
            </h2>
          </div>

          <div class="cai-col-right">
            <span class="custom-ui-tag cai-badge">
              Điều gì dẫn dắt chúng tôi
            </span>
            <div class="cai-desc">
              <p>Động lực lớn nhất của chúng tôi đến từ niềm tin: Mọi doanh nghiệp đều có thể bứt phá mạnh mẽ khi con người và công nghệ được kết nối đồng điệu. Sự chuyển đổi thành công của bạn là nguồn cảm hứng vô tận của ACC Academy.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 2: Image Banner with Overlay -->
    <section class="image-overlay-section">
      <div class="section section-blends section-full text-custom" style="--text-color: 255 255 255;">
        <image-banner reveal-on-scroll="true" parallax="0.3" class="content-over-media content-over-media--auto full-bleed text-custom" style="--text-color: 255 255 255;">
          <picture>
            <img src="/images/About_Us.png" alt="About ACC Academy" width="1920" height="960" sizes="100vw" fetchpriority="low" />
          </picture>
        </image-banner>
      </div>
    </section>

    <!-- Section 3: Services Grid -->
    <section class="cs-section">
      <div class="cs-top-container">
        <div class="cs-top">
          <span class="custom-ui-tag cs-badge">
            Về ACC Academy
          </span>
          <h2 class="cs-main-heading">
            <magic-text-animate animation="blur-in" split-by="word" stagger="0.05">
              ACC Academy là đối tác chiến lược trong việc giải quyết những thách thức nhân sự phức tạp và nắm bắt các cơ hội tăng trưởng đột phá
            </magic-text-animate>
          </h2>
        </div>
        <div class="cs-mid"></div>
      </div>

      <div class="cs-container">
        <div class="cs-grid">
          <div class="cs-card">
            <image-banner class="cs-card-bg" parallax="0.3">
              <img src="/images/Service_5.png" alt="Đào tạo doanh nghiệp" width="800" height="1067" loading="lazy" />
              <div class="cs-card-overlay"></div>
            </image-banner>
            <div class="cs-card-content">
              <div class="cs-card-center">
                <div class="cs-card-icon">
                  <img src="/fonts/B2B.svg" alt="B2B Icon" width="128" height="128" loading="lazy" />
                </div>
                <h4 class="cs-card-title">Đào tạo Đội ngũ doanh nghiệp</h4>
              </div>
              <div class="cs-card-bottom">
                <p>Xây dựng năng lực thích ứng cao cho tổ chức thông qua các lộ trình đào tạo được thiết kế riêng</p>
              </div>
            </div>
          </div>

          <div class="cs-card">
            <image-banner class="cs-card-bg" parallax="0.3">
              <img src="/images/Service_05.png" alt="Tư vấn tự động hóa" width="800" height="1067" loading="lazy" />
              <div class="cs-card-overlay"></div>
            </image-banner>
            <div class="cs-card-content">
              <div class="cs-card-center">
                <div class="cs-card-icon">
                  <img src="/fonts/automation.svg" alt="Automation Icon" width="128" height="128" loading="lazy" />
                </div>
                <h4 class="cs-card-title">Tư vấn Tự động hóa</h4>
              </div>
              <div class="cs-card-bottom">
                <p>Đưa AI và công nghệ tự động vào cốt lõi vận hành để tối ưu hóa nguồn lực và giảm thiểu rủi ro</p>
              </div>
            </div>
          </div>

          <div class="cs-card">
            <image-banner class="cs-card-bg" parallax="0.3">
              <img src="/images/Service_03.png" alt="Digital Marketing" width="800" height="1067" loading="lazy" />
              <div class="cs-card-overlay"></div>
            </image-banner>
            <div class="cs-card-content">
              <div class="cs-card-center">
                <div class="cs-card-icon">
                  <img src="/fonts/Digital.svg" alt="Digital Icon" width="128" height="128" loading="lazy" />
                </div>
                <h4 class="cs-card-title">Tư vấn Digital Marketing</h4>
              </div>
              <div class="cs-card-bottom">
                <p>Kết nối chiến lược thương hiệu với sức mạnh số để tạo ra sự tăng trưởng doanh thu có thể đo lường được</p>
              </div>
            </div>
          </div>

          <div class="cs-card">
            <image-banner class="cs-card-bg" parallax="0.3">
              <img src="/images/Img_2.png" alt="Khóa học cá nhân" width="800" height="800" loading="lazy" />
              <div class="cs-card-overlay"></div>
            </image-banner>
            <div class="cs-card-content">
              <div class="cs-card-center">
                <div class="cs-card-icon">
                  <img src="/fonts/B2C.svg" alt="B2C Icon" width="128" height="128" loading="lazy" />
                </div>
                <h4 class="cs-card-title">Khóa học Cá nhân</h4>
              </div>
              <div class="cs-card-bottom">
                <p>Trang bị hệ thống tư duy và công cụ để mỗi cá nhân trở thành phiên bản xuất sắc nhất trong sự nghiệp</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 4: Our Story -->
    <section class="cos-section">
      <div class="cos-container">
        <div class="cos-grid">
          <div class="cos-col-left">
            <div class="cos-badge">
              <span class="custom-ui-tag">Câu chuyện của chúng tôi</span>
            </div>
            <h2 class="cos-heading">
              <magic-text-animate animation="blur-in" split-by="word" stagger="0.05">
                Hành trình <br><em>Kiến tạo tác động</em>
              </magic-text-animate>
            </h2>
          </div>

          <div class="cos-col-right">
            <h3 class="cos-content-heading">Từ ý tưởng đến thực tế</h3>
            <div class="cos-text">
              <p>Từ những nền tảng tư duy đầu tiên, ACC Academy đã tiến hóa thành một tổ chức cung cấp giải pháp chuyển đổi uy tín, đồng hành cùng mạng lưới những cá nhân và doanh nghiệp khát khao định nghĩa lại chuẩn mực của sự xuất sắc.</p>
              <p>Mục tiêu cốt lõi của chúng tôi được gói gọn trong một tuyên bố: <strong>Khai mở tiềm năng của những người thúc đẩy tương lai.</strong></p>
              <p>Chúng tôi hiện thực hóa sứ mệnh này thông qua 3 nguyên tắc hành động:<br><br>
                <strong>1. Chinh phục sự Phức tạp</strong>: Chúng tôi giúp doanh nghiệp khám phá các nguồn lợi thế cạnh tranh mới bằng cách tối ưu hóa các hệ thống vận hành phức tạp thông qua AI và Tự động hóa.<br><br>
                <strong>2. Cùng tăng trưởng</strong>: Chúng tôi tin vào sức mạnh của việc nâng tầm năng lực cộng sự và đối tác, giúp họ đạt được tiềm năng tối đa và xây dựng thành công bền vững.<br><br>
                <strong>3. Kiến tạo Tác động Truyền cảm hứng</strong>: Chúng tôi nhìn xa hơn những mục tiêu ngắn hạn để xây dựng năng lực thích ứng cho tổ chức trong cả một thập kỷ kế tiếp.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 5: Scrolling Images -->
    <section class="scrolling-section">
      <div class="section section--narrow section-full bg-custom" style="--background: 247 247 244;">
        <!-- Mobile Layout -->
        <images-with-text-scrolling class="images-scrolling-mobile scroll-area bleed sm:unbleed">
          <div class="images-scrolling-mobile__item snap-start">
            <img src="/images/B2B_7.png" alt="Khởi nguồn" loading="lazy" class="rounded-sm" />
            <div class="images-scrolling__content">
              <span class="images-scrolling__counter bold">01</span>
              <div class="prose">
                <p class="h1" reveal-on-scroll="true"><split-lines>Khởi nguồn</split-lines></p>
                <p>Bắt đầu với khát vọng phá vỡ các rào cản học tập truyền thống, chúng tôi đã đặt những viên gạch đầu tiên cho một hệ sinh thái giáo dục thực chiến, nơi tri thức được chuyển hóa trực tiếp thành giá trị vận hành.</p>
              </div>
            </div>
          </div>
          <div class="images-scrolling-mobile__item snap-start">
            <img src="/images/B2B_15.png" alt="Mở rộng quy mô" loading="lazy" class="rounded-sm" />
            <div class="images-scrolling__content">
              <span class="images-scrolling__counter bold">02</span>
              <div class="prose">
                <p class="h1" reveal-on-scroll="true"><split-lines>Mở rộng quy mô</split-lines></p>
                <p>Với triết lý "Người học là trung tâm của mọi sự thay đổi", chúng tôi không ngừng hội tụ đội ngũ chuyên gia giàu kinh nghiệm thực chiến và áp dụng các công nghệ tiên phong để cá nhân hóa hành trình phát triển cho mọi đối tác.</p>
              </div>
            </div>
          </div>
          <div class="images-scrolling-mobile__item snap-start">
            <img src="/images/B2B_14_1fce947b-4288-4364-bfc5-49f6305b4abe.png" alt="Vị thế hiện tại" loading="lazy" class="rounded-sm" />
            <div class="images-scrolling__content">
              <span class="images-scrolling__counter bold">03</span>
              <div class="prose">
                <p class="h1" reveal-on-scroll="true"><split-lines>Vị thế hiện tại</split-lines></p>
                <p>Qua nhiều năm không ngừng đổi mới phương pháp luận, ACC Academy đã trở thành bảo chứng cho sự thành công của hàng chục nghìn chuyên gia và hàng chục doanh nghiệp dẫn đầu.</p>
              </div>
            </div>
          </div>
        </images-with-text-scrolling>

        <!-- Desktop Layout -->
        <images-with-text-scrolling scrolling-experience="reveal" class="images-scrolling-desktop">
          <div class="images-scrolling-desktop__content-list">
            <div class="images-scrolling__content">
              <span class="images-scrolling__counter bold">01</span>
              <div class="prose">
                <p class="h1" reveal-on-scroll="true"><split-lines>Khởi nguồn</split-lines></p>
                <p>Bắt đầu với khát vọng phá vỡ các rào cản học tập truyền thống, chúng tôi đã đặt những viên gạch đầu tiên cho một hệ sinh thái giáo dục thực chiến, nơi tri thức được chuyển hóa trực tiếp thành giá trị vận hành.</p>
              </div>
            </div>
            <div class="images-scrolling__content opacity-0">
              <span class="images-scrolling__counter bold">02</span>
              <div class="prose">
                <p class="h1" reveal-on-scroll="true"><split-lines>Mở rộng quy mô</split-lines></p>
                <p>Với triết lý "Người học là trung tâm của mọi sự thay đổi", chúng tôi không ngừng hội tụ đội ngũ chuyên gia giàu kinh nghiệm thực chiến và áp dụng các công nghệ tiên phong để cá nhân hóa hành trình phát triển cho mọi đối tác.</p>
              </div>
            </div>
            <div class="images-scrolling__content opacity-0">
              <span class="images-scrolling__counter bold">03</span>
              <div class="prose">
                <p class="h1" reveal-on-scroll="true"><split-lines>Vị thế hiện tại</split-lines></p>
                <p>Qua nhiều năm không ngừng đổi mới phương pháp luận, ACC Academy đã trở thành bảo chứng cho sự thành công của hàng chục nghìn chuyên gia và hàng chục doanh nghiệp dẫn đầu.</p>
              </div>
            </div>
          </div>

          <div class="images-scrolling-desktop__media-wrapper">
            <img src="/images/B2B_7.png" alt="Step 1" loading="lazy" class="rounded-sm" />
            <img src="/images/B2B_15.png" alt="Step 2" loading="lazy" class="rounded-sm" />
            <img src="/images/B2B_14_1fce947b-4288-4364-bfc5-49f6305b4abe.png" alt="Step 3" loading="lazy" class="rounded-sm" />
          </div>
        </images-with-text-scrolling>
      </div>
    </section>

    <!-- Section 6: Stats -->
    <section class="cstats-section">
      <div class="cstats-bg-image">
        <img src="/images/About-us-hero.png" alt="Stats background" loading="lazy" />
      </div>
      <div class="cstats-overlay"></div>

      <div class="cstats-container">
        <div class="cstats-content">
          <span class="custom-ui-tag cstats-badge">
            Thống kê
          </span>
          <h2 class="cstats-heading">
            <magic-text-animate animation="blur-in" split-by="word" stagger="0.05">
              Những con số minh chứng cho <br><em>Tác động chiến lược</em>
            </magic-text-animate>
          </h2>
          <div class="cstats-description">
            <p>Chúng tôi không chỉ nói về thay đổi; chúng tôi đo lường nó. Mỗi chỉ số dưới đây là kết quả của sự cam kết tuyệt đối về chất lượng và hiệu quả thực tế.</p>
          </div>
        </div>

        <div class="cstats-grid">
          <div class="cstats-card">
            <h3 class="cstats-card-value">17,000+ Chuyên gia</h3>
            <p class="cstats-card-text">Đã được nâng tầm năng lực, sẵn sàng cho những vị trí then chốt</p>
          </div>
          <div class="cstats-card">
            <h3 class="cstats-card-value">70+ Doanh nghiệp</h3>
            <p class="cstats-card-text">Đã chuyển đổi thành công mô hình vận hành và đào tạo</p>
          </div>
          <div class="cstats-card">
            <h3 class="cstats-card-value">7 Thị trường Quốc tế</h3>
            <p class="cstats-card-text">Minh chứng cho phương pháp luận chuẩn mực toàn cầu</p>
          </div>
          <div class="cstats-card">
            <h3 class="cstats-card-value">75% Chỉ số NPS</h3>
            <p class="cstats-card-text">Sự khẳng định tuyệt đối về chất lượng và tính ứng dụng thực tiễn từ các đối tác</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  // Trigger animations if needed or track analytics
});
</script>

<style scoped>
.about-us-page {
  width: 100%;
  overflow-x: hidden;
}

/* Common tag style */
.custom-ui-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: 600;
  padding: var(--spacing-1) var(--spacing-3);
  background-color: rgb(var(--button-background-secondary) / 0.1);
  border: 1px solid rgb(var(--button-background-secondary) / 0.3);
  color: rgb(var(--button-background-secondary));
  border-radius: var(--rounded-xs);
  text-decoration: none;
  line-height: 1.4;
  transition: opacity 0.3s ease;
}

/* Section 1 Styles */
.cai-section {
  background-color: transparent;
  color: rgb(var(--text-primary));
  padding-block-start: var(--spacing-20);
  padding-block-end: var(--spacing-10);
}
.cai-container {
  padding-inline: var(--container-gutter);
  max-width: var(--container-max-width);
  margin-inline: auto;
}
.cai-top {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
}
.cai-col-left {
  flex: 1;
  max-width: 600px;
}
.cai-heading {
  margin: 0;
  line-height: 1.1;
}
.cai-heading-1 {
  display: block;
  font-size: clamp(40px, 6vw, 68px);
  font-weight: 500;
  color: rgb(var(--text-primary));
  letter-spacing: var(--heading-letter-spacing);
}
.cai-heading-2 {
  display: block;
  font-size: clamp(40px, 6vw, 68px);
  font-family: var(--font-display, serif);
  font-style: italic;
  font-weight: 400;
  color: rgb(var(--text-primary));
}
.cai-col-right {
  flex: 1;
  max-width: 500px;
}
.cai-badge {
  margin-bottom: var(--spacing-6);
}
.cai-desc {
  font-size: var(--text-base);
  line-height: 1.6;
  color: rgb(var(--text-primary));
  opacity: 0.8;
}

@media (min-width: 1024px) {
  .cai-top {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }
}

/* Section 2: Banner */
.image-overlay-section {
  width: 100%;
}

/* Section 3: Services Styles */
.cs-section {
  background-color: transparent;
  color: rgb(var(--text-primary));
  padding-block-start: var(--spacing-20);
  padding-block-end: var(--spacing-20);
  overflow: hidden;
}
.cs-top-container {
  padding-inline: var(--container-gutter);
  max-width: var(--container-max-width);
  margin-inline: auto;
}
.cs-top {
  text-align: center;
  max-width: 1000px;
  margin-inline: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-6);
  margin-bottom: var(--spacing-15);
}
.cs-badge {
  margin-bottom: var(--spacing-2);
}
.cs-main-heading {
  margin: 0;
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 500;
  line-height: 1.2;
  color: rgb(var(--text-primary));
  letter-spacing: var(--heading-letter-spacing);
}
.cs-container {
  width: 100%;
}
.cs-grid {
  display: grid;
  grid-template-columns: 1fr;
}
.cs-card {
  position: relative;
  height: 600px;
  display: flex;
  flex-direction: column;
  color: #ffffff;
  overflow: hidden;
  text-decoration: none;
}
.cs-card-bg {
  position: absolute;
  inset: 0;
  z-index: 1;
}
.cs-card-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cs-card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2;
  transition: backdrop-filter 0.4s ease, background 0.4s ease;
}
.cs-card:hover .cs-card-overlay {
  backdrop-filter: blur(12px);
  background: rgba(0, 0, 0, 0.75);
}
.cs-card-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 40px 20px;
}
.cs-card-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
}
.cs-card-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.cs-card-icon img {
  max-width: 100%;
  height: auto;
}
.cs-card-title {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
  text-align: center;
}
.cs-card-bottom {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  padding: 24px;
  font-size: 16px;
  line-height: 1.6;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  margin-top: auto;
}

@media (min-width: 768px) {
  .cs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .cs-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Section 4: Our Story Styles */
.cos-section {
  background-color: rgb(var(--background-primary));
  color: rgb(var(--text-primary));
  padding-block-start: var(--spacing-20);
  padding-block-end: var(--spacing-20);
}
.cos-container {
  padding-inline: var(--container-gutter);
  max-width: var(--container-max-width);
  margin-inline: auto;
}
.cos-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-10);
}
.cos-col-left {
  flex: 1;
  max-width: 500px;
}
.cos-badge {
  margin-bottom: var(--spacing-6);
}
.cos-heading {
  margin: 0;
  line-height: 1.1;
  font-size: clamp(40px, 6vw, 68px);
  font-weight: 500;
  color: rgb(var(--text-primary));
  letter-spacing: var(--heading-letter-spacing);
}
.cos-heading em {
  font-family: var(--font-display, serif);
  font-style: italic;
  font-weight: 400;
}
.cos-col-right {
  flex: 1;
  max-width: 720px;
}
.cos-content-heading {
  margin: 0 0 var(--spacing-6) 0;
  font-size: clamp(24px, 3vw, 32px);
  font-weight: 500;
  line-height: 1.2;
  color: rgb(var(--text-primary));
}
.cos-text {
  font-size: var(--text-base);
  line-height: 1.6;
  color: rgb(var(--text-primary));
  opacity: 0.8;
}
.cos-text p {
  margin-bottom: var(--spacing-4);
}

@media (min-width: 1024px) {
  .cos-container {
    max-width: 1200px;
    padding-inline: 0;
  }
  .cos-grid {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
    gap: 80px;
  }
}

/* Section 5: Scrolling Layout */
.scrolling-section {
  width: 100%;
}
.images-scrolling-desktop {
  display: flex;
  max-width: var(--container-narrow-max-width);
  margin-inline: auto;
  gap: var(--spacing-15);
  padding: var(--spacing-20) 0;
}
.images-scrolling-desktop__content-list {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-20);
}
.images-scrolling-desktop__media-wrapper {
  flex: 1.2;
  position: sticky;
  top: 100px;
  height: 600px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-5);
  overflow: hidden;
}
.images-scrolling-desktop__media-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--rounded-sm);
}
.images-scrolling__content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}
.images-scrolling__counter {
  font-size: var(--text-h3);
  font-weight: 700;
  color: rgb(var(--button-background-secondary));
}
.images-scrolling__content .h1 {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 600;
  margin: 0;
  color: rgb(var(--text-primary));
}
.images-scrolling__content p {
  font-size: var(--text-base);
  color: var(--text-secondary);
  line-height: 1.6;
}

.images-scrolling-mobile {
  display: none;
  padding: 40px 16px;
}

@media (max-width: 768px) {
  .images-scrolling-desktop {
    display: none;
  }
  .images-scrolling-mobile {
    display: flex;
    flex-direction: column;
    gap: 40px;
  }
  .images-scrolling-mobile__item {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .images-scrolling-mobile__item img {
    width: 100%;
    height: auto;
    object-fit: cover;
  }
}

/* Section 6: Stats Styles */
.cstats-section {
  position: relative;
  padding-block-start: 100px;
  padding-block-end: 100px;
  color: #ffffff;
  overflow: hidden;
}
.cstats-bg-image {
  position: absolute;
  inset: 0;
  z-index: 1;
}
.cstats-bg-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cstats-overlay {
  position: absolute;
  inset: 0;
  background: #000000;
  opacity: 0.6;
  z-index: 2;
}
.cstats-container {
  position: relative;
  z-index: 3;
  max-width: 1600px;
  margin-inline: auto;
  padding-inline: 16px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
}
.cstats-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.cstats-badge {
  margin-bottom: 24px !important;
}
.cstats-heading {
  margin: 0 0 24px 0;
  font-size: clamp(32px, 5vw, 64px);
  font-weight: 500;
  line-height: 1.1;
  color: #ffffff;
  letter-spacing: -0.02em;
}
.cstats-heading em {
  font-family: var(--font-display, serif);
  font-style: italic;
  font-weight: 400;
}
.cstats-description {
  margin: 0;
  font-size: 16px;
  line-height: 1.6;
  max-width: 480px;
  color: rgba(255, 255, 255, 0.9);
}
.cstats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}
.cstats-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border-radius: 4px;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.15);
  transition: background 0.3s ease, transform 0.3s ease;
}
.cstats-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}
.cstats-card-value {
  margin: 0 0 16px 0;
  font-size: 32px;
  font-weight: 500;
  line-height: 1.2;
  color: #ffffff;
}
.cstats-card-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.8);
}

@media (min-width: 768px) {
  .cstats-container {
    padding-inline: 40px;
  }
  .cstats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
}
@media (min-width: 1024px) {
  .cstats-container {
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;
  }
}
@media (min-width: 1200px) {
  .cstats-container {
    grid-template-columns: 5fr 7fr;
    gap: 100px;
  }
}
</style>
