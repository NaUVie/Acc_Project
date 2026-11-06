<template>
  <div class="legal-policy-page container">
    <div class="policy-wrapper glass-card">
      <nav class="policy-breadcrumbs">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">/</span>
        <span class="current">{{ pageTitle }}</span>
      </nav>

      <div class="policy-layout">
        <!-- Sidebar Navigation giữa các trang chính sách -->
        <aside class="policy-sidebar">
          <h3 class="sidebar-heading">Chính sách & Quy định</h3>
          <ul class="policy-nav-list">
            <li>
              <router-link to="/terms-of-service" :class="{ active: currentTab === 'terms' }">
                Điều khoản dịch vụ
              </router-link>
            </li>
            <li>
              <router-link to="/privacy-policy" :class="{ active: currentTab === 'privacy' }">
               Chính sách bảo mật
              </router-link>
            </li>
            <li>
              <router-link to="/refund-policy" :class="{ active: currentTab === 'refund' }">
                Chính sách hoàn tiền
              </router-link>
            </li>
            <li>
              <router-link to="/payment-guide" :class="{ active: currentTab === 'payment' }">
                Hướng dẫn thanh toán
              </router-link>
            </li>
            <li>
              <router-link to="/delivery-policy" :class="{ active: currentTab === 'delivery' }">
                Truy cập & Kích hoạt khóa học
              </router-link>
            </li>
          </ul>

          <div class="support-box">
            <span class="support-title">Cần hỗ trợ trực tiếp?</span>
            <p class="support-desc">Hotline hỗ trợ học viên 24/7</p>
            <a href="tel:0938566700" class="btn-support-call"> 0938 566 700</a>
          </div>
        </aside>

        <!-- Main Content theo tab chính sách -->
        <main class="policy-content">
          <!-- 1. ĐIỀU KHOẢN DỊCH VỤ -->
          <article v-if="currentTab === 'terms'" class="content-section">
            <h1 class="policy-title">ĐIỀU KHOẢN DỊCH VỤ & SỬ DỤNG HỆ THỐNG</h1>
            <p class="policy-date">Áp dụng từ ngày 01/01/2026 | Công ty Cổ phần Kết nối Tri thức ACC</p>

            <div class="policy-body">
              <section>
                <h2>1. Giới thiệu chung</h2>
                <p>Chào mừng bạn đến với <strong>ACC Academy</strong> (nền tảng đào tạo trực tuyến thuộc Công ty Cổ phần Kết nối Tri thức ACC). Khi đăng ký tài khoản, mua khóa học hoặc sử dụng bất kỳ dịch vụ nào trên website, bạn đồng ý tuân thủ toàn bộ các điều khoản và quy định được nêu tại đây.</p>
              </section>

              <section>
                <h2>2. Đăng ký & Bảo mật tài khoản</h2>
                <ul>
                  <li>Học viên có nghĩa vụ cung cấp thông tin chính xác (Họ tên, Email, Số điện thoại) khi tạo tài khoản để đảm bảo quyền lợi kích hoạt khóa học và cấp chứng chỉ.</li>
                  <li>Mỗi tài khoản được cấp cho <strong>một cá nhân duy nhất</strong> sử dụng. Nghiêm cấm mọi hành vi chia sẻ, bán lại hoặc cho thuê tài khoản cho nhiều người sử dụng chung.</li>
                  <li>Nếu phát hiện hành vi truy cập bất thường từ nhiều địa chỉ IP/thiết bị khác nhau cùng lúc, hệ thống có quyền tạm khóa tài khoản để xác minh bảo mật.</li>
                </ul>
              </section>

              <section>
                <h2>3. Quyền sở hữu trí tuệ & Bản quyền bài học</h2>
                <ul>
                  <li>Toàn bộ bài giảng video, slide bài thuyết trình, tài liệu giáo trình, biểu mẫu và case study trên website đều thuộc bản quyền của ACC Academy và các Chuyên gia / Giảng viên đối tác.</li>
                  <li>Học viên chỉ có quyền xem và tải các tài liệu đính kèm phục vụ mục đích học tập cá nhân. Nghiêm cấm sao chép, tải lậu video, phát tán công khai hoặc thương mại hóa dưới mọi hình thức mà không có sự đồng ý bằng văn bản của ACC.</li>
                </ul>
              </section>

              <section>
                <h2>4. Giới hạn trách nhiệm</h2>
                <p>ACC Academy cam kết duy trì hệ thống hoạt động ổn định và thông suốt. Tuy nhiên, chúng tôi không chịu trách nhiệm đối với các sự cố gián đoạn do lỗi đường truyền mạng của học viên hoặc các sự cố bất khả kháng từ nhà cung cấp hạ tầng viễn thông.</p>
              </section>
            </div>
          </article>

          <!-- 2. CHÍNH SÁCH BẢO MẬT THÔNG TIN -->
          <article v-else-if="currentTab === 'privacy'" class="content-section">
            <h1 class="policy-title">CHÍNH SÁCH BẢO MẬT THÔNG TIN KHÁCH HÀNG</h1>
            <p class="policy-date">Tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân</p>

            <div class="policy-body">
              <section>
                <h2>1. Mục đích thu thập thông tin</h2>
                <p>Chúng tôi chỉ thu thập các thông tin cần thiết phục vụ cho việc vận hành đào tạo:</p>
                <ul>
                  <li><strong>Thông tin liên hệ:</strong> Họ tên, Số điện thoại, Email để gửi thông báo kích hoạt khóa học, biên lai thanh toán và hỗ trợ học tập.</li>
                  <li><strong>Dữ liệu học tập:</strong> Tiến độ hoàn thành bài học, kết quả bài trắc nghiệm để đánh giá và cấp chứng chỉ hoàn thành.</li>
                  <li><strong>Lịch sử giao dịch:</strong> Mã đơn hàng, phương thức thanh toán, số tiền đã trả để đối soát khi cần hoàn tiền hoặc hỗ trợ kỹ thuật.</li>
                </ul>
              </section>

              <section>
                <h2>2. Cam kết không chia sẻ thông tin</h2>
                <p>ACC Academy cam kết tuyệt đối bảo mật thông tin cá nhân của khách hàng. Chúng tôi <strong>không bao giờ bán, trao đổi hoặc chia sẻ</strong> dữ liệu của bạn cho bất kỳ đơn vị quảng cáo hay bên thứ ba nào, ngoại trừ:</p>
                <ul>
                  <li>Các đối tác cổng thanh toán được cấp phép (như Cổng VNPAY) nhằm mục đích xử lý giao dịch an toàn.</li>
                  <li>Khi có yêu cầu bằng văn bản từ cơ quan nhà nước có thẩm quyền theo quy định của pháp luật Việt Nam.</li>
                </ul>
              </section>

              <section>
                <h2>3. Bảo mật thanh toán</h2>
                <p>Mọi giao dịch trực tuyến qua thẻ ATM, Internet Banking hoặc mã QR đều được điều hướng trực tiếp sang hạ tầng bảo mật của <strong>Cổng thanh toán VNPAY</strong> (đạt chứng chỉ bảo mật quốc tế PCI DSS). Hệ thống của ACC Academy <strong>hoàn toàn không lưu trữ</strong> số thẻ, mật khẩu OTP hay thông tin tài khoản ngân hàng của bạn.</p>
              </section>

              <section>
                <h2>4. Quyền của chủ thể dữ liệu</h2>
                <p>Học viên có quyền yêu cầu tra cứu, chỉnh sửa hoặc xóa thông tin cá nhân của mình trên hệ thống bằng cách liên hệ bộ phận hỗ trợ qua email <strong>info@acc-edu.vn</strong>.</p>
              </section>
            </div>
          </article>

          <!-- 3. CHÍNH SÁCH HOÀN TIỀN -->
          <article v-else-if="currentTab === 'refund'" class="content-section">
            <h1 class="policy-title">CHÍNH SÁCH HOÀN TIỀN & ĐỔI KHÓA HỌC</h1>
            <p class="policy-date">Đảm bảo quyền lợi và sự hài lòng tuyệt đối của học viên</p>

            <div class="policy-body">
              <section>
                <h2>1. Điều kiện được áp dụng hoàn tiền</h2>
                <p>Học viên có quyền gửi yêu cầu hoàn lại <strong>100% học phí</strong> trong các trường hợp sau:</p>
                <ul>
                  <li>Yêu cầu hoàn tiền được gửi trong vòng <strong>03 ngày (72 giờ)</strong> kể từ thời điểm thanh toán thành công.</li>
                  <li>Học viên chưa xem quá <strong>20% tổng số bài học</strong> của khóa học đó.</li>
                  <li>Chưa thực hiện tải về các tài nguyên số độc quyền (file mẫu, prompts bản quyền, source code).</li>
                  <li>Khóa học gặp lỗi kỹ thuật nghiêm trọng từ phía máy chủ ACC Academy mà đội ngũ kỹ thuật không thể khắc phục được trong 48 giờ.</li>
                </ul>
              </section>

              <section>
                <h2>2. Các trường hợp không được hoàn tiền</h2>
                <ul>
                  <li>Yêu cầu gửi quá thời hạn 03 ngày kể từ ngày kích hoạt đơn hàng.</li>
                  <li>Đã học hoặc mở xem vượt quá 20% nội dung chương trình.</li>
                  <li>Các gói khóa học Combo / Khuyến mãi giảm giá sốc từ 50% trở lên hoặc các khóa đào tạo doanh nghiệp In-house đã ký hợp đồng riêng.</li>
                  <li>Tài khoản bị khóa do vi phạm Điều khoản dịch vụ (chia sẻ tài khoản, cào lậu video bài giảng).</li>
                </ul>
              </section>

              <section>
                <h2>3. Quy trình & Thời gian nhận lại tiền</h2>
                <ol>
                  <li><strong>Bước 1:</strong> Gửi email yêu cầu về <code>info@acc-edu.vn</code> hoặc liên hệ hotline <code>0938 566 700</code>, cung cấp Mã đơn hàng và Lý do yêu cầu hoàn tiền.</li>
                  <li><strong>Bước 2:</strong> Bộ phận Chăm sóc Học viên sẽ kiểm tra lịch sử học tập trong vòng 24 giờ làm việc.</li>
                  <li><strong>Bước 3:</strong> Khi yêu cầu hợp lệ, số tiền sẽ được hoàn trả trực tiếp về tài khoản ngân hàng / thẻ mà bạn đã dùng để thanh toán qua cổng VNPAY trong thời gian từ <strong>03 - 07 ngày làm việc</strong> tùy theo quy định của ngân hàng phát hành thẻ.</li>
                </ol>
              </section>
            </div>
          </article>

          <!-- 4. HƯỚNG DẪN THANH TOÁN -->
          <article v-else-if="currentTab === 'payment'" class="content-section">
            <h1 class="policy-title">HƯỚNG DẪN THANH TOÁN KHÓA HỌC</h1>
            <p class="policy-date">Thanh toán an toàn, bảo mật và kích hoạt tự động tức thì</p>

            <div class="policy-body">
              <section>
                <h2>1. Các phương thức thanh toán được hỗ trợ</h2>
                <p>ACC Academy tích hợp giải pháp thanh toán điện tử thông qua <strong>Cổng thanh toán VNPAY</strong> với các hình thức đa dạng:</p>
                <ul>
                  <li><strong>Ứng dụng Ngân hàng (VNPAY-QR):</strong> Quét mã QR bằng App của hơn 40 ngân hàng lớn (Vietcombank, BIDV, Techcombank, MB, VPBank,...) hoặc Ví VNPAY.</li>
                  <li><strong>Thẻ ATM & Tài khoản Ngân hàng nội địa:</strong> Hỗ trợ tất cả các ngân hàng tại Việt Nam có kích hoạt Internet Banking.</li>
                  <li><strong>Thẻ quốc tế:</strong> Visa, MasterCard, JCB, American Express.</li>
                  <li><strong>Chuyển khoản trực tiếp:</strong> Chuyển khoản theo mã đơn hàng đến tài khoản công ty của ACC.</li>
                </ul>
              </section>

              <section>
                <h2>2. Các bước thanh toán qua Cổng VNPAY</h2>
                <div class="step-guide">
                  <div class="step-card">
                    <span class="step-num">1</span>
                    <div class="step-text">
                      <strong>Chọn khóa học & Vào trang Thanh toán</strong>
                      <p>Kiểm tra kỹ thông tin đơn hàng, nhập mã giảm giá (nếu có) và nhấn "Tiến hành thanh toán".</p>
                    </div>
                  </div>
                  <div class="step-card">
                    <span class="step-num">2</span>
                    <div class="step-text">
                      <strong>Chọn hình thức thanh toán VNPAY</strong>
                      <p>Hệ thống tự động chuyển bạn sang giao diện thanh toán bảo mật của Cổng VNPAY.</p>
                    </div>
                  </div>
                  <div class="step-card">
                    <span class="step-num">3</span>
                    <div class="step-text">
                      <strong>Xác nhận giao dịch</strong>
                      <p>Mở ứng dụng ngân hàng quét mã QR hoặc nhập thông tin thẻ và xác thực mã OTP gửi về điện thoại.</p>
                    </div>
                  </div>
                  <div class="step-card">
                    <span class="step-num">4</span>
                    <div class="step-text">
                      <strong>Nhận khóa học tức thì</strong>
                      <p>Sau khi thanh toán thành công, hệ thống tự động đưa bạn về trang xác nhận và kích hoạt khóa học vào mục "Khu vực học tập" của bạn.</p>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </article>

          <!-- 5. TRUY CẬP & KÍCH HOẠT KHÓA HỌC -->
          <article v-else-if="currentTab === 'delivery'" class="content-section">
            <h1 class="policy-title">QUY TRÌNH TRUY CẬP & GIAO NHẬN DỊCH VỤ SỐ</h1>
            <p class="policy-date">Chính sách áp dụng cho các sản phẩm giáo dục số trực tuyến</p>

            <div class="policy-body">
              <section>
                <h2>1. Đặc thù sản phẩm</h2>
                <p>Các sản phẩm cung cấp trên ACC Academy là <strong>sản phẩm số / khóa học trực tuyến</strong> (Digital Products). Do đó không phát sinh chi phí vận chuyển, không giao nhận hàng hóa vật lý thông thường.</p>
              </section>

              <section>
                <h2>2. Thời gian & Cách thức kích hoạt</h2>
                <ul>
                  <li><strong>Thanh toán trực tuyến (VNPAY):</strong> Khóa học được hệ thống tự động kích hoạt <strong>ngay lập tức (trong vòng 1 - 3 phút)</strong> sau khi giao dịch thành công.</li>
                  <li><strong>Thanh toán Chuyển khoản ngân hàng thủ công:</strong> Bộ phận tài chính sẽ duyệt kích hoạt trong vòng <strong>15 - 30 phút</strong> trong giờ hành chính.</li>
                  <li>Hệ thống đồng thời gửi email thông báo xác nhận đơn hàng kèm hướng dẫn chi tiết đến địa chỉ email bạn đã đăng ký.</li>
                </ul>
              </section>

              <section>
                <h2>3. Hướng dẫn vào học sau khi mua</h2>
                <ol>
                  <li>Đăng nhập tài khoản trên website <strong>accacademy.vn</strong>.</li>
                  <li>Nhấp vào ảnh đại diện hoặc chọn menu <strong>"Dashboard / Khóa học của tôi"</strong>.</li>
                  <li>Bấm vào khóa học để xem thông tin chi tiết và tải tài liệu học tập đính kèm.</li>
                  <li>Khóa học có giá trị truy cập không giới hạn thời gian (trừ các chương trình có cam kết mentor đặc biệt theo kỳ hạn).</li>
                </ol>
              </section>
            </div>
          </article>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const currentTab = computed(() => {
  const p = route.path;
  if (p.includes('privacy-policy')) return 'privacy';
  if (p.includes('refund-policy')) return 'refund';
  if (p.includes('payment-guide')) return 'payment';
  if (p.includes('delivery-policy')) return 'delivery';
  return 'terms';
});

const pageTitle = computed(() => {
  switch (currentTab.value) {
    case 'privacy': return 'Chính sách bảo mật';
    case 'refund': return 'Chính sách hoàn tiền';
    case 'payment': return 'Hướng dẫn thanh toán';
    case 'delivery': return 'Truy cập & Giao nhận khóa học';
    default: return 'Điều khoản dịch vụ';
  }
});
</script>

<style scoped src="@/styles/views/LegalPolicy.css"></style>
