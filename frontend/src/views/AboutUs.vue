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

<style scoped src="@/styles/views/AboutUs.css"></style>
