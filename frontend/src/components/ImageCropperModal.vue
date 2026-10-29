<template>
  <Teleport to="body">
    <Transition name="cropper-fade">
      <div v-if="isOpen" class="cropper-modal-overlay" @click.self="handleClose">
        <div class="cropper-modal-container" role="dialog" aria-modal="true">
          <!-- Header -->
          <div class="cropper-header">
            <div class="cropper-title-group">
              <h3 class="cropper-title">{{ title || '✂ Cắt & Điều Chỉnh Vùng Hiển Thị Hình Ảnh' }}</h3>
              <p class="cropper-subtitle">Kéo khung cắt hoặc di chuyển ảnh để chọn đúng phần hình ảnh bạn muốn hiển thị</p>
            </div>
            <button class="cropper-close-btn" @click="handleClose" aria-label="Đóng">&times;</button>
          </div>

          <!-- Body -->
          <div class="cropper-body">
            <!-- Left: Interactive Cropper Work Area -->
            <div class="cropper-stage-wrapper">
              <div v-if="loadingImage" class="cropper-loading-overlay">
                <div class="cropper-spinner"></div>
                <span>Đang tải ảnh...</span>
              </div>

              <div class="cropper-img-box">
                <img 
                  ref="cropperImageRef" 
                  :src="sourceImageUrl" 
                  alt="Cropping target" 
                  class="cropper-target-img"
                  crossorigin="anonymous"
                  @load="onImgLoaded"
                />
              </div>
            </div>

            <!-- Right: Controls & Live Preview -->
            <div class="cropper-sidebar">
              <!-- 1. Live Preview -->
              <div class="cropper-section">
                <div class="cropper-section-header">
                  <label class="cropper-section-label">Xem trước kết quả</label>
                  <span class="cropper-badge">{{ ratioBadgeLabel }}</span>
                </div>
                <div class="cropper-preview-card">
                  <canvas ref="previewCanvasRef" class="cropper-live-canvas"></canvas>
                </div>
                <small class="cropper-hint">Hiển thị chính xác 100% hình ảnh thực tế sau khi cắt</small>
              </div>

              <!-- 2. Aspect Ratio Presets -->
              <div class="cropper-section">
                <label class="cropper-section-label">Tỷ lệ khung cắt</label>
                <div class="cropper-ratio-buttons">
                  <button 
                    type="button"
                    class="ratio-btn"
                    :class="{ active: currentRatioMode === 'square' }"
                    @click="setRatioMode('square')"
                  >
                    Vuông (1:1)
                  </button>
                  <button 
                    type="button"
                    class="ratio-btn"
                    :class="{ active: currentRatioMode === 'wide' }"
                    @click="setRatioMode('wide')"
                  >
                    Ngang (16:9)
                  </button>
                  <button 
                    type="button"
                    class="ratio-btn"
                    :class="{ active: currentRatioMode === 'partner' }"
                    @click="setRatioMode('partner')"
                  >
                    Logo (26:11)
                  </button>
                  <button 
                    type="button"
                    class="ratio-btn"
                    :class="{ active: currentRatioMode === 'free' }"
                    @click="setRatioMode('free')"
                  >
                    Tự do
                  </button>
                </div>
              </div>

              <!-- 3. Zoom & Rotation Controls -->
              <div class="cropper-section">
                <label class="cropper-section-label">Thu phóng & Góc xoay</label>
                <div class="cropper-tool-grid">
                  <button type="button" class="tool-btn" @click="zoom(0.1)" title="Phóng to ảnh">
                    <span>➕</span> Phóng to
                  </button>
                  <button type="button" class="tool-btn" @click="zoom(-0.1)" title="Thu nhỏ ảnh">
                    <span>➖</span> Thu nhỏ
                  </button>
                  <button type="button" class="tool-btn" @click="rotate(90)" title="Xoay ảnh 90 độ">
                    <span>🔄</span> Xoay 90°
                  </button>
                  <button type="button" class="tool-btn" @click="resetCrop" title="Đặt lại trạng thái ban đầu">
                    <span>↺</span> Đặt lại
                  </button>
                </div>
              </div>

              <!-- 4. Drag Mode -->
              <div class="cropper-section">
                <label class="cropper-section-label">Chế độ chuột</label>
                <div class="cropper-mode-buttons">
                  <button 
                    type="button" 
                    class="mode-btn" 
                    :class="{ active: currentDragMode === 'move' }"
                    @click="setDragMode('move')"
                  >
                    ✋ Di chuyển ảnh
                  </button>
                  <button 
                    type="button" 
                    class="mode-btn" 
                    :class="{ active: currentDragMode === 'crop' }"
                    @click="setDragMode('crop')"
                  >
                    ✂ Vẽ khung mới
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="cropper-footer">
            <span class="cropper-tip">💡 Mẹo: Bạn có thể kéo chuột di chuyển ảnh, lăn chuột để phóng to/thu nhỏ, hoặc kéo 8 điểm tròn neo để chỉnh khung.</span>
            <div class="cropper-footer-actions">
              <button type="button" class="btn btn-secondary" @click="handleClose" :disabled="savingCropped">
                Hủy
              </button>
              <button type="button" class="btn btn-primary" @click="applyCropAndUpload" :disabled="savingCropped || loadingImage">
                <span v-if="!savingCropped">✓ Xác nhận Cắt & Cập nhật Ảnh</span>
                <span v-else>Đang tối ưu & Tải lên...</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from 'vue';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  imageUrl: { type: String, default: '' },
  aspectRatio: { type: String, default: 'free' },
  title: { type: String, default: '' }
});

const emit = defineEmits(['close', 'cropped']);
const courseStore = useCourseStore();

const cropperImageRef = ref(null);
const previewCanvasRef = ref(null);
const loadingImage = ref(false);
const savingCropped = ref(false);
const currentRatioMode = ref('free');
const currentDragMode = ref('move');
const sourceImageUrl = ref('');
let cropperInstance = null;
let previewRaf = null;

const ratioBadgeLabel = computed(() => {
  switch (currentRatioMode.value) {
    case 'square': return 'Vuông 1:1';
    case 'wide': return 'Ngang 16:9';
    case 'partner': return 'Logo 26:11';
    default: return 'Tự do';
  }
});

const setDragMode = (mode) => {
  currentDragMode.value = mode;
  if (cropperInstance) {
    cropperInstance.setDragMode(mode);
  }
};

const getApiBase = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  if (typeof window !== 'undefined') {
    if (import.meta.env.DEV) return `${window.location.protocol}//${window.location.hostname}:8000/api`;
    return `${window.location.origin}/api`;
  }
  return '/api';
};

const getNumericRatio = (mode) => {
  switch (mode) {
    case 'partner': return 260 / 110;
    case 'square': return 1;
    case 'wide': return 16 / 9;
    default: return NaN;
  }
};

const resolveImageUrl = (url) => {
  if (!url) return '';
  let finalSourceUrl = url.trim();
  const isDataUrl = finalSourceUrl.startsWith('data:') || finalSourceUrl.startsWith('blob:');
  const isGoogleDrive = /(?:drive\.google\.com|lh3\.googleusercontent\.com)/i.test(finalSourceUrl);
  if (!isDataUrl && isGoogleDrive) {
    return `${getApiBase()}/upload/proxy-image?url=${encodeURIComponent(finalSourceUrl)}`;
  }
  if (!isDataUrl) {
    return formatImageUrl(finalSourceUrl, 's1600');
  }
  return finalSourceUrl;
};

const updatePreviewCanvas = () => {
  if (!cropperInstance || !previewCanvasRef.value) return;

  try {
    let previewOpts = {
      fillColor: '#ffffff',
      imageSmoothingEnabled: true,
      imageSmoothingQuality: 'medium'
    };

    if (currentRatioMode.value === 'square') {
      previewOpts.width = 300;
      previewOpts.height = 300;
    } else if (currentRatioMode.value === 'wide') {
      previewOpts.width = 320;
      previewOpts.height = 180;
    } else if (currentRatioMode.value === 'partner') {
      previewOpts.width = 320;
      previewOpts.height = 135;
    } else {
      previewOpts.maxWidth = 320;
      previewOpts.maxHeight = 320;
    }

    const cropped = cropperInstance.getCroppedCanvas(previewOpts);
    if (!cropped) return;

    const canvas = previewCanvasRef.value;
    canvas.width = cropped.width;
    canvas.height = cropped.height;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(cropped, 0, 0);
  } catch (err) {
    console.warn('Canvas preview error:', err);
  }
};

const schedulePreviewUpdate = () => {
  if (previewRaf) cancelAnimationFrame(previewRaf);
  previewRaf = requestAnimationFrame(() => {
    updatePreviewCanvas();
  });
};

const onImgLoaded = () => {
  if (props.isOpen) {
    nextTick(() => {
      initCropper();
    });
  }
};

const initCropper = () => {
  if (cropperInstance) {
    cropperInstance.destroy();
    cropperInstance = null;
  }
  if (!cropperImageRef.value) return;

  const CropperConstructor = window.Cropper || Cropper;
  const ratio = getNumericRatio(currentRatioMode.value);

  cropperInstance = new CropperConstructor(cropperImageRef.value, {
    aspectRatio: ratio,
    viewMode: 0,
    dragMode: currentDragMode.value,
    autoCropArea: 0.9,
    cropBoxMovable: true,
    cropBoxResizable: true,
    responsive: true,
    restore: false,
    checkCrossOrigin: true,
    ready() {
      loadingImage.value = false;
      setTimeout(() => {
        if (cropperInstance) {
          cropperInstance.resize();
          schedulePreviewUpdate();
        }
      }, 60);
    },
    crop() {
      schedulePreviewUpdate();
    }
  });
};

const setRatioMode = (mode) => {
  currentRatioMode.value = mode;
  if (cropperInstance) {
    cropperInstance.setAspectRatio(getNumericRatio(mode));
    schedulePreviewUpdate();
  }
};

const zoom = (delta) => {
  if (!cropperInstance) return;
  cropperInstance.zoom(delta);
  schedulePreviewUpdate();
};

const rotate = (deg) => {
  if (!cropperInstance) return;
  cropperInstance.rotate(deg);
  schedulePreviewUpdate();
};

const resetCrop = () => {
  if (!cropperInstance) return;
  cropperInstance.reset();
  schedulePreviewUpdate();
};

const applyCropAndUpload = async () => {
  if (!cropperInstance) return;

  savingCropped.value = true;
  try {
    const cropData = cropperInstance.getData();

    let canvasOptions = {
      fillColor: '#ffffff',
      imageSmoothingEnabled: true,
      imageSmoothingQuality: 'high',
    };

    if (currentRatioMode.value === 'square') {
      canvasOptions.width = 800;
      canvasOptions.height = 800;
    } else if (currentRatioMode.value === 'wide') {
      canvasOptions.width = 1280;
      canvasOptions.height = 720;
    } else if (currentRatioMode.value === 'partner') {
      canvasOptions.width = 800;
      canvasOptions.height = 338;
    } else {
      if (cropData.width > 1920 || cropData.height > 1920) {
        canvasOptions.maxWidth = 1920;
        canvasOptions.maxHeight = 1920;
      }
    }

    const canvas = cropperInstance.getCroppedCanvas(canvasOptions);

    if (!canvas) throw new Error('Không thể tạo canvas từ ảnh cắt!');

    const blob = await new Promise(resolve => {
      canvas.toBlob(resolve, 'image/webp', 0.95);
    });

    if (!blob) throw new Error('Không thể tạo file ảnh từ canvas!');

    const file = new File([blob], `cropped-image-${Date.now()}.webp`, { type: 'image/webp' });
    const uploadedUrl = await courseStore.uploadImage(file);

    courseStore.showToast('Cắt và cập nhật ảnh thành công!', 'success');
    handleClose();
    emit('cropped', uploadedUrl);
  } catch (err) {
    console.error('Apply crop error:', err);
    courseStore.showToast('Lỗi khi lưu ảnh: ' + (err.message || err), 'error');
  } finally {
    savingCropped.value = false;
  }
};

const handleClose = () => {
  if (savingCropped.value) return;
  if (cropperInstance) {
    cropperInstance.destroy();
    cropperInstance = null;
  }
  emit('close');
};

watch(() => props.isOpen, async (newVal) => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = newVal ? 'hidden' : '';
  }
  if (newVal && props.imageUrl) {
    loadingImage.value = true;
    currentDragMode.value = 'move';
    currentRatioMode.value = props.aspectRatio || 'free';
    sourceImageUrl.value = resolveImageUrl(props.imageUrl);
    await nextTick();
    setTimeout(() => {
      if (!cropperInstance && cropperImageRef.value) {
        initCropper();
      }
    }, 200);
  } else if (!newVal && cropperInstance) {
    cropperInstance.destroy();
    cropperInstance = null;
  }
});

watch(() => props.imageUrl, (newVal) => {
  if (props.isOpen && newVal) {
    loadingImage.value = true;
    sourceImageUrl.value = resolveImageUrl(newVal);
    nextTick(() => {
      setTimeout(() => initCropper(), 120);
    });
  }
});

onUnmounted(() => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = '';
  }
  if (cropperInstance) {
    cropperInstance.destroy();
    cropperInstance = null;
  }
});
</script>

<style scoped src="@/styles/components/ImageCropperModal.css"></style>
