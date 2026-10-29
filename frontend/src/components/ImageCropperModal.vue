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
            <!-- Left: Interactive Canvas Work Area -->
            <div class="cropper-stage-wrapper" ref="stageWrapperRef">
              <div v-if="loadingImage" class="cropper-loading-state">
                <div class="cropper-spinner"></div>
                <span>Đang tải ảnh...</span>
              </div>

              <div 
                v-show="!loadingImage"
                class="cropper-canvas-box"
                ref="canvasBoxRef"
                @mousedown="onStageMouseDown"
                @touchstart="onStageTouchStart"
                @wheel.prevent="onWheel"
              >
                <!-- Main background canvas rendering the image -->
                <canvas ref="mainCanvasRef" class="cropper-main-canvas"></canvas>

                <!-- Single unified Crop Mask & Bounding Box (Box shadow creates the dark mask) -->
                <div 
                  class="cropper-selection-box"
                  :style="selectionBoxStyle"
                  ref="selectionBoxRef"
                  @mousedown.stop="onBoxMouseDown"
                  @touchstart.stop="onBoxTouchStart"
                >
                  <!-- Grid Lines (Rule of Thirds) -->
                  <div class="cropper-grid-line grid-h-1"></div>
                  <div class="cropper-grid-line grid-h-2"></div>
                  <div class="cropper-grid-line grid-v-1"></div>
                  <div class="cropper-grid-line grid-v-2"></div>

                  <!-- 8 Interactive Resize Handles -->
                  <div class="cropper-handle handle-nw" @mousedown.stop="startResize('nw', $event)" @touchstart.stop="startResize('nw', $event)"></div>
                  <div class="cropper-handle handle-ne" @mousedown.stop="startResize('ne', $event)" @touchstart.stop="startResize('ne', $event)"></div>
                  <div class="cropper-handle handle-se" @mousedown.stop="startResize('se', $event)" @touchstart.stop="startResize('se', $event)"></div>
                  <div class="cropper-handle handle-sw" @mousedown.stop="startResize('sw', $event)" @touchstart.stop="startResize('sw', $event)"></div>
                  <div class="cropper-handle handle-n" @mousedown.stop="startResize('n', $event)" @touchstart.stop="startResize('n', $event)"></div>
                  <div class="cropper-handle handle-e" @mousedown.stop="startResize('e', $event)" @touchstart.stop="startResize('e', $event)"></div>
                  <div class="cropper-handle handle-s" @mousedown.stop="startResize('s', $event)" @touchstart.stop="startResize('s', $event)"></div>
                  <div class="cropper-handle handle-w" @mousedown.stop="startResize('w', $event)" @touchstart.stop="startResize('w', $event)"></div>
                </div>
              </div>
            </div>

            <!-- Right: Controls & Live Preview -->
            <div class="cropper-sidebar">
              <!-- 1. Live Preview -->
              <div class="cropper-section">
                <label class="cropper-section-label">Xem trước kết quả</label>
                <div class="cropper-preview-card" :style="{ aspectRatio: previewAspectRatioStyle }">
                  <canvas ref="previewCanvasRef" class="cropper-preview-canvas"></canvas>
                </div>
                <small class="cropper-hint">Khung hiển thị thực tế sau khi cắt</small>
              </div>

              <!-- 2. Aspect Ratio Presets -->
              <div class="cropper-section">
                <label class="cropper-section-label">Tỷ lệ khung cắt</label>
                <div class="cropper-ratio-buttons">
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
                    :class="{ active: currentRatioMode === 'free' }"
                    @click="setRatioMode('free')"
                  >
                    Tự do
                  </button>
                </div>
              </div>

              <!-- 3. Zoom Controls -->
              <div class="cropper-section">
                <div class="cropper-zoom-header">
                  <label class="cropper-section-label" style="margin-bottom: 0;">Thu phóng ảnh</label>
                  <span class="cropper-zoom-val">{{ Math.round(zoomLevel * 100) }}%</span>
                </div>
                <div class="cropper-zoom-row">
                  <button type="button" class="tool-icon-btn" @click="adjustZoom(-0.1)" title="Thu nhỏ">-</button>
                  <input 
                    type="range" 
                    v-model.number="zoomLevel" 
                    min="0.3" 
                    max="3.0" 
                    step="0.05"
                    class="cropper-slider"
                    @input="redraw"
                  />
                  <button type="button" class="tool-icon-btn" @click="adjustZoom(0.1)" title="Phóng to">+</button>
                </div>
              </div>

              <!-- 4. Quick Actions -->
              <div class="cropper-section">
                <label class="cropper-section-label">Công cụ nhanh</label>
                <div class="cropper-quick-tools">
                  <button type="button" class="quick-btn" @click="autoDetectLogoBounds" title="Tự động nhận diện và cắt sát phần nội dung ảnh">
                    🎯 Cắt sát nội dung
                  </button>
                  <button type="button" class="quick-btn" @click="rotateImage(90)" title="Xoay 90 độ">
                    🔄 Xoay 90°
                  </button>
                  <button type="button" class="quick-btn" @click="resetCrop" title="Đặt lại vị trí gốc">
                    ↺ Đặt lại
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="cropper-footer">
            <span class="cropper-tip">💡 Mẹo: Bạn có thể lăn chuột trên ảnh để phóng to/thu nhỏ, hoặc kéo các góc của khung chữ nhật.</span>
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
import { ref, reactive, computed, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  imageUrl: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: '✂ Cắt & Điều Chỉnh Vùng Hiển Thị Hình Ảnh'
  },
  aspectRatio: {
    type: String,
    default: 'partner' // 'partner' | 'square' | 'wide' | 'free'
  }
});

const emit = defineEmits(['close', 'cropped']);
const courseStore = useCourseStore();

// Elements
const stageWrapperRef = ref(null);
const canvasBoxRef = ref(null);
const mainCanvasRef = ref(null);
const previewCanvasRef = ref(null);

// States
const loadingImage = ref(false);
const savingCropped = ref(false);
const currentRatioMode = ref(props.aspectRatio || 'partner');
const zoomLevel = ref(1);
const rotation = ref(0);

// Image Pan Offset
const panOffset = reactive({ x: 0, y: 0 });

// Image Source Object
let rawImage = null;
let originalWidth = 0;
let originalHeight = 0;

// Canvas Display Dimensions
const canvasWidth = ref(600);
const canvasHeight = ref(400);

// Crop Selection Box
const cropRect = reactive({
  x: 50,
  y: 50,
  width: 260,
  height: 110
});

// Drag & Resize Modes
let dragMode = null; // 'box' | 'stage' | 'resize'
let resizeHandle = '';
let startMouseX = 0;
let startMouseY = 0;
let startCropX = 0;
let startCropY = 0;
let startCropW = 0;
let startCropH = 0;
let startPanX = 0;
let startPanY = 0;

const selectionBoxStyle = computed(() => {
  return {
    left: `${cropRect.x}px`,
    top: `${cropRect.y}px`,
    width: `${cropRect.width}px`,
    height: `${cropRect.height}px`
  };
});

const getTargetRatio = () => {
  switch (currentRatioMode.value) {
    case 'partner': return 260 / 110; // ~2.3636
    case 'square': return 1;
    case 'wide': return 16 / 9;
    default: return null; // free
  }
};

const previewAspectRatioStyle = computed(() => {
  const r = getTargetRatio();
  if (r) return `${r}`;
  if (cropRect.height > 0) return `${cropRect.width} / ${cropRect.height}`;
  return '260 / 110';
});

const setRatioMode = (mode) => {
  currentRatioMode.value = mode;
  alignCropBoxToRatio();
  redraw();
};

const alignCropBoxToRatio = () => {
  const ratio = getTargetRatio();
  if (!ratio) return;

  const currentCenter = {
    x: cropRect.x + cropRect.width / 2,
    y: cropRect.y + cropRect.height / 2
  };

  let newW = cropRect.width;
  let newH = newW / ratio;

  if (newH > canvasHeight.value * 0.9) {
    newH = canvasHeight.value * 0.85;
    newW = newH * ratio;
  }
  if (newW > canvasWidth.value * 0.9) {
    newW = canvasWidth.value * 0.85;
    newH = newW / ratio;
  }

  cropRect.width = Math.round(newW);
  cropRect.height = Math.round(newH);
  cropRect.x = Math.max(0, Math.min(canvasWidth.value - cropRect.width, Math.round(currentCenter.x - cropRect.width / 2)));
  cropRect.y = Math.max(0, Math.min(canvasHeight.value - cropRect.height, Math.round(currentCenter.y - cropRect.height / 2)));
};

const adjustZoom = (delta) => {
  const next = Math.max(0.3, Math.min(3.0, +(zoomLevel.value + delta).toFixed(2)));
  zoomLevel.value = next;
  redraw();
};

const onWheel = (e) => {
  const delta = e.deltaY < 0 ? 0.08 : -0.08;
  adjustZoom(delta);
};

const rotateImage = (deg) => {
  rotation.value = (rotation.value + deg) % 360;
  redraw();
};

const resetCrop = () => {
  zoomLevel.value = 1;
  rotation.value = 0;
  panOffset.x = 0;
  panOffset.y = 0;
  initCropBox();
  redraw();
};

const initCropBox = () => {
  const w = canvasWidth.value;
  const h = canvasHeight.value;
  const ratio = getTargetRatio() || (260 / 110);

  let boxW = Math.min(w * 0.85, 520);
  let boxH = boxW / ratio;

  if (boxH > h * 0.82) {
    boxH = h * 0.8;
    boxW = boxH * ratio;
  }

  cropRect.width = Math.round(boxW);
  cropRect.height = Math.round(boxH);
  cropRect.x = Math.round((w - cropRect.width) / 2);
  cropRect.y = Math.round((h - cropRect.height) / 2);
};

const getApiBase = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  if (typeof window !== 'undefined') {
    const isDev = import.meta.env.DEV;
    if (isDev) {
      return `${window.location.protocol}//${window.location.hostname}:8000/api`;
    }
    return `${window.location.origin}/api`;
  }
  return '/api';
};

const loadImage = async (url) => {
  if (!url) return;
  loadingImage.value = true;

  try {
    let finalSourceUrl = url.trim();
    const isDataUrl = finalSourceUrl.startsWith('data:') || finalSourceUrl.startsWith('blob:');

    // If it's a Google Drive link or external drive link, route through backend proxy
    // to completely bypass browser CORS restrictions and prevent canvas tainting.
    const isGoogleDrive = /(?:drive\.google\.com|lh3\.googleusercontent\.com)/i.test(finalSourceUrl);
    if (!isDataUrl && isGoogleDrive) {
      finalSourceUrl = `${getApiBase()}/upload/proxy-image?url=${encodeURIComponent(finalSourceUrl)}`;
    } else if (!isDataUrl) {
      finalSourceUrl = formatImageUrl(finalSourceUrl, 's1600');
    }

    const img = new Image();
    if (!isDataUrl) {
      img.crossOrigin = 'anonymous';
    }

    await new Promise((resolve, reject) => {
      img.onload = () => resolve();
      img.onerror = (err) => {
        // If direct load failed and we haven't tried proxy yet, fallback to proxy
        if (!isDataUrl && !finalSourceUrl.includes('/upload/proxy-image')) {
          const proxyImg = new Image();
          proxyImg.crossOrigin = 'anonymous';
          proxyImg.onload = () => {
            rawImage = proxyImg;
            resolve();
          };
          proxyImg.onerror = (proxyErr) => reject(proxyErr);
          proxyImg.src = `${getApiBase()}/upload/proxy-image?url=${encodeURIComponent(url)}`;
          return;
        }
        reject(err);
      };
      img.src = finalSourceUrl;
      rawImage = img;
    });

    originalWidth = rawImage.naturalWidth || rawImage.width;
    originalHeight = rawImage.naturalHeight || rawImage.height;

    await nextTick();
    updateCanvasSize();
    initCropBox();
    redraw();
  } catch (err) {
    console.error('Failed to load image into cropper:', err);
    courseStore.showToast('Không thể tải ảnh để cắt. Vui lòng kiểm tra quyền truy cập!', 'error');
  } finally {
    loadingImage.value = false;
  }
};

const updateCanvasSize = () => {
  if (!canvasBoxRef.value) return;
  const rect = canvasBoxRef.value.getBoundingClientRect();
  const w = Math.max(300, Math.floor(rect.width) || 600);
  const h = Math.max(260, Math.floor(rect.height) || 400);

  canvasWidth.value = w;
  canvasHeight.value = h;

  if (mainCanvasRef.value) {
    mainCanvasRef.value.width = w;
    mainCanvasRef.value.height = h;
  }
};

const redraw = () => {
  if (!mainCanvasRef.value || !rawImage) return;

  const canvas = mainCanvasRef.value;
  const ctx = canvas.getContext('2d');
  const cw = canvas.width;
  const ch = canvas.height;

  ctx.clearRect(0, 0, cw, ch);

  // 1. Draw Checkered Background
  drawCheckeredPattern(ctx, cw, ch);

  // 2. Draw Image (Scaled, Rotated, Panned)
  const fitScale = Math.min(cw / originalWidth, ch / originalHeight) * 0.9;
  const currentScale = fitScale * zoomLevel.value;

  const scaledW = originalWidth * currentScale;
  const scaledH = originalHeight * currentScale;

  ctx.save();
  ctx.translate(cw / 2 + panOffset.x, ch / 2 + panOffset.y);
  ctx.rotate((rotation.value * Math.PI) / 180);
  ctx.drawImage(
    rawImage,
    -scaledW / 2,
    -scaledH / 2,
    scaledW,
    scaledH
  );
  ctx.restore();

  // 3. Update Live Preview
  updatePreviewCanvas();
};

const drawCheckeredPattern = (ctx, w, h) => {
  const size = 12;
  ctx.fillStyle = '#f1f5f9';
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = '#e2e8f0';
  for (let y = 0; y < h; y += size) {
    for (let x = 0; x < w; x += size) {
      if ((Math.floor(x / size) + Math.floor(y / size)) % 2 === 1) {
        ctx.fillRect(x, y, size, size);
      }
    }
  }
};

const updatePreviewCanvas = () => {
  if (!previewCanvasRef.value || !mainCanvasRef.value || !rawImage) return;

  const prevCanvas = previewCanvasRef.value;
  const prevCtx = prevCanvas.getContext('2d');
  
  prevCanvas.width = 520;
  prevCanvas.height = 220;

  prevCtx.clearRect(0, 0, prevCanvas.width, prevCanvas.height);
  prevCtx.fillStyle = '#ffffff';
  prevCtx.fillRect(0, 0, prevCanvas.width, prevCanvas.height);

  const cw = mainCanvasRef.value.width;
  const ch = mainCanvasRef.value.height;
  const fitScale = Math.min(cw / originalWidth, ch / originalHeight) * 0.9;
  const currentScale = fitScale * zoomLevel.value;

  prevCtx.save();
  const scale = Math.min(prevCanvas.width / cropRect.width, prevCanvas.height / cropRect.height);
  const offsetX = (prevCanvas.width - cropRect.width * scale) / 2;
  const offsetY = (prevCanvas.height - cropRect.height * scale) / 2;

  prevCtx.translate(offsetX, offsetY);
  prevCtx.scale(scale, scale);
  prevCtx.translate(-cropRect.x, -cropRect.y);

  prevCtx.translate(cw / 2 + panOffset.x, ch / 2 + panOffset.y);
  prevCtx.rotate((rotation.value * Math.PI) / 180);
  const scaledW = originalWidth * currentScale;
  const scaledH = originalHeight * currentScale;
  prevCtx.drawImage(rawImage, -scaledW / 2, -scaledH / 2, scaledW, scaledH);
  prevCtx.restore();
};

const autoDetectLogoBounds = () => {
  if (!rawImage || !originalWidth || !originalHeight) return;

  try {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = originalWidth;
    tempCanvas.height = originalHeight;
    const ctx = tempCanvas.getContext('2d');
    ctx.drawImage(rawImage, 0, 0);

    const imgData = ctx.getImageData(0, 0, originalWidth, originalHeight);
    const data = imgData.data;

    let minX = originalWidth;
    let minY = originalHeight;
    let maxX = 0;
    let maxY = 0;
    let found = false;

    for (let y = 0; y < originalHeight; y++) {
      for (let x = 0; x < originalWidth; x++) {
        const i = (y * originalWidth + x) * 4;
        const alpha = data[i + 3];
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];

        const isContent = alpha > 20 && !(r > 245 && g > 245 && b > 245 && alpha === 255);
        if (isContent) {
          found = true;
          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
        }
      }
    }

    if (!found) {
      courseStore.showToast('Không tìm thấy viền nổi bật. Bạn có thể kéo khung cắt thủ công!', 'info');
      return;
    }

    const padX = Math.round((maxX - minX) * 0.06);
    const padY = Math.round((maxY - minY) * 0.06);
    const boxX = Math.max(0, minX - padX);
    const boxY = Math.max(0, minY - padY);
    const boxW = Math.min(originalWidth - boxX, (maxX - minX) + padX * 2);
    const boxH = Math.min(originalHeight - boxY, (maxY - minY) + padY * 2);

    const cw = mainCanvasRef.value.width;
    const ch = mainCanvasRef.value.height;
    const fitScale = Math.min(cw / originalWidth, ch / originalHeight) * 0.9 * zoomLevel.value;

    const canvasImgX = (cw - originalWidth * fitScale) / 2 + panOffset.x;
    const canvasImgY = (ch - originalHeight * fitScale) / 2 + panOffset.y;

    let mappedX = canvasImgX + boxX * fitScale;
    let mappedY = canvasImgY + boxY * fitScale;
    let mappedW = boxW * fitScale;
    let mappedH = boxH * fitScale;

    mappedX = Math.max(0, Math.min(cw - 50, mappedX));
    mappedY = Math.max(0, Math.min(ch - 50, mappedY));
    mappedW = Math.max(50, Math.min(cw - mappedX, mappedW));
    mappedH = Math.max(30, Math.min(ch - mappedY, mappedH));

    cropRect.x = Math.round(mappedX);
    cropRect.y = Math.round(mappedY);
    cropRect.width = Math.round(mappedW);
    cropRect.height = Math.round(mappedH);

    currentRatioMode.value = 'free';
    redraw();
    courseStore.showToast('Đã tự động căn sát vùng nội dung!', 'success');
  } catch (e) {
    courseStore.showToast('Không thể quét tự động. Bạn có thể kéo khung cắt thủ công!', 'warning');
  }
};

const onBoxMouseDown = (e) => {
  dragMode = 'box';
  startMouseX = e.clientX;
  startMouseY = e.clientY;
  startCropX = cropRect.x;
  startCropY = cropRect.y;

  window.addEventListener('mousemove', onGlobalMouseMove);
  window.addEventListener('mouseup', onGlobalMouseUp);
};

const onBoxTouchStart = (e) => {
  if (e.touches.length !== 1) return;
  dragMode = 'box';
  startMouseX = e.touches[0].clientX;
  startMouseY = e.touches[0].clientY;
  startCropX = cropRect.x;
  startCropY = cropRect.y;

  window.addEventListener('touchmove', onGlobalTouchMove);
  window.addEventListener('touchend', onGlobalTouchEnd);
};

const onStageMouseDown = (e) => {
  dragMode = 'stage';
  startMouseX = e.clientX;
  startMouseY = e.clientY;
  startPanX = panOffset.x;
  startPanY = panOffset.y;

  window.addEventListener('mousemove', onGlobalMouseMove);
  window.addEventListener('mouseup', onGlobalMouseUp);
};

const onStageTouchStart = (e) => {
  if (e.touches.length !== 1) return;
  dragMode = 'stage';
  startMouseX = e.touches[0].clientX;
  startMouseY = e.touches[0].clientY;
  startPanX = panOffset.x;
  startPanY = panOffset.y;

  window.addEventListener('touchmove', onGlobalTouchMove);
  window.addEventListener('touchend', onGlobalTouchEnd);
};

const startResize = (handle, e) => {
  dragMode = 'resize';
  resizeHandle = handle;
  startMouseX = e.clientX || (e.touches && e.touches[0].clientX);
  startMouseY = e.clientY || (e.touches && e.touches[0].clientY);
  startCropX = cropRect.x;
  startCropY = cropRect.y;
  startCropW = cropRect.width;
  startCropH = cropRect.height;

  window.addEventListener('mousemove', onGlobalMouseMove);
  window.addEventListener('mouseup', onGlobalMouseUp);
  window.addEventListener('touchmove', onGlobalTouchMove);
  window.addEventListener('touchend', onGlobalTouchEnd);
};

const onGlobalMouseMove = (e) => {
  handlePointerMove(e.clientX, e.clientY);
};

const onGlobalTouchMove = (e) => {
  if (e.touches.length !== 1) return;
  handlePointerMove(e.touches[0].clientX, e.touches[0].clientY);
};

const handlePointerMove = (clientX, clientY) => {
  const dx = clientX - startMouseX;
  const dy = clientY - startMouseY;

  if (dragMode === 'box') {
    const maxX = canvasWidth.value - cropRect.width;
    const maxY = canvasHeight.value - cropRect.height;
    cropRect.x = Math.max(0, Math.min(maxX, Math.round(startCropX + dx)));
    cropRect.y = Math.max(0, Math.min(maxY, Math.round(startCropY + dy)));
    redraw();
  } else if (dragMode === 'stage') {
    panOffset.x = Math.round(startPanX + dx);
    panOffset.y = Math.round(startPanY + dy);
    redraw();
  } else if (dragMode === 'resize') {
    const ratio = getTargetRatio();
    let newX = startCropX;
    let newY = startCropY;
    let newW = startCropW;
    let newH = startCropH;

    if (resizeHandle.includes('e')) newW = Math.max(50, startCropW + dx);
    if (resizeHandle.includes('s')) newH = Math.max(30, startCropH + dy);
    if (resizeHandle.includes('w')) {
      const proposedW = Math.max(50, startCropW - dx);
      newX = startCropX + (startCropW - proposedW);
      newW = proposedW;
    }
    if (resizeHandle.includes('n')) {
      const proposedH = Math.max(30, startCropH - dy);
      newY = startCropY + (startCropH - proposedH);
      newH = proposedH;
    }

    if (ratio) {
      if (resizeHandle === 'e' || resizeHandle === 'w') {
        newH = newW / ratio;
      } else {
        newW = newH * ratio;
      }
    }

    if (newX < 0) { newW += newX; newX = 0; }
    if (newY < 0) { newH += newY; newY = 0; }
    if (newX + newW > canvasWidth.value) newW = canvasWidth.value - newX;
    if (newY + newH > canvasHeight.value) newH = canvasHeight.value - newY;

    cropRect.x = Math.round(newX);
    cropRect.y = Math.round(newY);
    cropRect.width = Math.round(newW);
    cropRect.height = Math.round(newH);

    redraw();
  }
};

const onGlobalMouseUp = () => {
  dragMode = null;
  window.removeEventListener('mousemove', onGlobalMouseMove);
  window.removeEventListener('mouseup', onGlobalMouseUp);
};

const onGlobalTouchEnd = () => {
  dragMode = null;
  window.removeEventListener('touchmove', onGlobalTouchMove);
  window.removeEventListener('touchend', onGlobalTouchEnd);
};

const applyCropAndUpload = async () => {
  if (!rawImage || !originalWidth || !originalHeight) return;

  savingCropped.value = true;
  try {
    const cw = mainCanvasRef.value.width;
    const ch = mainCanvasRef.value.height;
    const fitScale = Math.min(cw / originalWidth, ch / originalHeight) * 0.9 * zoomLevel.value;

    const outWidth = Math.max(520, Math.round(cropRect.width * 2));
    const outHeight = Math.max(220, Math.round(cropRect.height * 2));

    const outputCanvas = document.createElement('canvas');
    outputCanvas.width = outWidth;
    outputCanvas.height = outHeight;
    const ctx = outputCanvas.getContext('2d');

    ctx.clearRect(0, 0, outWidth, outHeight);

    ctx.save();
    ctx.scale(outWidth / cropRect.width, outHeight / cropRect.height);
    ctx.translate(-cropRect.x, -cropRect.y);

    ctx.translate(cw / 2 + panOffset.x, ch / 2 + panOffset.y);
    ctx.rotate((rotation.value * Math.PI) / 180);
    const scaledW = originalWidth * fitScale;
    const scaledH = originalHeight * fitScale;
    ctx.drawImage(rawImage, -scaledW / 2, -scaledH / 2, scaledW, scaledH);
    ctx.restore();

    const blob = await new Promise(resolve => {
      outputCanvas.toBlob(resolve, 'image/webp', 0.95);
    });

    if (!blob) throw new Error('Không thể tạo file ảnh từ canvas!');

    const file = new File([blob], `cropped-image-${Date.now()}.webp`, { type: 'image/webp' });
    const uploadedUrl = await courseStore.uploadImage(file);

    courseStore.showToast('Cắt và tải ảnh mới lên thành công!', 'success');
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
  emit('close');
};

watch(() => props.isOpen, async (newVal) => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = newVal ? 'hidden' : '';
  }
  if (newVal && props.imageUrl) {
    zoomLevel.value = 1;
    rotation.value = 0;
    panOffset.x = 0;
    panOffset.y = 0;
    currentRatioMode.value = props.aspectRatio || 'free';
    await nextTick();
    loadImage(props.imageUrl);
  }
});

watch(() => props.imageUrl, (newVal) => {
  if (props.isOpen && newVal) {
    loadImage(newVal);
  }
});

onMounted(() => {
  window.addEventListener('resize', () => {
    if (props.isOpen) {
      updateCanvasSize();
      redraw();
    }
  });
});

onUnmounted(() => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = '';
  }
  window.removeEventListener('mousemove', onGlobalMouseMove);
  window.removeEventListener('mouseup', onGlobalMouseUp);
  window.removeEventListener('touchmove', onGlobalTouchMove);
  window.removeEventListener('touchend', onGlobalTouchEnd);
});
</script>

<style scoped src="@/styles/components/ImageCropperModal.css"></style>
