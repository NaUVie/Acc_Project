<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Gói Combo / Bundle (Multiple Courses)</h2>
          <p>Tạo các gói combo bundle chứa nhiều khóa học với mức giá ưu đãi và quà tặng kèm.</p>
        </div>
        <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm gói Combo mới</button>
      </div>

      <!-- Bundles Table -->
      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Hình ảnh</th>
              <th>Tên gói Bundle</th>
              <th>Mô tả</th>
              <th>Giá bán / Giá gốc</th>
              <th>Khóa học thuộc Bundle</th>
              <th>Quà tặng kèm (Bonus Gifts)</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bundles" :key="b.id">
              <td>
                <img :src="b.image || '/images/default.jpg'" :alt="b.title" class="admin-course-thumb" />
              </td>
              <td class="font-bold">
                <div>{{ b.title }}</div>
                <small class="text-muted">Handle: {{ b.handle }}</small>
              </td>
              <td style="max-width: 200px;">
                <div class="line-clamp-2 text-sm text-secondary" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;" :title="b.description">
                  {{ b.description }}
                </div>
              </td>
              <td>
                <div class="price-text font-bold text-primary">{{ formatPrice(b.price) }}</div>
                <del class="text-muted text-xs" v-if="b.original_price > b.price">{{ formatPrice(b.original_price) }}</del>
                <div v-if="b.original_price > b.price" class="badge badge-danger text-xs mt-1">
                  Giảm {{ Math.round((1 - b.price / b.original_price) * 100) }}%
                </div>
              </td>
              <td style="max-width: 240px;">
                <div class="bundle-courses-tags">
                  <template v-if="b.courses && b.courses.length > 0">
                    <span 
                      v-for="c in b.courses.slice(0, 2)" 
                      :key="c.id" 
                      class="badge badge-success mr-1 mb-1"
                      style="display: inline-block; margin-right: 4px; margin-bottom: 4px; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;"
                    >
                      ✓ {{ c.title }}
                    </span>
                    <span 
                      v-if="b.courses.length > 2"
                      class="badge" 
                      style="background: #e2e8f0; color: #334155; font-weight: 700; font-size: 11px; cursor: pointer; display: inline-block; margin-bottom: 4px; padding: 4px 8px; border-radius: 6px;"
                      :title="b.courses.map(x => x.title).join('\n')"
                    >
                      +{{ b.courses.length - 2 }} khóa khác
                    </span>
                  </template>
                  <span v-else class="text-muted text-xs">
                    (Chưa chọn khóa học nào)
                  </span>
                </div>
              </td>
              <td style="max-width: 220px;">
                <div class="bundle-gift-tags">
                  <template v-if="(b.gift_courses || b.giftCourses || []).length > 0">
                    <span 
                      v-for="g in (b.gift_courses || b.giftCourses || []).slice(0, 2)" 
                      :key="g.id" 
                      class="badge badge-warning mr-1 mb-1"
                      style="display: inline-block; margin-right: 4px; margin-bottom: 4px; background: #fef3c7; color: #d97706; border: 1px solid #fcd34d; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;"
                    >
                      🎁 {{ g.title }}
                    </span>
                    <span 
                      v-if="(b.gift_courses || b.giftCourses || []).length > 2"
                      class="badge" 
                      style="background: #fef3c7; color: #b45309; font-weight: 700; font-size: 11px; cursor: pointer; display: inline-block; margin-bottom: 4px; padding: 4px 8px; border-radius: 6px; border: 1px solid #fcd34d;"
                      :title="(b.gift_courses || b.giftCourses).map(x => x.title).join('\n')"
                    >
                      +{{ (b.gift_courses || b.giftCourses).length - 2 }} quà khác
                    </span>
                  </template>
                  <span v-else class="text-muted text-xs">
                    (Không có quà tặng)
                  </span>
                </div>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="editBundle(b)" class="btn-action edit" title="Sửa gói Bundle">✏️</button>
                  <button @click="deleteBundle(b.id)" class="btn-action delete" title="Xóa gói Bundle">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="bundles.length === 0">
              <td colspan="7" class="text-center py-8 text-muted">Chưa có gói Combo nào. Nhấn "+ Thêm gói Combo mới" để tạo gói mới.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ==================== SUB-PAGE FORM: ADD/EDIT BUNDLE ==================== -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa thông tin gói Combo / Bundle' : 'Thêm gói Combo / Bundle mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveBundle" class="mt-2">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Tên gói Combo</label>
          <input v-model="form.title" @input="onTitleInput" type="text" required class="admin-input-style" placeholder="Ví dụ: Bundle 2026 Master VIP Tất Cả Khóa Học" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Đường dẫn tĩnh (Handle - Tự động tạo)</label>
          <input v-model="form.handle" type="text" required class="admin-input-style" placeholder="bundle-2026-master" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <!-- Select Multiple Courses Included in Bundle -->
        <div class="form-group mt-4" style="padding: 18px; background: #f0f9ff; border-radius: 12px; border: 1px solid #bae6fd;">
          <div class="flex-between mb-3">
            <label class="font-bold" style="font-size: 15px; color: #0284c7;">
              1. Chọn các khóa học thuộc gói Bundle này:
            </label>
            <span class="text-sm font-bold" style="color: #475569;">
              Tự động tính Giá gốc: <strong style="color: #0284c7; font-size: 16px;">{{ formatPrice(form.originalPrice) }}</strong>
            </span>
          </div>
          <div class="courses-checkbox-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; max-height: 240px; overflow-y: auto; padding-right: 8px;">
            <label 
              v-for="c in courses" 
              :key="c.id"
              style="display: flex; align-items: center; gap: 10px; font-size: 13px; cursor: pointer; background: #ffffff; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; color: #0f172a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);"
            >
              <input 
                type="checkbox" 
                :value="c.id" 
                v-model="form.courseIds"
                @change="recalculatePrices"
                style="width: 18px; height: 18px; accent-color: #0284c7;"
              />
              <span style="flex: 1; font-weight: 600; color: #0f172a;">{{ c.title }}</span>
              <small style="color: #0284c7; font-weight: 700;">{{ formatPrice(c.originalPrice || c.price) }}</small>
            </label>
          </div>
        </div>

        <!-- Price & Discount Config -->
        <div class="price-config-box mt-4" style="padding: 18px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0;">
          <label class="font-bold mb-3" style="font-size: 15px; display: block; color: #0f172a;">2. Thiết lập giá bán & Khuyến mãi Combo:</label>
          
          <div class="discount-mode-selector mb-3" style="display: flex; gap: 20px; align-items: center;">
            <span class="text-sm font-bold" style="color: #475569;">Hình thức giảm giá:</span>
            <label style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 14px; color: #0f172a; font-weight: 600;">
              <input type="radio" value="percent" v-model="discountMode" @change="onDiscountModeChange" style="width: 16px; height: 16px; accent-color: #0284c7;" /> % Phần trăm giảm
            </label>
            <label style="cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 14px; color: #0f172a; font-weight: 600;">
              <input type="radio" value="vnd" v-model="discountMode" @change="onDiscountModeChange" style="width: 16px; height: 16px; accent-color: #0284c7;" /> Giá bán cụ thể (VNĐ)
            </label>
          </div>

          <div class="grid-3 gap-4">
            <div class="form-group">
              <label style="color: #1e293b; font-weight: 600;">Giá gốc tổng khóa học con (VNĐ)</label>
              <input v-model.number="form.originalPrice" type="number" readonly class="admin-input-style" style="background: #f1f5f9; color: #0f172a; font-weight: bold; border: 1px solid #cbd5e1;" />
            </div>

            <div class="form-group" v-if="discountMode === 'percent'">
              <label style="color: #1e293b; font-weight: 600;">% Khuyến mãi (%)</label>
              <input v-model.number="discountPercent" type="number" min="0" max="100" @input="calculatePriceFromPercent" class="admin-input-style font-bold" placeholder="VD: 30" style="background: #ffffff; color: #0284c7; border: 1px solid #cbd5e1;" />
            </div>

            <div class="form-group">
              <label style="color: #1e293b; font-weight: 600;">Giá bán ưu đãi cuối cùng (VNĐ)</label>
              <input v-model.number="form.price" type="number" required @input="calculatePercentFromPrice" class="admin-input-style font-bold" style="background: #ffffff; color: #0284c7; border: 1px solid #cbd5e1; font-size: 16px;" />
            </div>
          </div>
          
          <div class="mt-2 text-xs" style="color: #475569; font-weight: 600;" v-if="form.originalPrice > 0">
            Bạn đang áp dụng mức giảm <strong style="color: #0284c7;">{{ calculatedPercent }}%</strong> (Tiết kiệm {{ formatPrice(form.originalPrice - form.price) }}).
          </div>
        </div>

        <!-- Select Bonus Gift Courses -->
        <div class="form-group mt-4" style="padding: 18px; background: #fffbebf5; border-radius: 12px; border: 1px solid #fcd34d;">
          <label class="font-bold mb-2" style="font-size: 15px; display: block; color: #b45309;">
            3. Chọn quà tặng kèm khi mua Combo (Khóa học tặng miễn phí):
          </label>
          <div class="courses-checkbox-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; max-height: 200px; overflow-y: auto; padding-right: 8px;">
            <label 
              v-for="c in courses" 
              :key="'gift-' + c.id"
              style="display: flex; align-items: center; gap: 10px; font-size: 13px; cursor: pointer; background: #ffffff; padding: 10px 14px; border-radius: 8px; border: 1px solid #fde68a; color: #0f172a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);"
            >
              <input 
                type="checkbox" 
                :value="c.id" 
                v-model="form.giftCourseIds"
                style="width: 18px; height: 18px; accent-color: #d97706;"
              />
              <span style="flex: 1; font-weight: 600; color: #0f172a;">{{ c.title }}</span>
            </label>
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Hình ảnh gói Bundle (Tải ảnh từ máy lên Cloudinary hoặc dán URL)</label>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input v-model="form.image" type="text" class="admin-input-style" placeholder="/images/default.jpg hoặc URL Cloudinary" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; flex: 1; min-width: 240px;" />
            <label class="btn btn-primary btn-sm" style="padding: 10px 16px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600;">
              <span>Tải ảnh từ máy</span>
              <input type="file" accept="image/*" @change="uploadBundleImage" style="display: none;" />
            </label>
          </div>
          <div v-if="uploadingImage" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
            Đang tải ảnh lên Cloudinary (Thư mục Acc Demo)...
          </div>
          <div v-if="form.image" class="mt-2">
            <img :src="form.image" alt="Preview" style="max-height: 100px; border-radius: 8px; border: 1px solid #cbd5e1; object-fit: cover;" />
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Mô tả gói Combo</label>
          <textarea v-model="form.description" rows="4" class="admin-input-style" placeholder="Mô tả đặc quyền và danh sách quyền lợi gói..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        </div>

        <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
          <button type="submit" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu gói Combo</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';

const courseStore = useCourseStore();

const bundles = computed(() => courseStore.bundles);
const courses = computed(() => courseStore.courses);

// Active View State ('list' | 'form')
const activeView = ref('list');
const isEditing = ref(false);
const editingId = ref(null);

const discountMode = ref('percent'); // 'percent' | 'vnd'
const discountPercent = ref(30);
const uploadingImage = ref(false);

const uploadBundleImage = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadingImage.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    form.value.image = url;
  } catch (err) {
    alert('Lỗi khi tải ảnh lên Cloudinary: ' + err.message);
  } finally {
    uploadingImage.value = false;
  }
};

const form = ref({
  title: '',
  handle: '',
  price: 0,
  originalPrice: 0,
  image: '/images/default.jpg',
  description: '',
  courseIds: [],
  giftCourseIds: []
});

onMounted(() => {
  courseStore.fetchBundles();
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
});

const onTitleInput = () => {
  if (!isEditing.value || !form.value.handle) {
    form.value.handle = slugify(form.value.title);
  }
};

// Recalculate original price as sum of selected courses
const recalculatePrices = () => {
  const selectedCourses = courses.value.filter(c => form.value.courseIds.includes(c.id));
  const sumOriginal = selectedCourses.reduce((sum, c) => sum + (c.originalPrice || c.price || 0), 0);
  form.value.originalPrice = sumOriginal;

  if (discountMode.value === 'percent') {
    calculatePriceFromPercent();
  } else {
    calculatePercentFromPrice();
  }
};

const calculatePriceFromPercent = () => {
  if (!form.value.originalPrice) return;
  const pct = Math.min(100, Math.max(0, Number(discountPercent.value) || 0));
  form.value.price = Math.round(form.value.originalPrice * (1 - pct / 100));
};

const calculatePercentFromPrice = () => {
  if (!form.value.originalPrice || form.value.originalPrice <= 0) {
    discountPercent.value = 0;
    return;
  }
  const pct = Math.round((1 - form.value.price / form.value.originalPrice) * 100);
  discountPercent.value = Math.max(0, pct);
};

const calculatedPercent = computed(() => {
  if (!form.value.originalPrice || form.value.originalPrice <= 0) return 0;
  return Math.round((1 - form.value.price / form.value.originalPrice) * 100);
});

const onDiscountModeChange = () => {
  if (discountMode.value === 'percent') {
    calculatePriceFromPercent();
  } else {
    calculatePercentFromPrice();
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  const allIds = courses.value.map(c => c.id);
  
  form.value = {
    title: '',
    handle: '',
    price: 0,
    originalPrice: 0,
    image: '/images/default.jpg',
    description: '',
    courseIds: allIds,
    giftCourseIds: []
  };
  discountMode.value = 'percent';
  discountPercent.value = 30;
  
  recalculatePrices();
  activeView.value = 'form';
};

const editBundle = (b) => {
  isEditing.value = true;
  editingId.value = b.id;
  
  const courseIds = b.courses ? b.courses.map(c => c.id) : [];
  const giftCourseIds = (b.gift_courses || b.giftCourses) ? (b.gift_courses || b.giftCourses).map(g => g.id) : [];

  form.value = {
    title: b.title,
    handle: b.handle,
    price: b.price,
    originalPrice: b.original_price || b.originalPrice || 0,
    image: b.image || '/images/default.jpg',
    description: b.description || '',
    courseIds: courseIds,
    giftCourseIds: giftCourseIds
  };
  
  discountMode.value = 'vnd';
  calculatePercentFromPrice();
  activeView.value = 'form';
};

const saveBundle = async () => {
  try {
    if (isEditing.value) {
      await courseStore.updateAdminBundle(editingId.value, form.value);
      alert('Cập nhật gói Combo thành công!');
    } else {
      await courseStore.addAdminBundle(form.value);
      alert('Thêm gói Combo mới thành công!');
    }
    activeView.value = 'list';
  } catch (err) {
    alert(err.message || 'Không thể lưu gói Combo.');
  }
};

const deleteBundle = async (id) => {
  if (confirm('Bạn có chắc muốn xóa gói Combo này?')) {
    try {
      await courseStore.deleteAdminBundle(id);
      alert('Đã xóa gói Combo thành công.');
    } catch (err) {
      alert(err.message || 'Không thể xóa gói Combo.');
    }
  }
};

const formatPrice = (val) => {
  if (!val) return '0đ';
  return val.toLocaleString('vi-VN') + 'đ';
};
</script>
