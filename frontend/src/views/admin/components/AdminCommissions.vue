<template>
  <div class="admin-commissions-component">
    <div style="margin-bottom: 24px;">
      <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0;">🤝 Cấu hình Hoa hồng Giới thiệu Tùy chỉnh (Affiliate Commissions)</h2>
      <p style="font-size: 13px; color: #64748b; margin: 4px 0 0 0;">Cài đặt tỷ lệ % hoa hồng riêng biệt cho từng Học viên/CTV với từng Khóa học cụ thể.</p>
    </div>

    <!-- Form set commission -->
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
      <h4 style="font-size: 15px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 14px;">Thiết lập tỷ lệ Hoa hồng Mới</h4>
      
      <form @submit.prevent="handleSetCommission" style="display: grid; grid-template-columns: 2fr 2fr 1fr auto; gap: 12px; align-items: flex-end;">
        <div>
          <label style="font-size: 12px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Chọn Học viên / CTV</label>
          <select v-model="form.user_id" required style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; box-sizing: border-box;">
            <option value="" disabled>-- Chọn tài khoản học viên --</option>
            <option v-for="u in courseStore.adminUsers" :key="u.id" :value="u.id">
              {{ u.fullname }} ({{ u.email }})
            </option>
          </select>
        </div>

        <div>
          <label style="font-size: 12px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Chọn Khóa học</label>
          <select v-model="form.course_id" required style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; box-sizing: border-box;">
            <option value="" disabled>-- Chọn khóa học áp dụng --</option>
            <option v-for="c in courseStore.courses" :key="c.id" :value="c.id">
              {{ c.title }}
            </option>
          </select>
        </div>

        <div>
          <label style="font-size: 12px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Hoa hồng (%)</label>
          <input type="number" min="0" max="100" v-model.number="form.commission_percent" required placeholder="VD: 15" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; box-sizing: border-box;" />
        </div>

        <button type="submit" :disabled="submitting" style="background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; font-size: 13px; cursor: pointer; height: 40px;">
          {{ submitting ? 'Đang lưu...' : 'Lưu cấu hình' }}
        </button>
      </form>
    </div>

    <!-- Commissions Table -->
    <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px; text-align: left;">
        <thead style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #475569; font-weight: 700;">
          <tr>
            <th style="padding: 12px 16px;">Học viên / CTV</th>
            <th style="padding: 12px 16px;">Khóa học áp dụng</th>
            <th style="padding: 12px 16px;">Tỷ lệ Hoa hồng</th>
            <th style="padding: 12px 16px;">Cập nhật lúc</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="courseStore.adminCommissions.length === 0">
            <td colspan="4" style="text-align: center; padding: 30px; color: #94a3b8;">Chưa có cấu hình hoa hồng riêng nào. Hệ thống đang sử dụng mức mặc định (10%).</td>
          </tr>
          <tr v-for="com in courseStore.adminCommissions" :key="com.id" style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 12px 16px; font-weight: 700; color: #0f172a;">{{ com.user_fullname || `User #${com.user_id}` }}</td>
            <td style="padding: 12px 16px; color: #334155;">{{ com.course_title || `Course #${com.course_id}` }}</td>
            <td style="padding: 12px 16px; font-weight: 800; color: #d97706; font-size: 15px;">{{ com.commission_percent }}%</td>
            <td style="padding: 12px 16px; color: #94a3b8; font-size: 12px;">{{ formatDate(com.updated_at || com.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const submitting = ref(false);

const form = ref({
  user_id: '',
  course_id: '',
  commission_percent: 15
});

const formatDate = (iso) => {
  if (!iso) return '';
  return new Date(iso).toLocaleDateString('vi-VN');
};

const handleSetCommission = async () => {
  submitting.value = true;
  try {
    await courseStore.setAdminCommission(form.value.user_id, form.value.course_id, form.value.commission_percent);
  } catch (err) {
    // handled in store
  } finally {
    submitting.value = false;
  }
};

onMounted(() => {
  courseStore.fetchAdminCommissions();
  if (courseStore.adminUsers.length === 0) courseStore.fetchAdminUsers();
  if (courseStore.courses.length === 0) courseStore.fetchCourses();
});
</script>
