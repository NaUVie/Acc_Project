<template>
  <div class="tab-content animate-fade-in">
    <!-- SUB-NAV: PROJECTS VS REVIEWS -->
    <div class="mb-4" style="display: flex; gap: 10px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">
      <button 
        type="button" 
        @click="subTab = 'projects'" 
        class="btn btn-sm"
        :class="subTab === 'projects' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Danh sách Dự án ({{ projects.length }})
      </button>
      <button 
        type="button" 
        @click="openReviewsTab" 
        class="btn btn-sm"
        :class="subTab === 'reviews' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px; display: inline-flex; align-items: center; gap: 6px;"
      >
        <span>Duyệt Nhận xét học viên</span>
        <span 
          v-if="pendingReviewsCount > 0" 
          style="background: #ef4444; color: white; border-radius: 10px; padding: 1px 7px; font-size: 11px; font-weight: 800;"
        >
          {{ pendingReviewsCount }}
        </span>
      </button>
    </div>

    <!-- VIEW 1: PROJECTS MANAGEMENT -->
    <div v-if="subTab === 'projects'">
      <!-- VIEW 1.1: LIST TABLE -->
      <div v-if="activeView === 'list'">
        <div class="content-header flex-between">
          <div>
            <h2>Quản lý Dự án </h2>
            <p>Quản lý các dự án đào tạo, tư vấn chuyển đổi số đã thực hiện cho các Tập đoàn, Doanh nghiệp và Cá nhân.</p>
          </div>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Dự án mới</button>
        </div>

      <!-- Filters & Search -->
      <div class="flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0;">
          <button 
            @click="filterCategory = 'all'" 
            class="btn btn-sm"
            :class="filterCategory === 'all' ? 'btn-primary' : 'btn-secondary'"
          >
            Tất cả ({{ projects.length }})
          </button>
          <button 
            @click="filterCategory = 'du-an-doanh-nghiep'" 
            class="btn btn-sm"
            :class="filterCategory === 'du-an-doanh-nghiep' ? 'btn-primary' : 'btn-secondary'"
          >
            Doanh nghiệp ({{ corporateCount }})
          </button>
          <button 
            @click="filterCategory = 'du-an-ca-nhan'" 
            class="btn btn-sm"
            :class="filterCategory === 'du-an-ca-nhan' ? 'btn-primary' : 'btn-secondary'"
          >
            Cá nhân ({{ personalCount }})
          </button>
          <button 
            @click="filterCategory = 'du-an-nha-nuoc'" 
            class="btn btn-sm"
            :class="filterCategory === 'du-an-nha-nuoc' ? 'btn-primary' : 'btn-secondary'"
          >
            Khối Nhà nước ({{ govCount }})
          </button>
        </div>

        <div style="position: relative; min-width: 260px;">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Tìm tên dự án, khách hàng..." 
            class="admin-input-style"
            style="padding-left: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
          />
        </div>
      </div>

      <!-- Projects Table -->
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 120px;">Ảnh bìa</th>
              <th>Tên Dự án</th>
              <th>Khách hàng / Đối tác</th>
              <th>Chuyên mục</th>
              <th>Thời gian</th>
              <th style="width: 110px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in paginatedProjects" :key="p.id">
              <td>
                <img 
                  :src="p.image || '/images/default.jpg'" 
                  :alt="p.title" 
                  style="width: 110px; height: 65px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" 
                  referrerpolicy="no-referrer"
                />
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ p.title }}</div>
                <small class="text-muted" style="display: block; margin-top: 2px; color: #64748b;">
                  ID: {{ p.id }}
                </small>
              </td>
              <td>
                <span style="font-weight: 700; color: #0369a1;">{{ p.client || 'N/A' }}</span>
                <small v-if="p.drive_profile" style="display: block; margin-top: 2px;">
                  <a :href="p.drive_profile" target="_blank" style="color: #0284c7; text-decoration: underline;">Xem Drive Profile</a>
                </small>
              </td>
              <td>
                <span class="badge" style="background: rgba(2, 43, 159, 0.08); color: #022b9f; font-weight: 700;">
                  {{ p.category_name || p.category }}
                </span>
              </td>
              <td>
                <span class="text-muted" style="font-weight: 600; font-size: 13px;">{{ p.date || 'N/A' }}</span>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="editProject(p)" class="btn btn-sm btn-secondary" style="padding: 4px 8px; font-size: 12px;" title="Sửa dự án">Sửa</button>
                  <button @click="deleteItem(p.id)" class="btn btn-sm" style="padding: 4px 8px; font-size: 12px; background: #fee2e2; color: #b91c1c;" title="Xóa dự án">Xóa</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredProjects.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">
                Không tìm thấy dự án nào.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination for Projects Table -->
      <Pagination 
        v-if="filteredProjects.length > projectsPageSize"
        v-model:currentPage="projectsPage"
        :totalItems="filteredProjects.length"
        :pageSize="projectsPageSize"
      />
    </div>

    <!-- VIEW 2: FORM ADD/EDIT -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa Dự án / Case Study' : 'Thêm Dự án / Case Study mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveProject" class="mt-2">
        <div class="grid grid-2 gap-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Mã định danh Slug (ID) <span style="color: #e11d48;">*</span></label>
            <input 
              v-model="form.id" 
              :disabled="isEditing" 
              type="text" 
              required 
              class="admin-input-style" 
              placeholder="dao-tao-ai-acb" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
            <small class="text-muted" style="display: block; margin-top: 2px;">Chuỗi không dấu dùng làm đường dẫn URL xem chi tiết dự án.</small>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Chuyên mục Dự án <span style="color: #e11d48;">*</span></label>
            <select v-model="form.category" @change="onCategoryChange" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
              <option value="du-an-doanh-nghiep">Dự án Doanh nghiệp</option>
              <option value="du-an-ca-nhan">Dự án Cá nhân</option>
              <option value="du-an-nha-nuoc">Dự án Khối Cơ quan - Nhà nước</option>
            </select>
          </div>
        </div>

        <div class="form-group mt-4">
          <label style="color: #1e293b; font-weight: 600;">Tên / Tiêu đề Dự án <span style="color: #e11d48;">*</span></label>
          <input 
            v-model="form.title" 
            @input="generateSlug" 
            type="text" 
            required 
            class="admin-input-style" 
            placeholder="Ví dụ: Đào tạo ứng dụng Generative AI cho 150+ nhân sự quản lý Tập đoàn ACB" 
            style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
          />
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Tên Khách hàng / Tác giả</label>
            <input v-model="form.client" type="text" class="admin-input-style" placeholder="Ví dụ: Tập đoàn Tài chính ACB / Bosch Việt Nam" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Thời gian thực hiện</label>
            <input v-model="form.date" type="text" class="admin-input-style" placeholder="Ví dụ: 15/08/2026 hoặc Tháng 09/2026" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh đại diện Dự án (Thumbnail URL)</label>
            <div style="display: flex; gap: 8px;">
              <input v-model="form.image" type="text" class="admin-input-style" placeholder="https://... hoặc URL ảnh" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="imageFileRef" @change="uploadImage" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.imageFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <img v-if="form.image" :src="form.image" alt="Preview Image" style="margin-top: 8px; max-height: 100px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" referrerpolicy="no-referrer" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Link Hồ sơ năng lực / Google Drive Profile</label>
            <input v-model="form.driveProfile" type="text" class="admin-input-style" placeholder="https://drive.google.com/file/d/..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="form-group mt-4">
          <label style="color: #1e293b; font-weight: 600;">Mô tả / Tóm tắt ngắn Dự án</label>
          <textarea v-model="form.summary" rows="3" class="admin-input-style" placeholder="Nêu vắn tắt mục tiêu và kết quả cốt lõi của dự án..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        </div>

        <!-- Detailed Content Editor (Rich Text vs Blocks) -->
        <div class="mt-6 p-4" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;">
          <div class="flex-between mb-3" style="flex-wrap: wrap; gap: 10px;">
            <h4 style="margin: 0; color: #022b9f; font-size: 16px; font-weight: 800;">Nội dung chi tiết Bài viết Case Study</h4>
            
            <div style="display: flex; gap: 8px;">
              <button 
                type="button" 
                @click="editorMode = 'rich'" 
                class="btn btn-sm"
                :class="editorMode === 'rich' ? 'btn-primary' : 'btn-secondary'"
              >
                Trình soạn thảo văn bản
              </button>
              <button 
                type="button" 
                @click="editorMode = 'blocks'" 
                class="btn btn-sm"
                :class="editorMode === 'blocks' ? 'btn-primary' : 'btn-secondary'"
              >
                Dạng Khối Cấu trúc
              </button>
            </div>
          </div>

          <!-- Mode 1: WYSIWYG Rich Text Editor -->
          <div v-if="editorMode === 'rich'" class="mt-2">
            <RichTextEditor 
              v-model="richHtmlContent" 
              placeholder="Soạn thảo bài viết dự án trực quan (In đậm, In nghiêng, H2, H3, Danh sách, Link...)..." 
            />
          </div>

          <!-- Mode 2: Content Blocks Builder -->
          <div v-else-if="editorMode === 'blocks'" class="mt-2">
            <div class="flex-between mb-2">
              <span style="font-size: 13px; font-weight: 600; color: #475569;">Quản lý các khối văn bản chuẩn:</span>
              <button type="button" @click="addContentBlock('paragraph')" class="btn btn-secondary btn-sm">+ Thêm Khối văn bản mới</button>
            </div>

            <div v-for="(block, bIdx) in contentBlocks" :key="bIdx" class="mb-3 p-3" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px;">
              <div class="flex-between mb-2">
                <div style="display: flex; gap: 8px; align-items: center;">
                  <select v-model="block.type" class="admin-input-style" style="width: 150px; padding: 4px 8px; font-size: 13px;">
                    <option value="paragraph">Đoạn văn (Paragraph)</option>
                    <option value="heading">Tiêu đề phụ (Heading)</option>
                    <option value="bullets">Danh sách chấm tròn (Bullets)</option>
                  </select>
                  <span class="font-bold text-muted" style="font-size: 12px;">Khối {{ bIdx + 1 }}</span>
                </div>
                <button type="button" @click="removeContentBlock(bIdx)" class="btn btn-sm" style="padding: 2px 6px; font-size: 12px; background: #fee2e2; color: #b91c1c;" title="Xóa khối">Xóa</button>
              </div>

              <div v-if="block.type === 'bullets'">
                <label style="font-size: 12px; font-weight: 600; color: #475569;">Các ý chấm tròn (Mỗi ý 1 dòng):</label>
                <textarea v-model="block.bulletText" rows="3" class="admin-input-style" placeholder="Ý 1&#10;Ý 2&#10;Ý 3" style="font-size: 13.5px;"></textarea>
              </div>
              <div v-else>
                <textarea v-model="block.text" rows="2" class="admin-input-style" placeholder="Nhập nội dung văn bản..." style="font-size: 13.5px;"></textarea>
              </div>
            </div>

            <div v-if="contentBlocks.length === 0" class="text-center py-4 text-muted" style="font-size: 13px;">
              Chưa có khối nội dung nào. Nhấn "+ Thêm Khối văn bản mới" để bổ sung chi tiết bài viết.
            </div>
          </div>
        </div>

        <!-- Form Submit Actions -->
        <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary">Hủy</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Dự án' : 'Tạo Dự án') }}
          </button>
        </div>
      </form>
    </div>
    </div> <!-- END VIEW 1: PROJECTS -->

    <!-- VIEW 2: PROJECT REVIEWS MODERATION -->
    <div v-else-if="subTab === 'reviews'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Nhận xét & Đánh giá Dự án</h2>
          <p>Kiểm duyệt các ý kiến nhận xét của học viên trước khi cho phép hiển thị công khai trên bài viết dự án.</p>
        </div>
        <button @click="loadAdminReviews" class="btn btn-secondary btn-sm" :disabled="loadingReviews">
          Tải lại
        </button>
      </div>

      <!-- Filters -->
      <div class="flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0;">
          <button 
            @click="reviewStatusFilter = 'all'" 
            class="btn btn-sm"
            :class="reviewStatusFilter === 'all' ? 'btn-primary' : 'btn-secondary'"
          >
            Tất cả ({{ allProjectReviews.length }})
          </button>
          <button 
            @click="reviewStatusFilter = 'pending'" 
            class="btn btn-sm"
            :class="reviewStatusFilter === 'pending' ? 'btn-primary' : 'btn-secondary'"
          >
            Chờ duyệt ({{ pendingReviewsCount }})
          </button>
          <button 
            @click="reviewStatusFilter = 'approved'" 
            class="btn btn-sm"
            :class="reviewStatusFilter === 'approved' ? 'btn-primary' : 'btn-secondary'"
          >
            Đã duyệt ({{ approvedReviewsCount }})
          </button>
        </div>

        <div style="min-width: 260px;">
          <select v-model="reviewProjectFilter" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
            <option value="all">-- Lọc theo tất cả dự án --</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">
              {{ p.title }}
            </option>
          </select>
        </div>
      </div>

      <!-- Reviews Table -->
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 160px;">Học viên</th>
              <th style="width: 200px;">Dự án</th>
              <th style="width: 90px;">Đánh giá</th>
              <th>Nội dung nhận xét</th>
              <th style="width: 130px;">Trạng thái</th>
              <th style="width: 140px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rev in filteredProjectReviews" :key="rev.id">
              <td>
                <div class="font-bold" style="color: #0f172a;">{{ rev.author_name }}</div>
                <small class="text-muted" style="display: block; font-size: 11.5px; color: #64748b;">
                  {{ rev.author_email || 'Không có email' }}
                </small>
                <small class="text-muted" style="display: block; font-size: 11px; margin-top: 2px;">
                  {{ formatReviewDate(rev.created_at) }}
                </small>
              </td>
              <td>
                <span class="font-bold" style="color: #022b9f; font-size: 13.5px; display: block;">
                  {{ getProjectTitle(rev.project_id) }}
                </span>
                <router-link :to="'/du-an/' + rev.project_id" target="_blank" style="font-size: 12px; color: #0284c7; text-decoration: underline;">
                  Xem trang dự án
                </router-link>
              </td>
              <td>
                <span style="color: #f59e0b; font-weight: 700;">
                  ★ {{ rev.rating }}/5
                </span>
              </td>
              <td>
                <div class="admin-review-comment-box">
                  <p class="admin-review-comment-excerpt">
                    {{ rev.comment }}
                  </p>
                  <button 
                    type="button" 
                    @click="openReviewDetailModal(rev)" 
                    class="btn-view-review-detail"
                  >
                    Xem chi tiết
                  </button>
                </div>
              </td>
              <td>
                <span 
                  class="badge" 
                  :style="rev.is_approved ? 'background: #d1fae5; color: #065f46; font-weight: 700;' : 'background: #fef3c7; color: #92400e; font-weight: 700;'"
                >
                  {{ rev.is_approved ? 'Đã hiển thị' : 'Chờ phê duyệt' }}
                </span>
              </td>
              <td>
                <div class="action-buttons" style="gap: 6px;">
                  <button 
                    @click="handleToggleApproval(rev)" 
                    class="btn btn-sm"
                    :class="rev.is_approved ? 'btn-secondary' : 'btn-primary'"
                    style="padding: 4px 10px; font-size: 12px;"
                    :title="rev.is_approved ? 'Bấm để ẩn nhận xét' : 'Bấm để duyệt hiển thị nhận xét'"
                  >
                    {{ rev.is_approved ? 'Ẩn' : 'Duyệt' }}
                  </button>
                  <button 
                    @click="handleDeleteReview(rev.id)" 
                    class="btn btn-sm" 
                    style="padding: 4px 8px; font-size: 12px; background: #fee2e2; color: #b91c1c;"
                    title="Xóa nhận xét"
                  >
                    Xóa
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredProjectReviews.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">
                {{ loadingReviews ? 'Đang tải danh sách nhận xét...' : 'Không có nhận xét nào phù hợp bộ lọc.' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination for Admin Reviews -->
      <div class="mt-6 flex-between" style="flex-wrap: wrap; gap: 14px;" v-if="filteredProjectReviews.length > 0">
        <span style="font-size: 13px; color: #64748b;">
          Hiển thị {{ paginatedAdminReviews.length }} / {{ filteredProjectReviews.length }} nhận xét (Trang {{ adminReviewsPage }})
        </span>
        <Pagination 
          :currentPage="adminReviewsPage" 
          :totalItems="filteredProjectReviews.length" 
          :pageSize="adminReviewsPageSize" 
          @update:currentPage="adminReviewsPage = $event"
          @page-change="adminReviewsPage = $event"
        />
      </div>

      <!-- Review Detail Modal in Admin -->
      <div v-if="selectedReviewDetail" class="admin-modal-overlay animate-fade-in" @click.self="selectedReviewDetail = null">
        <div class="admin-modal-box">
          <div class="admin-modal-header">
            <h3>Chi tiết nhận xét của học viên</h3>
            <button @click="selectedReviewDetail = null" class="btn-modal-close">✕</button>
          </div>

          <div class="admin-modal-body">
            <div class="detail-row">
              <span class="detail-label">Dự án:</span>
              <strong style="color: #022b9f;">{{ getProjectTitle(selectedReviewDetail.project_id) }}</strong>
            </div>

            <div class="detail-row">
              <span class="detail-label">Học viên:</span>
              <span><strong>{{ selectedReviewDetail.author_name }}</strong> ({{ selectedReviewDetail.author_email || 'Không có email' }})</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Thời gian:</span>
              <span>{{ formatReviewDate(selectedReviewDetail.created_at) }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Đánh giá:</span>
              <span style="color: #f59e0b; font-weight: 700;">★ {{ selectedReviewDetail.rating }}/5 sao</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Trạng thái:</span>
              <span 
                class="badge" 
                :style="selectedReviewDetail.is_approved ? 'background: #d1fae5; color: #065f46; font-weight: 700;' : 'background: #fef3c7; color: #92400e; font-weight: 700;'"
              >
                {{ selectedReviewDetail.is_approved ? 'Đã phê duyệt hiển thị' : 'Đang chờ phê duyệt' }}
              </span>
            </div>

            <div class="detail-comment-section">
              <label class="detail-label" style="display: block; margin-bottom: 8px;">Nội dung nhận xét đầy đủ:</label>
              <div class="detail-comment-content">
                {{ selectedReviewDetail.comment }}
              </div>
            </div>
          </div>

          <div class="admin-modal-footer">
            <button 
              @click="handleToggleApproval(selectedReviewDetail)" 
              class="btn"
              :class="selectedReviewDetail.is_approved ? 'btn-secondary' : 'btn-primary'"
            >
              {{ selectedReviewDetail.is_approved ? 'Chuyển sang Ẩn' : 'Duyệt hiển thị ngay' }}
            </button>
            <button @click="selectedReviewDetail = null" class="btn btn-secondary">
              Đóng
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import RichTextEditor from '@/components/RichTextEditor.vue';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();

const subTab = ref('projects'); // 'projects' or 'reviews'

const activeView = ref('list');
const filterCategory = ref('all');
const searchQuery = ref('');
const isEditing = ref(false);
const saving = ref(false);

// Reviews Moderation State
const allProjectReviews = ref([]);
const loadingReviews = ref(false);
const reviewStatusFilter = ref('pending'); // 'all', 'pending', 'approved'
const reviewProjectFilter = ref('all');

// Main Projects Pagination
const projectsPage = ref(1);
const projectsPageSize = ref(10);

// Admin Reviews Pagination & Detail Modal
const adminReviewsPage = ref(1);
const adminReviewsPageSize = ref(10);
const selectedReviewDetail = ref(null);

const editorMode = ref('rich');
const richHtmlContent = ref('');

const form = ref({
  id: '',
  title: '',
  category: 'du-an-doanh-nghiep',
  categoryName: 'Dự án Doanh nghiệp',
  summary: '',
  image: '',
  date: '',
  client: '',
  driveProfile: ''
});

const contentBlocks = ref([]);

const projects = computed(() => courseStore.adminProjects || []);

const corporateCount = computed(() => projects.value.filter(p => p.category === 'du-an-doanh-nghiep').length);
const personalCount = computed(() => projects.value.filter(p => p.category === 'du-an-ca-nhan').length);
const govCount = computed(() => projects.value.filter(p => p.category === 'du-an-nha-nuoc').length);

const filteredProjects = computed(() => {
  return projects.value.filter(p => {
    // Category Filter
    if (filterCategory.value !== 'all' && p.category !== filterCategory.value) return false;

    // Search Query
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const matchTitle = p.title && p.title.toLowerCase().includes(q);
      const matchClient = p.client && p.client.toLowerCase().includes(q);
      const matchId = p.id && p.id.toLowerCase().includes(q);
      return matchTitle || matchClient || matchId;
    }
    return true;
  });
});

const paginatedProjects = computed(() => {
  const start = (projectsPage.value - 1) * projectsPageSize.value;
  return filteredProjects.value.slice(start, start + projectsPageSize.value);
});

watch([filterCategory, searchQuery], () => {
  projectsPage.value = 1;
});

onMounted(async () => {
  try {
    await courseStore.fetchAdminProjects();
  } catch (err) {
    console.error("Error loading admin projects:", err);
  }
});

const onCategoryChange = () => {
  if (form.value.category === 'du-an-doanh-nghiep') form.value.categoryName = 'Dự án Doanh nghiệp';
  else if (form.value.category === 'du-an-ca-nhan') form.value.categoryName = 'Dự án Cá nhân';
  else if (form.value.category === 'du-an-nha-nuoc') form.value.categoryName = 'Dự án Khối Cơ quan - Nhà nước';
};

const generateSlug = () => {
  if (isEditing.value) return;
  if (!form.value.title) {
    form.value.id = '';
    return;
  }
  let slug = form.value.title.toLowerCase();
  slug = slug.replace(/á|à|ả|ã|ạ|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ/g, 'a');
  slug = slug.replace(/é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ/g, 'e');
  slug = slug.replace(/i|í|ì|ỉ|ĩ|ị/g, 'i');
  slug = slug.replace(/ó|ò|ỏ|õ|ọ|ô|ố|ồ|ổ|ỗ|ộ|ơ|ớ|ờ|ở|ỡ|ợ/g, 'o');
  slug = slug.replace(/ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự/g, 'u');
  slug = slug.replace(/ý|ỳ|ỷ|ỹ|ỵ/g, 'y');
  slug = slug.replace(/đ/g, 'd');
  slug = slug.replace(/[^a-z0-9\s-]/g, '');
  slug = slug.replace(/\s+/g, '-').replace(/-+/g, '-');
  form.value.id = slug.substring(0, 60);
};

const addContentBlock = (type = 'paragraph') => {
  contentBlocks.value.push({
    type,
    text: '',
    bulletText: ''
  });
};

const removeContentBlock = (idx) => {
  contentBlocks.value.splice(idx, 1);
};

const openAddModal = () => {
  isEditing.value = false;
  editorMode.value = 'rich';
  richHtmlContent.value = '';
  form.value = {
    id: '',
    title: '',
    category: 'du-an-doanh-nghiep',
    categoryName: 'Dự án Doanh nghiệp',
    summary: '',
    image: '',
    date: '',
    client: '',
    driveProfile: ''
  };
  contentBlocks.value = [
    { type: 'paragraph', text: '' }
  ];
  activeView.value = 'form';
};

const editProject = (p) => {
  isEditing.value = true;
  form.value = {
    id: p.id,
    title: p.title || '',
    category: p.category || 'du-an-doanh-nghiep',
    categoryName: p.category_name || 'Dự án Doanh nghiệp',
    summary: p.summary || '',
    image: p.image || '',
    date: p.date || '',
    client: p.client || '',
    driveProfile: p.drive_profile || ''
  };

  // Parse JSON or HTML content
  let rawContent = p.content;
  let parsedBlocks = [];
  let isHtmlString = false;

  if (typeof rawContent === 'string') {
    try {
      const parsed = JSON.parse(rawContent);
      if (Array.isArray(parsed)) {
        parsedBlocks = parsed;
      } else {
        isHtmlString = true;
      }
    } catch (err) {
      isHtmlString = true;
    }
  } else if (Array.isArray(rawContent)) {
    parsedBlocks = rawContent;
  }

  if (isHtmlString) {
    editorMode.value = 'rich';
    richHtmlContent.value = rawContent || '';
  } else {
    // Convert parsed blocks to Rich HTML if they exist
    editorMode.value = 'rich';
    let htmlResult = '';
    parsedBlocks.forEach(b => {
      if (b.type === 'heading') htmlResult += `<h2>${b.text || ''}</h2>`;
      else if (b.type === 'paragraph') htmlResult += `<p>${b.text || ''}</p>`;
      else if (b.type === 'bullets' && Array.isArray(b.items)) {
        htmlResult += `<ul>${b.items.map(i => `<li>${i}</li>`).join('')}</ul>`;
      } else if (b.type === 'html') {
        htmlResult += b.text || '';
      }
    });
    richHtmlContent.value = htmlResult;

    contentBlocks.value = parsedBlocks.map(b => ({
      type: b.type || 'paragraph',
      text: b.text || '',
      bulletText: Array.isArray(b.items) ? b.items.join('\n') : (b.text || '')
    }));
  }

  activeView.value = 'form';
};

const uploadImage = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const url = await courseStore.uploadImage(file);
    form.value.image = url;
    courseStore.showToast('Tải ảnh bìa thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh: ' + err.message, 'error');
  }
};

const saveProject = async () => {
  if (!form.value.id || !form.value.title) {
    courseStore.showToast('Vui lòng nhập ID và Tiêu đề dự án', 'error');
    return;
  }

  let finalContent;

  if (editorMode.value === 'rich') {
    finalContent = richHtmlContent.value || '';
  } else {
    finalContent = contentBlocks.value.map(b => {
      if (b.type === 'bullets') {
        const items = (b.bulletText || '').split('\n').map(s => s.trim()).filter(Boolean);
        return { type: 'bullets', items };
      }
      return { type: b.type || 'paragraph', text: b.text || '' };
    });
  }

  const payload = {
    ...form.value,
    content: finalContent
  };

  saving.value = true;
  try {
    if (isEditing.value) {
      await courseStore.updateAdminProject(form.value.id, payload);
    } else {
      await courseStore.addAdminProject(payload);
    }
    activeView.value = 'list';
  } catch (err) {
    console.error("Save project error:", err);
  } finally {
    saving.value = false;
  }
};

const deleteItem = async (id) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa Dự án',
    message: 'Bạn có chắc chắn muốn xóa Case study / Dự án này?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminProject(id);
    } catch (err) {
      console.error("Delete project error:", err);
    }
  }
};

// ==================== REVIEWS MODERATION METHODS ====================
const pendingReviewsCount = computed(() => {
  return allProjectReviews.value.filter(r => !r.is_approved).length;
});

const approvedReviewsCount = computed(() => {
  return allProjectReviews.value.filter(r => r.is_approved).length;
});

const filteredProjectReviews = computed(() => {
  return allProjectReviews.value.filter(r => {
    // Status Filter
    if (reviewStatusFilter.value === 'pending' && r.is_approved) return false;
    if (reviewStatusFilter.value === 'approved' && !r.is_approved) return false;

    // Project Filter
    if (reviewProjectFilter.value !== 'all' && r.project_id !== reviewProjectFilter.value) return false;

    return true;
  });
});

const paginatedAdminReviews = computed(() => {
  const start = (adminReviewsPage.value - 1) * adminReviewsPageSize.value;
  return filteredProjectReviews.value.slice(start, start + adminReviewsPageSize.value);
});

const openReviewDetailModal = (review) => {
  selectedReviewDetail.value = review;
};

const getProjectTitle = (projectId) => {
  const p = projects.value.find(item => item.id === projectId);
  return p ? p.title : projectId;
};

const formatReviewDate = (dateStr) => {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    return d.toLocaleString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return dateStr;
  }
};

const loadAdminReviews = async () => {
  loadingReviews.value = true;
  try {
    const data = await courseStore.fetchProjectReviewsAdmin();
    allProjectReviews.value = Array.isArray(data) ? data : [];
    adminReviewsPage.value = 1;
  } catch (err) {
    console.error("Error loading project reviews:", err);
  } finally {
    loadingReviews.value = false;
  }
};

const openReviewsTab = () => {
  subTab.value = 'reviews';
  loadAdminReviews();
};

const handleToggleApproval = async (review) => {
  try {
    const updated = await courseStore.toggleProjectReviewApproval(review.id);
    if (updated) {
      review.is_approved = updated.is_approved;
    }
  } catch (e) {
    console.error("Toggle approval error:", e);
  }
};

const handleDeleteReview = async (reviewId) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa nhận xét',
    message: 'Bạn có chắc chắn muốn xóa vĩnh viễn nhận xét này của học viên?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      const ok = await courseStore.deleteProjectReviewAdmin(reviewId);
      if (ok) {
        allProjectReviews.value = allProjectReviews.value.filter(r => r.id !== reviewId);
      }
    } catch (e) {
      console.error("Delete review error:", e);
    }
  }
};
</script>

<style scoped>
.admin-input-style {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
}

/* Excerpt comment in table */
.admin-review-comment-box {
  max-width: 380px;
}

.admin-review-comment-excerpt {
  margin: 0;
  font-size: 13.5px;
  line-height: 1.5;
  color: #334155;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
}

.btn-view-review-detail {
  background: none;
  border: none;
  color: #022b9f;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  padding: 2px 0 0 0;
  display: inline-block;
  transition: color 0.15s;
}

.btn-view-review-detail:hover {
  text-decoration: underline;
  color: #1e40af;
}

/* Admin Detail Modal */
.admin-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.admin-modal-box {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-modal-header {
  padding: 18px 24px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.btn-modal-close {
  background: none;
  border: none;
  font-size: 18px;
  color: #64748b;
  cursor: pointer;
}

.admin-modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-height: 70vh;
  overflow-y: auto;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
}

.detail-label {
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
  min-width: 90px;
}

.detail-comment-section {
  margin-top: 8px;
  padding-top: 14px;
  border-top: 1px solid #f1f5f9;
}

.detail-comment-content {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px;
  font-size: 14.5px;
  line-height: 1.7;
  color: #1e293b;
  white-space: pre-line;
  word-break: break-word;
}

.admin-modal-footer {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
