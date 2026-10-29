<template>
  <div class="tab-content animate-fade-in">
    <!-- SUB-NAV: TẤT CẢ VS THEO HÀNG -->
    <div class="mb-4" style="display: flex; gap: 10px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; flex-wrap: wrap;">
      <button 
        type="button" 
        @click="filterRowType = 'all'" 
        class="btn btn-sm"
        :class="filterRowType === 'all' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Tất cả ({{ partners.length }})
      </button>
      <button 
        type="button" 
        @click="filterRowType = 'top_fixed'" 
        class="btn btn-sm" 
        :class="filterRowType === 'top_fixed' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Hàng trên cố định ({{ topFixedCount }}/6)
      </button>
      <button 
        type="button" 
        @click="filterRowType = 'marquee'" 
        class="btn btn-sm"
        :class="filterRowType === 'marquee' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Hàng giữa chạy Marquee ({{ marqueeCount }})
      </button>
      <button 
        type="button" 
        @click="filterRowType = 'bottom_fixed'" 
        class="btn btn-sm"
        :class="filterRowType === 'bottom_fixed' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Hàng dưới cố định ({{ bottomFixedCount }}/6)
      </button>
    </div>

    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Đối tác & Doanh nghiệp hợp tác ({{ partners.length }})</h2>
          <p>
            Trang chủ hiển thị 3 hàng: <strong>Hàng trên</strong> (cố định 6 đối tác), <strong>Hàng giữa</strong> (chạy vô tận Marquee), và <strong>Hàng dưới</strong> (cố định 6 đối tác).
          </p>
        </div>
        <div style="display: flex; gap: 10px;">
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Đối tác mới</button>
        </div>
      </div>

      <!-- SEARCH & FILTER BAR -->
      <div class="table-search-bar mt-4 mb-4" style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="admin-input-style" 
          placeholder="Tìm kiếm theo tên đối tác..." 
          style="max-width: 300px; padding: 8px 14px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        />
        <select 
          v-model="filterStatus" 
          class="admin-input-style"
          style="max-width: 170px; padding: 8px 12px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        >
          <option value="all">Tất cả trạng thái</option>
          <option value="active">Đang hiển thị</option>
          <option value="hidden">Đã ẩn</option>
        </select>
        <select 
          v-model="filterRowType" 
          class="admin-input-style"
          style="max-width: 220px; padding: 8px 12px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        >
          <option value="all">Tất cả vị trí hiển thị</option>
          <option value="top_fixed">Hàng trên cố định (Top 6)</option>
          <option value="marquee">Hàng giữa chạy Marquee</option>
          <option value="bottom_fixed">Hàng dưới cố định (Bottom 6)</option>
        </select>
        <span class="text-muted" style="font-size: 13.5px; margin-left: auto;">
          Hiển thị <strong>{{ filteredPartners.length }}</strong> / {{ partners.length }} đối tác
        </span>
      </div>

      <!-- Partners Table -->
      <div class="table-responsive mt-2">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 70px;">Thứ tự</th>
              <th style="width: 140px;">Logo</th>
              <th>Tên doanh nghiệp / Đối tác</th>
              <th style="width: 190px;">Vị trí hàng</th>
              <th>Liên kết (Link website)</th>
              <th style="width: 140px;">Trạng thái</th>
              <th style="width: 110px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in paginatedPartners" :key="p.id">
              <td class="font-bold text-center">
                <span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
                  #{{ p.position }}
                </span>
              </td>
              <td>
                <div style="width: 110px; height: 50px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; padding: 4px;">
                  <img :src="formatImageUrl(p.src)" :alt="p.name" @error="handleLogoError" style="max-width: 100%; max-height: 100%; object-fit: contain;" referrerpolicy="no-referrer" />
                </div>
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ p.name }}</div>
                <small class="text-muted" style="font-size: 12px;">ID: #{{ p.id }}</small>
              </td>
              <td>
                <span 
                  class="badge" 
                  :style="getRowBadgeStyle(p.row_type)"
                  style="font-weight: 700; padding: 5px 10px; border-radius: 6px; display: inline-flex; align-items: center; gap: 4px;"
                >
                  {{ getRowLabel(p.row_type) }}
                </span>
              </td>
              <td>
                <a v-if="p.link" :href="p.link" target="_blank" rel="noopener" style="color: #0284c7; word-break: break-all; font-size: 13.5px; text-decoration: underline;">
                  {{ p.link }}
                </a>
                <span v-else class="text-muted" style="font-size: 13px;">(Chưa có link)</span>
              </td>
              <td>
                <button 
                  @click="toggleActive(p)" 
                  class="badge" 
                  :style="p.is_active ? 'background: #dcfce7; color: #15803d; border: none; cursor: pointer; padding: 6px 12px;' : 'background: #fee2e2; color: #b91c1c; border: none; cursor: pointer; padding: 6px 12px;'"
                  title="Nhấn để đổi trạng thái"
                >
                  {{ p.is_active ? 'Đang hiển thị' : 'Đã ẩn' }}
                </button>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="openCropper(p.src, async (url) => { await courseStore.updatePartner(p.id, { src: url }); p.src = url; courseStore.showToast('Đã cắt và cập nhật logo đối tác!', 'success'); }, 'partner', '✂ Cắt Logo Đối Tác: ' + p.name)" class="btn-action edit" title="Cắt lại logo" style="color: #0284c7;">✂️</button>
                  <button @click="editPartner(p)" class="btn-action edit" title="Sửa Đối tác">✏️</button>
                  <button @click="deletePartnerItem(p.id)" class="btn-action delete" title="Xóa Đối tác">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredPartners.length === 0">
              <td colspan="7" class="text-center py-8 text-muted">
                {{ searchQuery ? 'Không tìm thấy đối tác nào phù hợp với từ khóa.' : 'Chưa có đối tác nào trong danh mục này.' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding: 12px 0;">
        <span class="text-muted" style="font-size: 13.5px;">
          Trang <strong>{{ currentPage }}</strong> / {{ totalPages }}
        </span>
        <div style="display: flex; gap: 6px;">
          <button 
            type="button" 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="btn btn-secondary btn-sm"
          >
            ← Trước
          </button>
          <button 
            v-for="page in visiblePages" 
            :key="page"
            type="button"
            @click="currentPage = page"
            class="btn btn-sm"
            :class="currentPage === page ? 'btn-primary' : 'btn-secondary'"
            style="min-width: 32px;"
          >
            {{ page }}
          </button>
          <button 
            type="button" 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="btn btn-secondary btn-sm"
          >
            Sau →
          </button>
        </div>
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
            {{ isEditing ? 'Chỉnh sửa Doanh nghiệp / Đối tác' : 'Thêm Doanh nghiệp / Đối tác mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="savePartner" class="mt-2">
        <div class="grid grid-2 gap-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Tên Doanh nghiệp / Đối tác <span style="color: #e11d48;">*</span></label>
            <input 
              v-model="form.name" 
              type="text" 
              required 
              class="admin-input-style" 
              placeholder="Ví dụ: Tập đoàn Vinamilk" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Vị trí hàng hiển thị trên Home <span style="color: #e11d48;">*</span></label>
            <select 
              v-model="form.row_type" 
              class="admin-input-style"
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 600;"
            >
              <option value="top_fixed">Hàng trên cố định (Tối đa 6 đối tác)</option>
              <option value="marquee">Hàng giữa chạy vô tận (Marquee)</option>
              <option value="bottom_fixed">Hàng dưới cố định (Tối đa 6 đối tác)</option>
            </select>
            <small class="text-muted" style="display: block; margin-top: 4px;">
              {{ form.row_type === 'top_fixed' ? 'Sẽ hiển thị cố định ở hàng trên cùng của trang chủ.' : (form.row_type === 'bottom_fixed' ? 'Sẽ hiển thị cố định ở hàng dưới cùng của trang chủ.' : 'Sẽ chạy cuộn liên tục ở hàng giữa.') }}
            </small>
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Logo Doanh nghiệp (URL hoặc tải lên) <span style="color: #e11d48;">*</span></label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input 
                v-model="form.src" 
                type="text" 
                required 
                class="admin-input-style" 
                placeholder="https://... hoặc /images/..." 
                style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
              />
              <input type="file" ref="logoFileRef" @change="onFileSelectForCrop($event, (url) => { form.src = url; }, 'partner', '✂ Cắt & Căn Chỉnh Logo Đối Tác')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.logoFileRef.click()" class="btn btn-secondary btn-sm" :disabled="uploadingLogo">
                {{ uploadingLogo ? 'Đang tải...' : 'Upload Logo' }}
              </button>
            </div>
            <div v-if="form.src" style="margin-top: 10px; display: flex; align-items: center; gap: 12px; padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;">
              <img :src="formatImageUrl(form.src)" alt="Logo Preview" @error="handleLogoError" style="max-height: 60px; max-width: 160px; object-fit: contain;" referrerpolicy="no-referrer" />
              <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.src, (url) => { form.src = url; }, 'partner', '✂ Cắt & Căn Chỉnh Logo Đối Tác')">✂ Cắt lại logo</button>
            </div>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Thứ tự sắp xếp (Position)</label>
            <input 
              v-model.number="form.position" 
              type="number" 
              min="0" 
              class="admin-input-style" 
              placeholder="1, 2, 3..." 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
            <small class="text-muted" style="display: block; margin-top: 4px;">Số nhỏ hơn hiển thị trước từ trái qua phải.</small>
          </div>
        </div>

        <div class="form-group mt-4">
          <label style="color: #1e293b; font-weight: 600;">Đường dẫn website doanh nghiệp (Link ngoài - Tùy chọn)</label>
          <input 
            v-model="form.link" 
            type="text" 
            class="admin-input-style" 
            placeholder="Ví dụ: https://vinamilk.com.vn" 
            style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
          />
          <small class="text-muted" style="display: block; margin-top: 4px;">Nếu có link, khi học viên click vào logo ở trang chủ sẽ được chuyển sang website của đối tác trong tab mới.</small>
        </div>

        <div class="mt-4" style="background: #f8fafc; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0;">
          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_active" type="checkbox" id="partner_active" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="partner_active" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">
              Hiển thị Logo này trên trang chủ (Kích hoạt)
            </label>
          </div>
        </div>

        <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary">Hủy</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Đối tác' : 'Tạo Đối tác') }}
          </button>
        </div>
      </form>
    </div>
    <!-- Image Cropper Modal -->
    <ImageCropperModal :isOpen="isCropperOpen" :imageUrl="cropTargetUrl" :aspectRatio="cropAspectRatio" :title="cropModalTitle" @close="isCropperOpen = false" @cropped="handleCroppedImage" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const courseStore = useCourseStore();

const handleLogoError = (e) => {
  const img = e.target;
  if (!img || img.dataset.retried) return;
  img.dataset.retried = 'true';
  const m = img.src.match(/(?:d\/|[?&]id=)([a-zA-Z0-9_-]+)/);
  if (m && m[1]) {
    const fileId = m[1];
    if (img.src.includes('lh3.googleusercontent.com')) {
      img.src = `https://drive.google.com/thumbnail?id=${fileId}&sz=w400`;
    } else {
      img.src = `https://lh3.googleusercontent.com/d/${fileId}=s400`;
    }
  }
};


// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('partner');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Logo Đối Tác');
let cropTargetCallback = null;

const openCropper = (url, callback, ratio = 'partner', title = '✂ Cắt & Căn Chỉnh Logo Đối Tác') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'partner', title = '✂ Cắt & Căn Chỉnh Logo Đối Tác') => {
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


const activeView = ref('list');
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);
const uploadingLogo = ref(false);
const logoFileRef = ref(null);

const searchQuery = ref('');
const filterStatus = ref('all');
const filterRowType = ref('all');
const currentPage = ref(1);
const pageSize = 20;

const form = ref({
  name: '',
  src: '',
  link: '',
  position: 1,
  row_type: 'marquee',
  is_active: true
});

const partners = computed(() => courseStore.adminPartners || []);

const topFixedCount = computed(() => partners.value.filter(p => p.row_type === 'top_fixed').length);
const bottomFixedCount = computed(() => partners.value.filter(p => p.row_type === 'bottom_fixed').length);
const marqueeCount = computed(() => partners.value.filter(p => !p.row_type || p.row_type === 'marquee').length);

const getRowLabel = (type) => {
  if (type === 'top_fixed') return 'Hàng trên (Cố định)';
  if (type === 'bottom_fixed') return 'Hàng dưới (Cố định)';
  return 'Hàng giữa (Chạy)';
};

const getRowBadgeStyle = (type) => {
  if (type === 'top_fixed') return 'background: #fef3c7; color: #b45309; border: 1px solid #fde68a;';
  if (type === 'bottom_fixed') return 'background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff;';
  return 'background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd;';
};

const filteredPartners = computed(() => {
  const query = (searchQuery.value || '').toLowerCase().trim();
  return (partners.value || []).filter(p => {
    const pName = (p.name || '').toLowerCase();
    const matchQuery = !query || pName.includes(query);
    const matchStatus = filterStatus.value === 'all' || 
      (filterStatus.value === 'active' && p.is_active) ||
      (filterStatus.value === 'hidden' && !p.is_active);
    const rowType = p.row_type || 'marquee';
    const matchRow = filterRowType.value === 'all' || rowType === filterRowType.value;
    return matchQuery && matchStatus && matchRow;
  });
});

const totalPages = computed(() => Math.ceil(filteredPartners.value.length / pageSize) || 1);

watch([filterRowType, filterStatus, searchQuery], () => {
  currentPage.value = 1;
});

const paginatedPartners = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredPartners.value.slice(start, start + pageSize);
});

const visiblePages = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const curr = currentPage.value;
  let start = Math.max(1, curr - 2);
  let end = Math.min(total, curr + 2);

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

onMounted(async () => {
  try {
    await courseStore.fetchAdminPartners();
  } catch (err) {
    console.error("Error loading admin partners:", err);
  }
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  form.value = {
    name: '',
    src: '',
    link: '',
    position: (partners.value.length || 0) + 1,
    row_type: filterRowType.value !== 'all' ? filterRowType.value : 'marquee',
    is_active: true
  };
  activeView.value = 'form';
};

const editPartner = (p) => {
  isEditing.value = true;
  editingId.value = p.id;
  form.value = {
    name: p.name,
    src: p.src,
    link: p.link || '',
    position: p.position ?? 1,
    row_type: p.row_type || 'marquee',
    is_active: p.is_active !== undefined ? !!p.is_active : true
  };
  activeView.value = 'form';
};

const toggleActive = async (p) => {
  try {
    await courseStore.updatePartner(p.id, { is_active: !p.is_active });
    courseStore.showToast(`Đã ${!p.is_active ? 'bật' : 'tắt'} hiển thị đối tác "${p.name}"`, 'success');
  } catch (err) {
    courseStore.showToast("Lỗi khi cập nhật trạng thái đối tác: " + err.message, 'error');
  }
};

const uploadLogo = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  uploadingLogo.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    form.value.src = url;
    courseStore.showToast('Tải logo lên thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh: ' + err.message, 'error');
  } finally {
    uploadingLogo.value = false;
  }
};

const savePartner = async () => {
  saving.value = true;
  try {
    if (isEditing.value) {
      await courseStore.updatePartner(editingId.value, form.value);
    } else {
      await courseStore.createPartner(form.value);
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast("Có lỗi xảy ra: " + (err.message || err), 'error');
  } finally {
    saving.value = false;
  }
};

const deletePartnerItem = async (id) => {
  const confirmed = await courseStore.confirmAction({
    title: 'Xóa đối tác này?',
    message: 'Bạn có chắc chắn muốn xóa đối tác này khỏi hệ thống? Hành động này không thể hoàn tác.',
    confirmText: 'Xóa vĩnh viễn',
    type: 'danger'
  });
  if (!confirmed) return;

  try {
    await courseStore.deletePartner(id);
  } catch (err) {
    courseStore.showToast("Lỗi xóa đối tác: " + err.message, 'error');
  }
};
</script>
