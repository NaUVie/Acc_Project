<template>
  <div class="tab-content animate-fade-in">
    <!-- SUB-NAV: HERO BANNERS VS HOME VIDEO & INTRO -->
    <div class="mb-4" style="display: flex; gap: 10px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">
      <button 
        type="button" 
        @click="subTab = 'banners'" 
        class="btn btn-sm"
        :class="subTab === 'banners' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Banner Hero ({{ banners.length }})
      </button>
      <button 
        type="button" 
        @click="openHomeIntroTab" 
        class="btn btn-sm"
        :class="subTab === 'home_intro' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px; display: inline-flex; align-items: center; gap: 6px;"
      >
        <span>Cấu hình Nội dung Trang chủ (Video, Giới thiệu & Bento)</span>
        <HelpTooltip 
          desc="Tùy chỉnh video giới thiệu, nội dung Kiến tạo năng lực và phần Năng lực cốt lõi (Bento Grid) ở Trang chủ." 
          impact="Hiển thị tại Section Video/Giới thiệu và Section Năng lực cốt lõi ở Trang chủ." 
        />
      </button>
    </div>

    <!-- TAB 1: BANNERS CAROUSEL -->
    <div v-if="subTab === 'banners'">
      <!-- VIEW 1: LIST TABLE -->
      <div v-if="activeView === 'list'">
        <div class="content-header flex-between">
          <div>
            <h2 style="display: flex; align-items: center; gap: 8px;">
              Quản lý Banner (Hero Carousel)
              <HelpTooltip 
                desc="Tùy chỉnh các banner ảnh trình chiếu tự động ở đầu trang chủ." 
                impact="Hiển thị ngay đầu màn hình Trang chủ (Section Hero Banner)." 
              />
            </h2>
            <p>Tùy chỉnh các banner quảng cáo và hình ảnh trình chiếu trên trang chủ.</p>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <button @click="refreshBanners" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách banner mới nhất từ máy chủ">
              <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
              <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới dữ liệu' }}</span>
            </button>
            <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Banner mới</button>
          </div>
        </div>

        <!-- Banners Table -->
        <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 60px;">Vị trí</th>
              <th>Preview Banner</th>
              <th>
                Tiêu đề & Link
                <HelpTooltip desc="Tên banner và đường dẫn điều hướng khi người dùng nhấp vào." />
              </th>
              <th>
                Loại Link
                <HelpTooltip desc="Nội bộ (chuyển trang trong website) hoặc Ngoại bộ (mở tab mới sang web ngoài)." />
              </th>
              <th>
                Trạng thái
                <HelpTooltip desc="Nhấp để chuyển đổi giữa 'Đang hiển thị' và 'Đã ẩn'." impact="Ẩn hoặc hiện banner trên slide Trang chủ." />
              </th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in banners" :key="b.id">
              <td class="font-bold text-center" data-label="Vị trí">
                <span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
                  #{{ b.position }}
                </span>
              </td>
              <td data-label="Preview Banner">
                <div style="display: flex; gap: 8px; align-items: center;">
                  <img :src="b.desktop_image" :alt="b.title" class="admin-course-thumb" style="width: 120px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" />
                  <img v-if="b.mobile_image" :src="b.mobile_image" alt="Mobile" class="admin-course-thumb" style="width: 35px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" title="Mobile Image" />
                </div>
              </td>
              <td data-label="Tiêu đề & Link">
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ b.title }}</div>
                <small class="text-muted" style="word-break: break-all; display: block; margin-top: 2px;">
                  {{ b.link || '(Không có)' }}
                </small>
              </td>
              <td data-label="Loại Link">
                <span class="badge" :style="b.is_external ? 'background: #fef3c7; color: #b45309;' : 'background: #f1f5f9; color: #475569;'">
                  {{ b.is_external ? 'Ngoại bộ' : 'Nội bộ' }}
                </span>
              </td>
              <td data-label="Trạng thái">
                <button 
                  @click="toggleActive(b)" 
                  class="badge" 
                  :style="b.is_active ? 'background: #dcfce7; color: #15803d; border: none; cursor: pointer; padding: 6px 12px;' : 'background: #fee2e2; color: #b91c1c; border: none; cursor: pointer; padding: 6px 12px;'"
                  title="Nhấn để đổi trạng thái"
                >
                  {{ b.is_active ? 'Đang hiển thị' : 'Đã ẩn' }}
                </button>
              </td>
              <td data-label="Hành động">
                <div class="action-buttons">
                  <button @click="openCropper(b.desktop_image, async (url) => { await courseStore.updateBanner(b.id, { desktop_image: url }); b.desktop_image = url; courseStore.showToast('Đã cắt và cập nhật banner!', 'success'); }, 'banner', '✂ Cắt Banner: ' + b.title)" class="btn-action edit" title="Cắt lại ảnh Banner" style="color: #0284c7;">✂️</button>
                  <button @click="editBanner(b)" class="btn-action edit" title="Sửa Banner">✏️</button>
                  <button @click="deleteBannerItem(b.id)" class="btn-action delete" title="Xóa Banner">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="banners.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">Chưa có banner nào. Hãy nhấn "+ Thêm Banner mới".</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- VIEW 2: FORM ADD/EDIT -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa Banner' : 'Thêm Banner mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveBanner" class="mt-2">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600; display: flex; align-items: center; gap: 6px;">
            <span>Tiêu đề Banner</span>
            <HelpTooltip desc="Tên gợi nhớ của banner để tiện quản lý trong hệ thống." />
          </label>
          <input v-model="form.title" type="text" required class="admin-input-style" placeholder="Ví dụ: AI Center of Excellence" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600; display: flex; align-items: center; gap: 6px;">
              <span>Ảnh Desktop (Yêu cầu)</span>
              <HelpTooltip desc="Ảnh banner kích thước lớn cho màn hình máy tính (tỷ lệ chuẩn 1920x720)." impact="Ảnh nền slide chính tại Section 1 Trang chủ." />
            </label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input v-model="form.desktop_image" type="text" required class="admin-input-style" placeholder="/images/CoE-Web.png hoặc URL" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="desktopFileRef" @change="onFileSelectForCrop($event, (url) => { form.desktop_image = url; }, 'banner', '✂ Cắt Banner Desktop (1920x720)')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.desktopFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <div v-if="form.desktop_image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
              <img :src="form.desktop_image" alt="Preview Desktop" style="max-height: 80px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />
              <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.desktop_image, (url) => { form.desktop_image = url; }, 'banner', '✂ Cắt Banner Desktop (1920x720)')">✂ Cắt lại ảnh</button>
            </div>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600; display: flex; align-items: center; gap: 6px;">
              <span>Ảnh Mobile (Tùy chọn)</span>
              <HelpTooltip desc="Ảnh tối ưu riêng cho điện thoại màn hình dọc (tùy chọn)." impact="Tự động hiển thị khi học viên truy cập bằng điện thoại." />
            </label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input v-model="form.mobile_image" type="text" class="admin-input-style" placeholder="/images/CoE-Mobile.png hoặc URL" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="mobileFileRef" @change="onFileSelectForCrop($event, (url) => { form.mobile_image = url; }, 'free', '✂ Cắt Banner Mobile')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.mobileFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <div v-if="form.mobile_image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
              <img :src="form.mobile_image" alt="Preview Mobile" style="max-height: 80px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />
              <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.mobile_image, (url) => { form.mobile_image = url; }, 'free', '✂ Cắt Banner Mobile')">✂ Cắt lại ảnh</button>
            </div>
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600; display: flex; align-items: center; gap: 6px;">
              <span>Đường dẫn Liên kết (Link)</span>
              <HelpTooltip desc="Link đích khi người dùng click vào banner (ví dụ: /corporate/coe hoặc https://...)." impact="Điều hướng khách hàng khi nhấp vào banner." />
            </label>
            <input v-model="form.link" type="text" class="admin-input-style" placeholder="Ví dụ: /corporate/coe hoặc https://..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600; display: flex; align-items: center; gap: 6px;">
              <span>Thứ tự hiển thị (Position)</span>
              <HelpTooltip desc="Thứ tự xuất hiện của slide (1, 2, 3...)." />
            </label>
            <input v-model.number="form.position" type="number" min="0" class="admin-input-style" placeholder="1, 2, 3..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4" style="background: #f8fafc; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0;">
          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_external" type="checkbox" id="is_external" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="is_external" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0; display: flex; align-items: center; gap: 6px;">
              <span>Mở link trong tab mới (Trang ngoài / External Link)</span>
              <HelpTooltip desc="Nếu bật, khi nhấp vào banner sẽ mở trang mới trong tab khác (thường dùng cho link ngoài)." />
            </label>
          </div>

          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_active" type="checkbox" id="is_active" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="is_active" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0; display: flex; align-items: center; gap: 6px;">
              <span>Hiển thị Banner này trên trang chủ (Active)</span>
              <HelpTooltip desc="Bật để slide này hiển thị trên trang chủ, tắt để tạm ẩn." impact="Ẩn hoặc hiện slide trên Trang chủ." />
            </label>
          </div>
        </div>

        <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary">Hủy</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Banner' : 'Tạo Banner') }}
          </button>
        </div>
      </form>
    </div>
    </div> <!-- END TAB 1: BANNERS -->

    <!-- TAB 2: HOME INTRO & VIDEO CONFIGURATION -->
    <div v-else-if="subTab === 'home_intro'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="content-header flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div>
          <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0;">Cấu hình Phần "Kiến tạo năng lực — Dẫn dắt chuyển đổi bền vững" & Video</h2>
          <p style="color: #64748b; margin: 0; font-size: 13.5px;">Tùy chỉnh tiêu đề, hai đoạn văn giới thiệu, số liệu bộ đếm, đường dẫn video giới thiệu và ảnh bìa hiển thị trên trang chủ.</p>
        </div>
        <button type="button" @click="loadHomeIntroSettings" class="btn btn-secondary btn-sm" :disabled="loadingIntro">
          {{ loadingIntro ? 'Đang tải...' : 'Tải lại' }}
        </button>
      </div>

      <form @submit.prevent="saveHomeIntro">
        <div class="form-group mb-4">
          <label style="color: #1e293b; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
            <span>Tiêu đề chính (Hiệu ứng chữ từng từ) <span style="color: #e11d48;">*</span></span>
            <HelpTooltip desc="Dòng chữ lớn chạy hiệu ứng từng từ (Word-by-word fade in)." impact="Xuất hiện ở đầu Section 3 (Kiến tạo năng lực) Trang chủ." />
          </label>
          <input 
            v-model="introForm.title" 
            type="text" 
            required 
            class="admin-input-style" 
            placeholder="Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững" 
            style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 600;" 
          />
          <small class="text-muted" style="display: block; margin-top: 4px;">Mỗi từ trong câu tiêu đề này sẽ tự động chạy hiệu ứng xuất hiện trên trang chủ.</small>
        </div>

        <div class="grid grid-2 gap-4 mb-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>Đoạn giới thiệu 1 <span style="color: #e11d48;">*</span></span>
              <HelpTooltip desc="Đoạn văn đầu tiên giới thiệu về tầm nhìn và sứ mệnh đào tạo của ACC." impact="Hiển thị ở cột bên trái Section 3 Trang chủ." />
            </label>
            <textarea 
              v-model="introForm.desc1" 
              rows="4" 
              required 
              class="admin-input-style" 
              placeholder="ACC Academy đồng hành cùng cá nhân, doanh nghiệp và tổ chức..." 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
            ></textarea>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>Đoạn giới thiệu 2 <span style="color: #e11d48;">*</span></span>
              <HelpTooltip desc="Đoạn văn thứ hai chi tiết về mô hình kết hợp Đào tạo - Tư vấn - Công nghệ." impact="Hiển thị dưới đoạn 1 ở Section 3 Trang chủ." />
            </label>
            <textarea 
              v-model="introForm.desc2" 
              rows="4" 
              required 
              class="admin-input-style" 
              placeholder="Chúng tôi kết hợp Đào tạo – Tư vấn – Công nghệ – Chiến lược..." 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
            ></textarea>
          </div>
        </div>

        <div class="grid grid-2 gap-4 mb-4" style="background: #f8fafc; padding: 18px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>Số đếm hiển thị (Counter number)</span>
              <HelpTooltip desc="Con số dự án/chương trình đào tạo, tự động có hiệu ứng đếm số khi cuộn tới." impact="Hiển thị số lớn kèm dấu + (Ví dụ: 500+)." />
            </label>
            <input 
              v-model.number="introForm.counter_number" 
              type="number" 
              min="0" 
              class="admin-input-style" 
              placeholder="500" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 700;" 
            />
            <small class="text-muted" style="display: block; margin-top: 4px;">Hệ thống sẽ tự động thêm dấu "+" và chạy hiệu ứng tăng số (Ví dụ: 500+).</small>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>Mô tả dưới số đếm</span>
              <HelpTooltip desc="Dòng chữ chú thích bên dưới con số bộ đếm." impact="Hiển thị ngay dưới con số 500+ ở Section 3." />
            </label>
            <input 
              v-model="introForm.counter_label" 
              type="text" 
              class="admin-input-style" 
              placeholder="CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
          </div>
        </div>

        <!-- Video Configuration Section -->
        <div class="p-4 mb-4" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px;">
          <h4 style="margin: 0 0 12px 0; color: #166534; font-size: 15px; font-weight: 800;">Cấu hình Video Giới thiệu Trang chủ</h4>

          <div class="form-group mb-3">
            <label style="color: #14532d; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
              <span>Đường dẫn Video (Hỗ trợ Link YouTube, Google Drive, Direct MP4 hoặc Upload file) <span style="color: #e11d48;">*</span></span>
              <HelpTooltip desc="Hỗ trợ dán link YouTube (thường hoặc Shorts), link chia sẻ Google Drive hoặc file MP4 tải lên." impact="Video phát khi học viên bấm nút 'Xem Video' tại Trang chủ." />
            </label>
            <div style="display: flex; gap: 8px;">
              <input 
                v-model="introForm.video_url" 
                type="text" 
                required 
                class="admin-input-style" 
                placeholder="Dán link YouTube, Google Drive (drive.google.com/file/d/...) hoặc URL .mp4" 
                style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #86efac;" 
              />
              <input type="file" ref="videoFileRef" @change="uploadVideoFile" style="display: none;" accept="video/*" />
              <button type="button" @click="$refs.videoFileRef.click()" class="btn btn-secondary btn-sm" :disabled="uploadingVideo">
                {{ uploadingVideo ? 'Đang tải...' : 'Upload Video' }}
              </button>
            </div>
            <small style="display: block; margin-top: 4px; color: #15803d;">
              <strong>Hệ thống hỗ trợ đa dạng:</strong> Dán link YouTube (thường / Shorts), link chia sẻ Google Drive (ví dụ link của bạn: <code>https://drive.google.com/file/d/.../view</code>), file video trực tiếp (.mp4) hoặc bấm "Upload Video".
            </small>
          </div>

          <div class="grid grid-2 gap-4">
            <div class="form-group">
              <label style="color: #14532d; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
                <span>Ảnh bìa Video (Poster Thumbnail)</span>
                <HelpTooltip desc="Ảnh đại diện của khung video trước khi người dùng bấm phát clip." impact="Ảnh bìa hiển thị tại Section 3 Trang chủ." />
              </label>
              <div style="display: flex; gap: 8px;">
                <input 
                  v-model="introForm.poster_url" 
                  type="text" 
                  class="admin-input-style" 
                  placeholder="/images/CoE-Thumb.png hoặc link ảnh" 
                  style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #86efac;" 
                />
                <input type="file" ref="posterFileRef" @change="onFileSelectForCrop($event, (url) => { introForm.poster_url = url; }, 'wide', '✂ Cắt Poster Video (16:9)')" style="display: none;" accept="image/*" />
                <button type="button" @click="$refs.posterFileRef.click()" class="btn btn-secondary btn-sm">
                  Upload Ảnh
                </button>
              </div>
              <div v-if="introForm.poster_url" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
                <img :src="introForm.poster_url" alt="Poster Preview" style="max-height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid #86efac;" referrerpolicy="no-referrer" />
                <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #166534; border-color: #86efac;" @click="openCropper(introForm.poster_url, (url) => { introForm.poster_url = url; }, 'wide', '✂ Cắt Poster Video (16:9)')">✂ Cắt lại ảnh</button>
              </div>
            </div>

            <div class="form-group">
              <label style="color: #14532d; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
                <span>Chữ nút phát trên ảnh bìa</span>
                <HelpTooltip desc="Nhãn chữ trên nút phát video màu đỏ (ví dụ: XEM VIDEO GIỚI THIỆU ACC ACADEMY)." />
              </label>
              <input 
                v-model="introForm.btn_label" 
                type="text" 
                class="admin-input-style" 
                placeholder="XEM VIDEO GIỚI THIỆU ACC ACADEMY" 
                style="background: #ffffff; color: #0f172a; border: 1px solid #86efac;" 
              />
            </div>
          </div>
        </div>

        <!-- Bento Grid Header Configuration Section -->
        <div class="p-4 mb-4" style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px;">
          <h4 style="margin: 0 0 8px 0; color: #1e40af; font-size: 15px; font-weight: 800;">
            Cấu hình Tiêu đề Phần "Năng lực cốt lõi của ACC Academy" (Bento Grid)
          </h4>
          <p style="color: #475569; margin: 0 0 16px 0; font-size: 13px;">
            Tùy chỉnh tiêu đề chính và các dòng thông điệp giới thiệu sứ mệnh đào tạo ở đầu Section Năng lực cốt lõi trên Trang chủ.
          </p>

          <div class="form-group mb-3">
            <label style="color: #1e3a8a; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
              <span>Tiêu đề Section (H2) <span style="color: #e11d48;">*</span></span>
              <HelpTooltip desc="Tiêu đề lớn của Section Năng lực cốt lõi Trang chủ." />
            </label>
            <input 
              v-model="introForm.bento_title" 
              type="text" 
              required 
              class="admin-input-style" 
              placeholder="Năng lực cốt lõi của ACC Academy" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #93c5fd; font-weight: 700;" 
            />
          </div>

          <div class="grid grid-2 gap-4 mb-3">
            <div class="form-group">
              <label style="color: #1e3a8a; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
                <span>Dòng mô tả 1</span>
                <HelpTooltip desc="Dòng chữ đầu tiên giới thiệu về đơn vị giáo dục ACC." />
              </label>
              <textarea 
                v-model="introForm.bento_line1" 
                rows="2" 
                class="admin-input-style" 
                placeholder="ACC — Học viện Cổ phần Kết nối Tri thức — là đơn vị giáo dục chuyên biệt dành cho cá nhân và doanh nghiệp," 
                style="background: #ffffff; color: #0f172a; border: 1px solid #93c5fd;"
              ></textarea>
            </div>

            <div class="form-group">
              <label style="color: #1e3a8a; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
                <span>Dòng mô tả 2</span>
                <HelpTooltip desc="Dòng chữ tiếp theo về bảo chứng học thuật (Đại học Andrews)." />
              </label>
              <textarea 
                v-model="introForm.bento_line2" 
                rows="2" 
                class="admin-input-style" 
                placeholder="được bảo chứng học thuật bởi Đại học Andrews (Hoa Kỳ)." 
                style="background: #ffffff; color: #0f172a; border: 1px solid #93c5fd;"
              ></textarea>
            </div>
          </div>

          <div class="grid grid-2 gap-4">
            <div class="form-group">
              <label style="color: #1e3a8a; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
                <span>Dòng chữ in đậm / Tuyên ngôn</span>
                <HelpTooltip desc="Dòng chữ in đậm nhấn mạnh triết lý đào tạo (Ví dụ: Chúng tôi không bán khóa học.)." />
              </label>
              <input 
                v-model="introForm.bento_strong" 
                type="text" 
                class="admin-input-style" 
                placeholder="Chúng tôi không bán khóa học." 
                style="background: #ffffff; color: #0f172a; border: 1px solid #93c5fd; font-weight: 700;" 
              />
            </div>

            <div class="form-group">
              <label style="color: #1e3a8a; font-weight: 700; font-size: 13.5px; display: flex; align-items: center; gap: 6px;">
                <span>Dòng kết luận / Cam kết kết quả</span>
                <HelpTooltip desc="Dòng thông điệp cam kết kết quả đo lường được đi cùng doanh nghiệp." />
              </label>
              <input 
                v-model="introForm.bento_line3" 
                type="text" 
                class="admin-input-style" 
                placeholder="Chúng tôi kiến tạo năng lực có thể đo lường, đi cùng tổ chức của bạn đến kết quả thực." 
                style="background: #ffffff; color: #0f172a; border: 1px solid #93c5fd;" 
              />
            </div>
          </div>
        </div>

        <div class="flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="submit" class="btn btn-primary" :disabled="savingIntro" style="padding: 10px 24px; font-weight: 700;">
            {{ savingIntro ? 'Đang lưu cài đặt...' : 'Lưu Thay Đổi Trang Chủ' }}
          </button>
        </div>
      </form>
    </div>
    <!-- Image Cropper Modal -->
    <ImageCropperModal :isOpen="isCropperOpen" :imageUrl="cropTargetUrl" :aspectRatio="cropAspectRatio" :title="cropModalTitle" @close="isCropperOpen = false" @cropped="handleCroppedImage" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';
import ImageCropperModal from '@/components/ImageCropperModal.vue';
import HelpTooltip from '@/components/common/HelpTooltip.vue';

const courseStore = useCourseStore();

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Hình Ảnh');
let cropTargetCallback = null;

const openCropper = (url, callback, ratio = 'wide', title = '✂ Cắt & Căn Chỉnh Hình Ảnh') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'wide', title = '✂ Cắt & Căn Chỉnh Hình Ảnh') => {
  const file = event.target?.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    openCropper(e.target.result, callback, ratio, title);
  };
  reader.readAsDataURL(file);
  event.target.value = '';
};

const handleCroppedImage = async (newUrl) => {
  isCropperOpen.value = false;
  if (cropTargetCallback) {
    await cropTargetCallback(newUrl);
  }
};


const subTab = ref('banners'); // 'banners' or 'home_intro'
const isRefreshing = ref(false);

const refreshBanners = async () => {
  isRefreshing.value = true;
  try {
    await Promise.all([
      courseStore.fetchAdminBanners(true),
      courseStore.fetchBanners(true),
      courseStore.fetchHomeIntroSettings(true)
    ]);
    courseStore.showToast('Đã làm mới danh sách banner mới nhất!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới: ' + (err.message || err), 'error');
  } finally {
    isRefreshing.value = false;
  }
};

const activeView = ref('list');
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);

const form = ref({
  title: '',
  desktop_image: '',
  mobile_image: '',
  link: '',
  is_external: false,
  position: 1,
  is_active: true
});

// Home Intro & Video Config States
const loadingIntro = ref(false);
const savingIntro = ref(false);
const uploadingVideo = ref(false);
const introForm = ref({
  title: 'Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững',
  desc1: 'ACC Academy đồng hành cùng cá nhân, doanh nghiệp và tổ chức trong hành trình nâng cao năng lực, ứng dụng AI và chuyển đổi số vào thực tiễn.',
  desc2: 'Chúng tôi kết hợp Đào tạo – Tư vấn – Công nghệ – Chiến lược, giúp đội ngũ không chỉ hiểu công nghệ mà còn biết cách ứng dụng hiệu quả vào công việc, tối ưu quy trình và tạo ra giá trị tăng trưởng bền vững.',
  counter_number: 500,
  counter_label: 'CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI',
  video_url: '/videos/intro.mp4',
  poster_url: '/images/CoE-Thumb.png',
  btn_label: 'XEM VIDEO GIỚI THIỆU ACC ACADEMY',
  bento_title: 'Năng lực cốt lõi của ACC Academy',
  bento_line1: 'ACC — Học viện Cổ phần Kết nối Tri thức — là đơn vị giáo dục chuyên biệt dành cho cá nhân và doanh nghiệp,',
  bento_line2: 'được bảo chứng học thuật bởi Đại học Andrews (Hoa Kỳ).',
  bento_strong: 'Chúng tôi không bán khóa học.',
  bento_line3: 'Chúng tôi kiến tạo năng lực có thể đo lường, đi cùng tổ chức của bạn đến kết quả thực.'
});

const banners = computed(() => courseStore.adminBanners);

onMounted(async () => {
  try {
    await courseStore.fetchAdminBanners();
  } catch (err) {
    console.error("Error loading admin banners:", err);
  }
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  form.value = {
    title: '',
    desktop_image: '',
    mobile_image: '',
    link: '',
    is_external: false,
    position: (banners.value.length || 0) + 1,
    is_active: true
  };
  activeView.value = 'form';
};

const editBanner = (b) => {
  isEditing.value = true;
  editingId.value = b.id;
  form.value = {
    title: b.title,
    desktop_image: b.desktop_image,
    mobile_image: b.mobile_image || '',
    link: b.link || '',
    is_external: !!b.is_external,
    position: b.position || 1,
    is_active: !!b.is_active
  };
  activeView.value = 'form';
};

const toggleActive = async (b) => {
  try {
    await courseStore.updateBanner(b.id, { is_active: !b.is_active });
    courseStore.showToast(`Đã ${!b.is_active ? 'bật' : 'tắt'} hiển thị banner "${b.title}"`, 'success');
  } catch (err) {
    courseStore.showToast("Lỗi khi cập nhật trạng thái banner: " + err.message, 'error');
  }
};

const uploadImage = async (event, targetField) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const url = await courseStore.uploadImage(file);
    form.value[targetField] = url;
    courseStore.showToast('Tải ảnh lên thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh: ' + err.message, 'error');
  }
};

const saveBanner = async () => {
  saving.value = true;
  try {
    const payload = {
      ...form.value,
      desktop_image: formatImageUrl(form.value.desktop_image),
      mobile_image: form.value.mobile_image ? formatImageUrl(form.value.mobile_image) : ''
    };
    if (isEditing.value) {
      await courseStore.updateBanner(editingId.value, payload);
      courseStore.showToast('Cập nhật banner thành công!', 'success');
    } else {
      await courseStore.createBanner(payload);
      courseStore.showToast('Tạo banner mới thành công!', 'success');
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast("Có lỗi xảy ra: " + (err.message || err), 'error');
  } finally {
    saving.value = false;
  }
};

const deleteBannerItem = async (id) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa Banner',
    message: 'Bạn có chắc chắn muốn xóa banner trình chiếu này khỏi trang chủ?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteBanner(id);
      courseStore.showToast('Đã xóa banner thành công!', 'success');
    } catch (err) {
      courseStore.showToast("Lỗi khi xóa banner: " + err.message, 'error');
    }
  }
};

// Home Intro Methods
const openHomeIntroTab = async () => {
  subTab.value = 'home_intro';
  await loadHomeIntroSettings();
};

const loadHomeIntroSettings = async () => {
  loadingIntro.value = true;
  try {
    const res = await courseStore.fetchHomeIntroSettings();
    if (res) {
      introForm.value = {
        title: res.title || 'Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững',
        desc1: res.desc1 || '',
        desc2: res.desc2 || '',
        counter_number: res.counter_number ?? 500,
        counter_label: res.counter_label || 'CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI',
        video_url: res.video_url || '/videos/intro.mp4',
        poster_url: res.poster_url || '/images/CoE-Thumb.png',
        btn_label: res.btn_label || 'XEM VIDEO GIỚI THIỆU ACC ACADEMY',
        bento_title: res.bento_title || 'Năng lực cốt lõi của ACC Academy',
        bento_line1: res.bento_line1 || 'ACC — Học viện Cổ phần Kết nối Tri thức — là đơn vị giáo dục chuyên biệt dành cho cá nhân và doanh nghiệp,',
        bento_line2: res.bento_line2 || 'được bảo chứng học thuật bởi Đại học Andrews (Hoa Kỳ).',
        bento_strong: res.bento_strong || 'Chúng tôi không bán khóa học.',
        bento_line3: res.bento_line3 || 'Chúng tôi kiến tạo năng lực có thể đo lường, đi cùng tổ chức của bạn đến kết quả thực.'
      };
    }
  } catch (err) {
    console.error("Error loading home intro settings:", err);
  } finally {
    loadingIntro.value = false;
  }
};

const uploadPosterFile = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const url = await courseStore.uploadImage(file);
    introForm.value.poster_url = url;
    courseStore.showToast('Tải ảnh bìa video thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh bìa: ' + err.message, 'error');
  }
};

const uploadVideoFile = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  uploadingVideo.value = true;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/api/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${courseStore.token}`
      },
      body: formData
    });
    if (!res.ok) throw new Error('Upload video thất bại');
    const data = await res.json();
    introForm.value.video_url = data.url;
    courseStore.showToast('Tải video thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload video: ' + err.message, 'error');
  } finally {
    uploadingVideo.value = false;
  }
};

const saveHomeIntro = async () => {
  savingIntro.value = true;
  try {
    const payload = {
      ...introForm.value,
      poster_url: formatImageUrl(introForm.value.poster_url)
    };
    await courseStore.updateHomeIntroSettings(payload);
    courseStore.showToast('Đã lưu cấu hình phần giới thiệu & video trang chủ thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi lưu cài đặt: ' + (err.message || err), 'error');
  } finally {
    savingIntro.value = false;
  }
};
</script>
