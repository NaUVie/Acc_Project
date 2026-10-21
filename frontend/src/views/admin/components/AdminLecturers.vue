<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LECTURERS LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Đội ngũ Giảng viên</h2>
          <p>Danh sách các chuyên gia, giảng viên, cố vấn và quản lý các chuyên ngành đào tạo.</p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button 
            @click="isReorderMode = !isReorderMode" 
            class="btn btn-sm"
            :style="{
              background: isReorderMode ? '#0284c7' : '#f1f5f9',
              color: isReorderMode ? '#ffffff' : '#334155',
              border: isReorderMode ? '1px solid #0284c7' : '1px solid #cbd5e1',
              fontWeight: '700',
              padding: '6px 12px',
              fontSize: '13px'
            }"
          >
            {{ isReorderMode ? '✓ Xong' : '↕ Sắp Xếp' }}
          </button>
          <button @click="openMajorsModal" class="btn btn-secondary btn-sm" style="font-weight: 600; padding: 6px 12px; fontSize: 13px;">QL Chuyên Ngành</button>
          <button @click="openAddLecturerModal" class="btn btn-primary btn-sm" style="font-weight: 600; padding: 6px 14px; fontSize: 13px;">+ Thêm</button>
        </div>
      </div>

      <!-- Search & Major Filter Bar -->
      <div class="filter-bar mt-4" style="display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Tìm theo tên, chức danh, chuyên ngành..." 
          class="admin-search-input"
          style="flex: 1; min-width: 200px;"
        />
        
        <!-- Filter by Major -->
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; font-weight: 600;">
          <span>Lọc chuyên ngành:</span>
          <select v-model="selectedMajorFilter" class="admin-input-style" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer; max-width: 230px;">
            <option value="all">Tất cả chuyên ngành ({{ lecturers.length }})</option>
            <option v-for="m in lecturerMajors" :key="m.id" :value="m.id">
              {{ m.name }} ({{ getMajorLecturersCount(m.id) }})
            </option>
          </select>
        </div>

        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; font-weight: 600;">
          <span>Hiển thị:</span>
          <select v-model="pageSize" class="admin-input-style" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer;">
            <option :value="8">8 / trang</option>
            <option :value="20">20 / trang</option>
            <option :value="999">Tất cả (Dễ kéo thả sắp xếp)</option>
          </select>
        </div>
      </div>

      <!-- Table with Up / Down Order Buttons -->
      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 50px; text-align: center;">STT</th>
              <th style="width: 56px;">Avatar</th>
              <th style="min-width: 150px;">Họ & Tên</th>
              <th style="max-width: 200px;">Chức danh / Vị trí</th>
              <th style="max-width: 220px;">Chuyên ngành</th>
              <th style="width: 105px; text-align: center;">Trang chủ</th>
              <th style="width: 90px; text-align: center;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(l, idx) in paginatedLecturers" 
              :key="l.id"
            >
              <td style="text-align: center; width: 80px;">
                <!-- Khi đang ở chế độ Sắp xếp: hiện nút ▲ ▼ -->
                <div v-if="isReorderMode" style="display: inline-flex; align-items: center; justify-content: center; gap: 3px; background: #f0f9ff; padding: 2px 6px; border-radius: 6px; border: 1px solid #bae6fd;">
                  <button 
                    type="button"
                    @click="moveLecturer(l, 'up')"
                    :disabled="isFirstInList(l)"
                    class="btn-arrow"
                    title="Di chuyển lên trên"
                    :style="{
                      opacity: isFirstInList(l) ? '0.3' : '1',
                      cursor: isFirstInList(l) ? 'not-allowed' : 'pointer'
                    }"
                  >
                    ▲
                  </button>
                  <span style="font-weight: 800; font-size: 13px; color: #0284c7; min-width: 20px; text-align: center;">
                    {{ (currentPage - 1) * pageSize + idx + 1 }}
                  </span>
                  <button 
                    type="button"
                    @click="moveLecturer(l, 'down')"
                    :disabled="isLastInList(l)"
                    class="btn-arrow"
                    title="Di chuyển xuống dưới"
                    :style="{
                      opacity: isLastInList(l) ? '0.3' : '1',
                      cursor: isLastInList(l) ? 'not-allowed' : 'pointer'
                    }"
                  >
                    ▼
                  </button>
                </div>
                <!-- Khi bình thường: hiện số thứ tự đơn giản, gọn gàng -->
                <span v-else style="font-weight: 700; font-size: 13px; color: #64748b;">
                  {{ (currentPage - 1) * pageSize + idx + 1 }}
                </span>
              </td>
              <td>
                <img :src="formatImageUrl(l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg')" :alt="l.name" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 14px;">{{ l.name }}</div>
                <div class="text-xs" style="color: #94a3b8; font-size: 11px;">ID: {{ l.id }}</div>
              </td>
              <td style="max-width: 200px;">
                <span 
                  class="badge badge-primary truncate-text" 
                  :title="l.title"
                  style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; font-size: 12px; display: inline-block; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;"
                >
                  {{ l.title }}
                </span>
              </td>
              <td style="max-width: 220px;">
                <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                  <span 
                    v-for="mId in (l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []))" 
                    :key="mId" 
                    class="badge badge-info" 
                    :title="getMajorNameById(mId)"
                    style="background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; font-size: 11px; padding: 2px 7px; border-radius: 6px; max-width: 210px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
                  >
                    {{ getMajorNameById(mId) }}
                  </span>
                  <span v-if="!l.majorIds || l.majorIds.length === 0" style="color: #94a3b8; font-size: 12px;">-- Chưa chọn --</span>
                </div>
              </td>
              <td style="text-align: center;">
                <button 
                  type="button" 
                  @click="toggleFeatured(l)" 
                  class="btn btn-xs" 
                  :style="{
                    background: l.is_featured ? '#fef3c7' : '#f1f5f9',
                    color: l.is_featured ? '#b45309' : '#64748b',
                    border: l.is_featured ? '1px solid #fde68a' : '1px solid #cbd5e1',
                    borderRadius: '20px',
                    padding: '3px 10px',
                    fontWeight: '700',
                    cursor: 'pointer',
                    fontSize: '11px',
                    whiteSpace: 'nowrap'
                  }"
                >
                  {{ l.is_featured ? '⭐ Nổi bật' : '☆ Thường' }}
                </button>
              </td>
              <td style="text-align: center;">
                <div class="action-buttons" style="justify-content: center; gap: 6px;">
                  <button @click="editLecturer(l)" class="btn-action edit" title="Sửa thông tin">✏️</button>
                  <button @click="deleteLecturer(l)" class="btn-action delete" title="Xóa">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredLecturers.length === 0">
              <td colspan="7" class="text-center py-8 text-muted">Không tìm thấy giảng viên nào.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Component -->
      <Pagination 
        :currentPage="currentPage" 
        :totalItems="filteredLecturers.length" 
        :pageSize="pageSize" 
        @update:currentPage="currentPage = $event"
      />
    </div>

    <!-- VIEW 2: LECTURER ADD/EDIT FORM -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa thông tin giảng viên' : 'Thêm giảng viên mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveLecturer">
        <div class="grid-2">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Mã định danh (ID Slug)</label>
            <input v-model="lecturerForm.id" :disabled="isEditing" type="text" required class="admin-input-style" placeholder="ví dụ: le-quang-trieu" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <small v-if="!isEditing" class="text-muted">Mã ID duy nhất không dấu, ví dụ: le-van-a</small>
          </div>
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Họ và Tên Giảng viên</label>
            <input v-model="lecturerForm.name" @input="onNameInput" type="text" required class="admin-input-style" placeholder="ví dụ: Lê Quang Triều" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Chức danh / Vị trí công tác</label>
          <input v-model="lecturerForm.title" type="text" required class="admin-input-style" placeholder="ví dụ: Chuyên gia Khai phá Dữ liệu & AI Agent" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Chuyên ngành đào tạo (Có thể tích chọn nhiều chuyên ngành)</label>
          <div style="display: flex; gap: 12px 20px; flex-wrap: wrap; margin-top: 6px; background: #f8fafc; padding: 14px 18px; border-radius: 10px; border: 1px solid #cbd5e1;">
            <label 
              v-for="m in lecturerMajors" 
              :key="m.id" 
              style="display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; font-weight: 600; color: #334155; cursor: pointer; user-select: none;"
            >
              <input 
                type="checkbox" 
                :value="m.id" 
                v-model="lecturerForm.majorIds" 
                style="width: 17px; height: 17px; cursor: pointer; accent-color: #0284c7;" 
              />
              <span>{{ m.name }}</span>
            </label>
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Hình ảnh Avatar (Tải từ máy hoặc dán URL)</label>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input v-model="lecturerForm.avatar" type="text" required class="admin-input-style" placeholder="/images/default-avatar.jpg hoặc URL Cloudinary" style="flex: 1; min-width: 240px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <label class="btn btn-primary btn-sm" style="padding: 10px 16px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600;">
              <span>Tải ảnh từ máy</span>
              <input type="file" accept="image/*" @change="uploadAvatar" style="display: none;" />
            </label>
          </div>
          <div v-if="uploadingAvatar" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
            Đang tải ảnh lên Cloudinary...
          </div>
          <div v-if="lecturerForm.avatar" class="mt-2">
            <img :src="formatImageUrl(lecturerForm.avatar)" alt="Preview" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Tiêu đề ngắn / Tagline</label>
          <input v-model="lecturerForm.tagline" type="text" class="admin-input-style" placeholder="ví dụ: 10+ năm kinh nghiệm cố vấn Chuyển đổi số doanh nghiệp" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3" style="display: flex; align-items: center; gap: 8px;">
          <input type="checkbox" id="is_featured_chk" v-model="lecturerForm.is_featured" style="width: 18px; height: 18px; cursor: pointer;" />
          <label for="is_featured_chk" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">Hiển thị nổi bật ngoài Trang chủ (Tối đa 4 người)</label>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Giới thiệu tóm tắt (Bio Short)</label>
          <textarea v-model="lecturerForm.bioShort" rows="3" class="admin-input-style" placeholder="Đoạn mô tả tóm tắt quá trình công tác, thành tựu..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        </div>

        <!-- Position Settings -->
        <div class="form-group mt-3" style="background: #f8fafc; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 700; color: #0f172a;">
            🔢 Cài đặt Thứ tự hiển thị
          </h4>
          <div class="grid-2">
            <div class="form-group">
              <label style="color: #1e293b; font-weight: 600; font-size: 13px;">Thứ tự chung (Trang Tất cả chuyên ngành)</label>
              <input 
                v-model.number="lecturerForm.position" 
                type="number" 
                min="1" 
                class="admin-input-style" 
                placeholder="1, 2, 3..." 
                style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
              />
              <small class="text-muted">Vị trí hiển thị tại danh sách Tất cả.</small>
            </div>
          </div>

          <div v-if="lecturerForm.majorIds && lecturerForm.majorIds.length > 0" class="mt-3">
            <label style="color: #1e293b; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;">
              Thứ tự riêng theo từng chuyên ngành đã chọn:
            </label>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px;">
              <div 
                v-for="mId in lecturerForm.majorIds" 
                :key="mId"
                style="background: #ffffff; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; display: flex; align-items: center; justify-content: space-between; gap: 10px;"
              >
                <span style="font-size: 12.5px; font-weight: 600; color: #334155;">{{ getMajorNameById(mId) }}</span>
                <div style="display: flex; align-items: center; gap: 6px;">
                  <span style="font-size: 12px; color: #64748b;">Số:</span>
                  <input 
                    type="number" 
                    min="1" 
                    :value="lecturerForm.major_positions ? lecturerForm.major_positions[mId] : ''"
                    @input="updateFormMajorPos(mId, $event.target.value)"
                    class="admin-input-style" 
                    placeholder="Mặc định"
                    style="width: 75px; text-align: center; padding: 4px 8px; font-size: 13px; font-weight: 700; color: #0284c7;"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
          <button type="submit" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu thông tin giảng viên</button>
        </div>
      </form>
    </div>

    <!-- MODAL LECTURER MAJORS CRUD -->
    <div v-if="showMajorsModal" class="modal-overlay" @click.self="closeMajorsModal">
      <div class="modal-content animate-fade-in" style="max-width: 700px;">
        <div class="modal-header">
          <h3>Quản lý Chuyên ngành Giảng viên (Database)</h3>
          <button class="close-btn" @click="closeMajorsModal">&times;</button>
        </div>

        <div class="modal-body" style="padding: 16px 0;">
          <!-- Form Create / Edit Major -->
          <form @submit.prevent="saveMajor" style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
            <h4 style="margin-top: 0; margin-bottom: 12px; font-size: 15px; color: #0f172a; font-weight: 700;">
              {{ isEditingMajor ? 'Chỉnh sửa chuyên ngành' : 'Thêm chuyên ngành mới' }}
            </h4>
            
            <div class="grid-2">
              <div class="form-group">
                <label style="font-size: 12px; font-weight: 600; color: #475569;">Mã ID chuyên ngành (Slug)</label>
                <input 
                  v-model="majorForm.id" 
                  :disabled="isEditingMajor" 
                  type="text" 
                  required 
                  class="admin-input-style" 
                  placeholder="tai-chinh-lanh-dao" 
                  style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
                />
              </div>
              <div class="form-group">
                <label style="font-size: 12px; font-weight: 600; color: #475569;">Tên chuyên ngành</label>
                <input 
                  v-model="majorForm.name" 
                  @input="onMajorNameInput" 
                  type="text" 
                  required 
                  class="admin-input-style" 
                  placeholder="QUẢN TRỊ - TÀI CHÍNH" 
                  style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
                />
              </div>
            </div>

            <div class="grid-2 mt-2">
              <div class="form-group">
                <label style="font-size: 12px; font-weight: 600; color: #475569;">Nhãn Badge Header</label>
                <input 
                  v-model="majorForm.badge" 
                  type="text" 
                  class="admin-input-style" 
                  placeholder="QUẢN TRỊ - TÀI CHÍNH" 
                  style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
                />
              </div>
              <div class="form-group">
                <label style="font-size: 12px; font-weight: 600; color: #475569;">Mô tả ngắn chuyên ngành</label>
                <input 
                  v-model="majorForm.description" 
                  type="text" 
                  class="admin-input-style" 
                  placeholder="Đội ngũ chuyên gia chuyên sâu thuộc..." 
                  style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
                />
              </div>
            </div>

            <div class="mt-3" style="display: flex; gap: 8px; justify-content: flex-end;">
              <button v-if="isEditingMajor" type="button" class="btn btn-secondary btn-xs" @click="resetMajorForm">Hủy sửa</button>
              <button type="submit" class="btn btn-primary btn-xs" style="padding: 6px 16px; font-weight: 700;">
                {{ isEditingMajor ? 'Cập nhật chuyên ngành' : 'Tạo mới' }}
              </button>
            </div>
          </form>

          <!-- Majors List Table -->
          <div class="table-responsive">
            <table class="admin-table" style="font-size: 13px;">
              <thead>
                <tr>
                  <th>ID Slug</th>
                  <th>Tên Chuyên ngành</th>
                  <th>Số Giảng viên</th>
                  <th class="text-right">Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="m in lecturerMajors" :key="m.id">
                  <td><code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #0284c7;">{{ m.id }}</code></td>
                  <td><strong>{{ m.name }}</strong></td>
                  <td><span class="badge badge-info">{{ getMajorLecturersCount(m.id) }} người</span></td>
                  <td class="text-right">
                    <div class="action-buttons" style="justify-content: flex-end;">
                      <button @click="editMajor(m)" class="btn-action edit" title="Sửa">✏️</button>
                      <button @click="deleteMajor(m)" class="btn-action delete" title="Xóa">🗑️</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="lecturerMajors.length === 0">
                  <td colspan="5" class="text-center py-4 text-muted">Chưa có chuyên ngành nào trong Database.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="modal-footer" style="display: flex; justify-content: flex-end;">
          <button type="button" class="btn btn-secondary" @click="closeMajorsModal">Đóng</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();

const isReorderMode = ref(false);

const lecturers = computed(() => courseStore.lecturers || []);
const lecturerMajors = computed(() => courseStore.lecturerMajors || []);

const localLecturers = ref([]);

watch(lecturers, (newList) => {
  localLecturers.value = [...newList];
}, { immediate: true });

const featuredCount = computed(() => {
  return lecturers.value.filter(l => l.is_featured).length;
});

const getMajorNameById = (id) => {
  if (!id) return 'Chuyên gia';
  const match = lecturerMajors.value.find(m => m.id === id);
  return match ? match.name : id;
};

const getMajorLecturersCount = (majorId) => {
  return lecturers.value.filter(l => {
    const ids = l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []);
    return ids.includes(majorId);
  }).length;
};

const isFirstInList = (l) => {
  const list = filteredLecturers.value;
  return list.length > 0 && list[0].id === l.id;
};

const isLastInList = (l) => {
  const list = filteredLecturers.value;
  return list.length > 0 && list[list.length - 1].id === l.id;
};

const moveLecturer = async (l, direction) => {
  const list = [...filteredLecturers.value];
  const currentIndex = list.findIndex(item => item.id === l.id);
  if (currentIndex === -1) return;

  const targetIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
  if (targetIndex < 0 || targetIndex >= list.length) return;

  // Swap elements
  const temp = list[currentIndex];
  list[currentIndex] = list[targetIndex];
  list[targetIndex] = temp;

  const majorId = selectedMajorFilter.value;

  if (majorId !== 'all') {
    // Map new positions 1..N in this major
    const posMap = new Map();
    const updates = [];
    list.forEach((item, idx) => {
      const pos = idx + 1;
      posMap.set(item.id, pos);
      updates.push({ id: item.id, position: pos });
    });

    // Instant local UI update
    localLecturers.value = localLecturers.value.map(item => {
      if (posMap.has(item.id)) {
        return {
          ...item,
          major_positions: {
            ...(item.major_positions || {}),
            [majorId]: posMap.get(item.id)
          }
        };
      }
      return item;
    });

    try {
      await courseStore.reorderLecturers(updates, majorId);
    } catch (err) {
      courseStore.showToast('Không thể lưu thứ tự.', 'error');
    }
  } else {
    // Global swap
    const fullList = [...localLecturers.value];
    const fromIdx = fullList.findIndex(item => item.id === l.id);
    const toLecturer = list[currentIndex]; // the one that took l's place
    const toIdx = fullList.findIndex(item => item.id === toLecturer.id);

    // Swap in full list
    if (fromIdx !== -1 && toIdx !== -1) {
      const tempFull = fullList[fromIdx];
      fullList[fromIdx] = fullList[toIdx];
      fullList[toIdx] = tempFull;
    }

    const posMap = new Map();
    const updates = [];
    fullList.forEach((item, idx) => {
      const pos = idx + 1;
      posMap.set(item.id, pos);
      updates.push({ id: item.id, position: pos });
    });

    localLecturers.value = localLecturers.value.map(item => {
      if (posMap.has(item.id)) {
        return {
          ...item,
          position: posMap.get(item.id)
        };
      }
      return item;
    });

    try {
      await courseStore.reorderLecturers(updates, 'all');
    } catch (err) {
      courseStore.showToast('Không thể lưu thứ tự.', 'error');
    }
  }
};

const updateFormMajorPos = (mId, val) => {
  const num = parseInt(val, 10);
  const current = { ...(lecturerForm.value.major_positions || {}) };
  if (!isNaN(num) && num > 0) {
    current[mId] = num;
  } else {
    delete current[mId];
  }
  lecturerForm.value.major_positions = current;
};

// Drag and drop state & handlers
const draggedIndex = ref(null);
const dragOverIndex = ref(null);

const onDragStart = (e, index) => {
  const globalIndex = (currentPage.value - 1) * pageSize.value + index;
  draggedIndex.value = globalIndex;
  e.dataTransfer.effectAllowed = 'move';
};

const onDragOver = (e, index) => {
  const globalIndex = (currentPage.value - 1) * pageSize.value + index;
  dragOverIndex.value = globalIndex;
};

const onDrop = async (e, targetIndex) => {
  const globalTargetIndex = (currentPage.value - 1) * pageSize.value + targetIndex;
  if (draggedIndex.value === null || draggedIndex.value === globalTargetIndex) {
    draggedIndex.value = null;
    dragOverIndex.value = null;
    return;
  }

  const currentFiltered = [...filteredLecturers.value];
  const draggedItem = currentFiltered[draggedIndex.value];
  const targetItem = currentFiltered[globalTargetIndex];

  draggedIndex.value = null;
  dragOverIndex.value = null;

  if (selectedMajorFilter.value !== 'all') {
    // Reorder within the specific major
    currentFiltered.splice(draggedIndex.value, 1);
    const newTargetIdx = currentFiltered.findIndex(item => item.id === targetItem.id);
    currentFiltered.splice(newTargetIdx >= 0 ? newTargetIdx : currentFiltered.length, 0, draggedItem);

    // Update localLecturers' major_positions for immediate reactive UI
    const majorId = selectedMajorFilter.value;
    const posMap = new Map();
    currentFiltered.forEach((item, idx) => {
      posMap.set(item.id, idx + 1);
    });

    localLecturers.value = localLecturers.value.map(l => {
      if (posMap.has(l.id)) {
        return {
          ...l,
          major_positions: {
            ...(l.major_positions || {}),
            [majorId]: posMap.get(l.id)
          }
        };
      }
      return l;
    });

    try {
      await courseStore.reorderLecturers(currentFiltered, majorId);
      courseStore.showToast('Đã cập nhật thứ tự giảng viên theo chuyên ngành!', 'success');
    } catch (err) {
      courseStore.showToast('Không thể cập nhật thứ tự.', 'error');
    }
  } else {
    // Reorder in full global list
    const fullList = [...localLecturers.value];
    const fromIdx = fullList.findIndex(item => item.id === draggedItem.id);
    fullList.splice(fromIdx, 1);
    const toIdx = fullList.findIndex(item => item.id === targetItem.id);
    fullList.splice(toIdx >= 0 ? toIdx : fullList.length, 0, draggedItem);
    localLecturers.value = fullList;

    try {
      await courseStore.reorderLecturers(localLecturers.value, 'all');
      courseStore.showToast('Đã cập nhật thứ tự hiển thị giảng viên!', 'success');
    } catch (err) {
      courseStore.showToast('Không thể cập nhật thứ tự.', 'error');
    }
  }
};

const toggleFeatured = async (l) => {
  try {
    const updated = await courseStore.toggleLecturerFeatured(l.id);
    const isNowFeatured = updated ? updated.is_featured : !l.is_featured;
    courseStore.showToast(isNowFeatured ? `Đã gắn mác Nổi bật Trang chủ cho ${l.name}` : `Đã bỏ Nổi bật đối với ${l.name}`, 'info');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể thay đổi trạng thái nổi bật.', 'error');
  }
};

const searchQuery = ref('');
const selectedMajorFilter = ref('all');
const currentPage = ref(1);
const pageSize = ref(8);

watch([searchQuery, selectedMajorFilter, pageSize], () => {
  currentPage.value = 1;
});

const filteredLecturers = computed(() => {
  const list = localLecturers.value.filter(l => {
    // Filter by Major
    if (selectedMajorFilter.value !== 'all') {
      const ids = l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []);
      if (!ids.includes(selectedMajorFilter.value)) {
        return false;
      }
    }

    // Filter by search query
    const q = (searchQuery.value || '').toLowerCase().trim();
    const lName = (l.name || '').toLowerCase();
    const lTitle = (l.title || '').toLowerCase();
    const lId = (l.id || '').toString().toLowerCase();
    const mNames = (l.majorIds || [l.majorId]).filter(Boolean).map(mId => getMajorNameById(mId).toLowerCase()).join(' ');
    return !q || 
           lName.includes(q) || 
           lTitle.includes(q) ||
           mNames.includes(q) ||
           lId.includes(q);
  });

  if (selectedMajorFilter.value !== 'all') {
    const majorId = selectedMajorFilter.value;
    return list.slice().sort((a, b) => {
      const posA = a.major_positions && a.major_positions[majorId] !== undefined ? a.major_positions[majorId] : (a.position ?? 999);
      const posB = b.major_positions && b.major_positions[majorId] !== undefined ? b.major_positions[majorId] : (b.position ?? 999);
      if (posA !== posB) return posA - posB;
      return (a.name || '').localeCompare(b.name || '', 'vi');
    });
  }

  return list.slice().sort((a, b) => {
    const posA = a.position ?? 999;
    const posB = b.position ?? 999;
    if (posA !== posB) return posA - posB;
    return (a.name || '').localeCompare(b.name || '', 'vi');
  });
});

const paginatedLecturers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredLecturers.value.slice(start, start + pageSize.value);
});

const activeView = ref('list'); // 'list' | 'form'
const isEditing = ref(false);
const uploadingAvatar = ref(false);

const lecturerForm = ref({
  id: '',
  name: '',
  title: '',
  tagline: '',
  avatar: '',
  avatarDriveLink: '',
  driveProfile: '',
  bioShort: '',
  detailsHtml: '',
  majorId: '',
  majorIds: [],
  position: 0,
  major_positions: {},
  is_featured: false
});

const onNameInput = () => {
  if (!isEditing.value) {
    lecturerForm.value.id = slugify(lecturerForm.value.name);
  }
};

onMounted(async () => {
  await Promise.all([
    courseStore.fetchLecturerMajors(),
    courseStore.fetchLecturers()
  ]);
});

const openAddLecturerModal = () => {
  isEditing.value = false;
  lecturerForm.value = {
    id: '',
    name: '',
    title: '',
    tagline: '',
    avatar: '/images/default-avatar.jpg',
    avatarDriveLink: '',
    driveProfile: '',
    bioShort: '',
    detailsHtml: '',
    majorId: lecturerMajors.value.length > 0 ? lecturerMajors.value[0].id : '',
    majorIds: lecturerMajors.value.length > 0 ? [lecturerMajors.value[0].id] : [],
    position: (lecturers.value.length || 0) + 1,
    major_positions: {},
    is_featured: false
  };
  activeView.value = 'form';
};

const editLecturer = (l) => {
  isEditing.value = true;
  const initialMajorIds = l.majorIds && l.majorIds.length > 0 ? [...l.majorIds] : (l.majorId ? [l.majorId] : []);
  lecturerForm.value = {
    id: l.id,
    name: l.name,
    title: l.title,
    tagline: l.tagline || '',
    avatar: l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg',
    avatarDriveLink: l.avatar_drive_link || '',
    driveProfile: l.drive_profile || '',
    bioShort: l.bio_short || '',
    detailsHtml: l.details_html || '',
    majorId: l.majorId || '',
    majorIds: initialMajorIds,
    position: l.position ?? 1,
    major_positions: l.major_positions ? { ...l.major_positions } : {},
    is_featured: l.is_featured || false
  };
  activeView.value = 'form';
};

const uploadAvatar = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadingAvatar.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    lecturerForm.value.avatar = url;
    courseStore.showToast('Tải ảnh đại diện thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi tải ảnh: ' + err.message, 'error');
  } finally {
    uploadingAvatar.value = false;
  }
};

const saveLecturer = async () => {
  try {
    if (!lecturerForm.value.id.trim()) {
      courseStore.showToast('Vui lòng nhập mã ID duy nhất!', 'warning');
      return;
    }
    const payload = {
      ...lecturerForm.value,
      avatar: formatImageUrl(lecturerForm.value.avatar)
    };
    if (isEditing.value) {
      await courseStore.updateAdminLecturer(payload.id, payload);
      courseStore.showToast('Cập nhật giảng viên thành công!', 'success');
    } else {
      if (lecturers.value.some(l => l.id === payload.id)) {
        courseStore.showToast('Mã ID này đã được sử dụng!', 'warning');
        return;
      }
      await courseStore.addAdminLecturer(payload);
      courseStore.showToast('Thêm giảng viên mới thành công!', 'success');
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu giảng viên.', 'error');
  }
};

const deleteLecturer = async (l) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa giảng viên',
    message: `Bạn có chắc chắn muốn xóa giảng viên "${l.name}" khỏi hệ thống?`,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminLecturer(l.id);
      courseStore.showToast(`Đã xóa giảng viên "${l.name}" thành công.`, 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa giảng viên.', 'error');
    }
  }
};

// --- LECTURER MAJORS CRUD MODAL STATE & ACTIONS ---
const showMajorsModal = ref(false);
const isEditingMajor = ref(false);
const majorForm = ref({
  id: '',
  name: '',
  icon: '',
  badge: '',
  description: '',
  position: 0
});

const openMajorsModal = () => {
  resetMajorForm();
  showMajorsModal.value = true;
};

const closeMajorsModal = () => {
  showMajorsModal.value = false;
};

const resetMajorForm = () => {
  isEditingMajor.value = false;
  majorForm.value = {
    id: '',
    name: '',
    icon: '',
    badge: '',
    description: '',
    position: 0
  };
};

const onMajorNameInput = () => {
  if (!isEditingMajor.value) {
    majorForm.value.id = slugify(majorForm.value.name);
    majorForm.value.badge = majorForm.value.name.toUpperCase();
  }
};

const editMajor = (m) => {
  isEditingMajor.value = true;
  majorForm.value = {
    id: m.id,
    name: m.name,
    icon: m.icon || '',
    badge: m.badge || m.name.toUpperCase(),
    description: m.description || '',
    position: m.position || 0
  };
};

const saveMajor = async () => {
  try {
    if (!majorForm.value.id.trim() || !majorForm.value.name.trim()) {
      courseStore.showToast('Vui lòng nhập tên và mã chuyên ngành!', 'warning');
      return;
    }
    if (isEditingMajor.value) {
      await courseStore.updateAdminLecturerMajor(majorForm.value.id, majorForm.value);
      courseStore.showToast('Cập nhật chuyên ngành thành công!', 'success');
    } else {
      if (lecturerMajors.value.some(m => m.id === majorForm.value.id)) {
        courseStore.showToast('Mã ID chuyên ngành này đã tồn tại!', 'warning');
        return;
      }
      await courseStore.addAdminLecturerMajor(majorForm.value);
      courseStore.showToast('Thêm chuyên ngành mới thành công!', 'success');
    }
    resetMajorForm();
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi lưu chuyên ngành.', 'error');
  }
};

const deleteMajor = async (m) => {
  const count = getMajorLecturersCount(m.id);
  let msg = `Bạn có chắc chắn muốn xóa chuyên ngành "${m.name}"?`;
  if (count > 0) {
    msg += `\n\nĐang có ${count} giảng viên thuộc chuyên ngành này. Sau khi xóa, các giảng viên sẽ trở về trạng thái chưa thuộc chuyên ngành.`;
  }
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa chuyên ngành giảng viên',
    message: msg,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminLecturerMajor(m.id);
      courseStore.showToast(`Đã xóa chuyên ngành "${m.name}".`, 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Lỗi khi xóa chuyên ngành.', 'error');
    }
  }
};
</script>

<style scoped>
.btn-arrow {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  border-radius: 6px;
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  line-height: 1;
  transition: all 0.15s ease;
  user-select: none;
}
.btn-arrow:hover:not(:disabled) {
  background: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
  transform: scale(1.08);
}
</style>