<template>
  <div class="rich-editor-wrapper">
    <!-- Toolbar -->
    <div class="rich-toolbar">
      <button type="button" class="toolbar-btn" :class="{ active: isHeadingActive('h2') }" @click="format('heading', 'h2')" title="Tiêu đề lớn (H2)">H2</button>
      <button type="button" class="toolbar-btn" :class="{ active: isHeadingActive('h3') }" @click="format('heading', 'h3')" title="Tiêu đề vừa (H3)">H3</button>
      <span class="toolbar-divider"></span>
      <button type="button" class="toolbar-btn" @click="format('bold')" title="In đậm (Ctrl+B)"><b>B</b></button>
      <button type="button" class="toolbar-btn" @click="format('italic')" title="In nghiêng (Ctrl+I)"><i>I</i></button>
      <button type="button" class="toolbar-btn" @click="format('underline')" title="Gạch chân (Ctrl+U)"><u>U</u></button>
      <button type="button" class="toolbar-btn" @click="format('strikeThrough')" title="Gạch ngang"><s>S</s></button>
      <span class="toolbar-divider"></span>
      <button type="button" class="toolbar-btn" @click="format('justifyLeft')" title="Căn trái">⬅️ Trái</button>
      <button type="button" class="toolbar-btn" @click="format('justifyCenter')" title="Căn giữa">↔️ Giữa</button>
      <button type="button" class="toolbar-btn" @click="format('justifyRight')" title="Căn phải">➡️ Phải</button>
      <button type="button" class="toolbar-btn" @click="format('justifyFull')" title="Căn đều 2 bên">↔️ Đều</button>
      <span class="toolbar-divider"></span>
      <button type="button" class="toolbar-btn" @click="format('insertUnorderedList')" title="Danh sách gạch đầu dòng">• Danh sách</button>
      <button type="button" class="toolbar-btn" @click="format('insertOrderedList')" title="Danh sách đánh số">1. Danh sách</button>
      <span class="toolbar-divider"></span>
      <button type="button" class="toolbar-btn" @click="addLink" title="Chèn đường dẫn (Link)">🔗 Link</button>
      <button type="button" class="toolbar-btn" @click="$refs.editorImageFileRef.click()" :disabled="isUploadingImage" title="Chèn hình ảnh vào nội dung">
        {{ isUploadingImage ? '⏳ Đang tải...' : '🖼️ Chèn ảnh' }}
      </button>
      <input type="file" ref="editorImageFileRef" @change="insertImage" style="display: none;" accept="image/*" />
      <span class="toolbar-divider" v-if="selectedImg"></span>
      <template v-if="selectedImg">
        <span style="font-size: 12px; font-weight: 600; color: #0284c7; margin-right: 4px;">Ảnh:</span>
        <button type="button" class="toolbar-btn" @click="resizeImage('25%')">25%</button>
        <button type="button" class="toolbar-btn" @click="resizeImage('50%')">50%</button>
        <button type="button" class="toolbar-btn" @click="resizeImage('75%')">75%</button>
        <button type="button" class="toolbar-btn" @click="resizeImage('100%')">100%</button>
        <div style="display: flex; align-items: center; gap: 4px; background: #e0f2fe; padding: 2px 6px; border-radius: 6px;">
          <span style="font-size: 11px; font-weight: 700; color: #0369a1;">Rộng:</span>
          <input 
            type="text" 
            v-model="customWidth" 
            @input="onCustomWidthChange" 
            placeholder="px hoặc %" 
            style="width: 65px; font-size: 12px; padding: 2px 4px; border: 1px solid #7dd3fc; border-radius: 4px; text-align: center; outline: none; background: #ffffff;"
          />
        </div>
        <button type="button" class="toolbar-btn" @click="alignImage('left')">◀️ Trái</button>
        <button type="button" class="toolbar-btn" @click="alignImage('center')">⏺️ Giữa</button>
        <button type="button" class="toolbar-btn" @click="alignImage('right')">▶️ Phải</button>
      </template>
      <button type="button" class="toolbar-btn" @click="format('removeFormat')" title="Xóa định dạng">🧹 Xóa định dạng</button>
      <button type="button" class="toolbar-btn" @click="cleanCurrentContent" title="Dọn sạch mã rác từ Word & Tối ưu dung lượng bài viết" style="color: #0284c7; font-weight: 700; background: #f0f9ff; border: 1px solid #bae6fd;">
        ✨ Dọn mã Word
      </button>
    </div>

    <!-- Editable Content Area -->
    <div
      ref="editorRef"
      class="rich-editor-content"
      contenteditable="true"
      @input="onInput"
      @blur="onBlur"
      @paste="onPaste"
      @click="onEditorClick"
      :placeholder="placeholder"
    ></div>

    <!-- Real-time Size & Word Count Status Bar -->
    <div class="editor-status-bar">
      <div class="status-left">
        <span class="stat-item"><strong>{{ wordCount }}</strong> từ</span>
        <span class="stat-divider">•</span>
        <span class="stat-item"><strong>{{ charCount }}</strong> ký tự</span>
      </div>
      <div class="status-right">
        <div class="size-indicator" :class="sizeStatusClass">
          <span class="status-icon">{{ sizeStatusIcon }}</span>
          <span class="size-text">Dung lượng: <strong>{{ formattedSize }}</strong></span>
          <span class="status-badge">{{ sizeStatusDesc }}</span>
        </div>
        <button 
          v-if="hasBase64Images || rawSizeBytes > 250 * 1024"
          type="button" 
          class="btn-clean-inline" 
          @click="cleanCurrentContent"
          title="Tối ưu dung lượng và chuyển ảnh dán Word sang Cloudinary"
        >
          ⚡ Nén & Dọn dẹp ngay
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCourseStore } from '@/stores/courses';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Nhập nội dung mô tả chi tiết tại đây...'
  }
});

const emit = defineEmits(['update:modelValue']);

const editorRef = ref(null);
const editorImageFileRef = ref(null);
const courseStore = useCourseStore();
const isUploadingImage = ref(false);

// Size & Word count analytics
const rawHtml = computed(() => props.modelValue || '');

const textContent = computed(() => {
  if (!rawHtml.value) return '';
  const div = document.createElement('div');
  div.innerHTML = rawHtml.value;
  return (div.textContent || div.innerText || '').trim();
});

const wordCount = computed(() => {
  if (!textContent.value) return 0;
  return textContent.value.split(/\s+/).filter(Boolean).length;
});

const charCount = computed(() => {
  return textContent.value.length;
});

const rawSizeBytes = computed(() => {
  if (!rawHtml.value) return 0;
  return new Blob([rawHtml.value]).size;
});

const formattedSize = computed(() => {
  const bytes = rawSizeBytes.value;
  if (bytes === 0) return '0 B';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
});

const hasBase64Images = computed(() => {
  return rawHtml.value.includes('data:image/');
});

const sizeStatusClass = computed(() => {
  if (hasBase64Images.value || rawSizeBytes.value > 400 * 1024) return 'status-danger';
  if (rawSizeBytes.value > 120 * 1024) return 'status-warning';
  return 'status-optimal';
});

const sizeStatusIcon = computed(() => {
  if (hasBase64Images.value || rawSizeBytes.value > 400 * 1024) return '🔴';
  if (rawSizeBytes.value > 120 * 1024) return '🟡';
  return '🟢';
});

const sizeStatusDesc = computed(() => {
  if (hasBase64Images.value) return 'Có ảnh dán Word';
  if (rawSizeBytes.value > 400 * 1024) return 'Rất nặng';
  if (rawSizeBytes.value > 120 * 1024) return 'Hơi nặng';
  return 'Tối ưu / Tải nhanh';
});

onMounted(() => {
  if (editorRef.value) {
    editorRef.value.innerHTML = props.modelValue || '';
  }
});

watch(
  () => props.modelValue,
  (newVal) => {
    if (editorRef.value && editorRef.value.innerHTML !== newVal) {
      editorRef.value.innerHTML = newVal || '';
    }
  }
);

const onInput = () => {
  if (editorRef.value) {
    emit('update:modelValue', editorRef.value.innerHTML);
  }
};

const onBlur = () => {
  if (editorRef.value) {
    emit('update:modelValue', editorRef.value.innerHTML);
  }
};

const format = (command, value = null) => {
  if (command === 'heading') {
    document.execCommand('formatBlock', false, `<${value}>`);
  } else {
    document.execCommand(command, false, value);
  }
  onInput();
};

const isHeadingActive = (tag) => {
  return false;
};

const addLink = () => {
  const url = prompt('Nhập đường dẫn URL:');
  if (url) {
    document.execCommand('createLink', false, url);
    onInput();
  }
};

const cleanWordHtml = (rawHtml) => {
  if (!rawHtml || typeof rawHtml !== 'string') return '';

  let html = rawHtml;

  // 1. Remove Word comments and conditional blocks <!--[if ...]>...<![endif]-->
  html = html.replace(/<!--\[if[\s\S]*?<!\[endif\]-->/gi, '');
  html = html.replace(/<!--[\s\S]*?-->/g, '');
  html = html.replace(/<\?xml[\s\S]*?>/gi, '');

  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  // 2. Remove all Office junk elements
  const junkTags = doc.querySelectorAll('o\\:p, xml, style, meta, link, script, w\\:worddocument, w\\:latentstyles, m\\:mathpr');
  junkTags.forEach(el => el.remove());

  // 3. Process all remaining elements
  const allElements = doc.body.querySelectorAll('*');
  allElements.forEach(el => {
    // Remove class names with Mso, Word, etc.
    const className = el.getAttribute('class');
    if (className) {
      const cleanClass = className
        .replace(/\bMso[a-zA-Z0-9_-]*/g, '')
        .replace(/\bWord[a-zA-Z0-9_-]*/g, '')
        .replace(/\s+/g, ' ')
        .trim();
      if (cleanClass) {
        el.setAttribute('class', cleanClass);
      } else {
        el.removeAttribute('class');
      }
    }

    // Remove Office attributes
    const attrsToRemove = ['lang', 'clear', 'border', 'cellpadding', 'cellspacing', 'data-mce-style', 'data-mce-bogus'];
    attrsToRemove.forEach(attr => el.removeAttribute(attr));

    // Clean inline styles
    const styleAttr = el.getAttribute('style');
    if (styleAttr) {
      let cleaned = styleAttr
        .replace(/mso-[^;]+;?/gi, '')
        .replace(/font-family\s*:[^;]+;?/gi, '')
        .replace(/line-height\s*:[^;]+;?/gi, '')
        .replace(/margin-left\s*:[^;]+;?/gi, '')
        .replace(/margin-right\s*:[^;]+;?/gi, '')
        .replace(/padding-left\s*:[^;]+;?/gi, '')
        .replace(/padding-right\s*:[^;]+;?/gi, '')
        .replace(/text-indent\s*:[^;]+;?/gi, '')
        .replace(/tab-stops\s*:[^;]+;?/gi, '')
        .replace(/font-size\s*:\s*(?:1[0-2](?:\.\d+)?pt|1[3-6]px)\s*;?/gi, '')
        .replace(/color\s*:\s*(?:black|windowtext|#000(?:000)?)\s*;?/gi, '')
        .trim();

      cleaned = cleaned.replace(/;+/g, ';').replace(/^;|;$/g, '').trim();

      if (cleaned) {
        el.setAttribute('style', cleaned);
      } else {
        el.removeAttribute('style');
      }
    }
  });

  // 4. Unwrap useless <span> tags that have no attributes
  const spans = doc.body.querySelectorAll('span');
  spans.forEach(span => {
    if (!span.hasAttributes() || !span.getAttribute('style')) {
      span.replaceWith(...span.childNodes);
    }
  });

  return doc.body.innerHTML;
};

// Automatically offload any embedded base64 images from Word to Cloudinary
const uploadBase64Images = async () => {
  if (!editorRef.value) return;
  const imgs = editorRef.value.querySelectorAll('img[src^="data:image/"]');
  if (imgs.length === 0) return;

  courseStore.showToast?.(`Đang tự động chuyển ${imgs.length} ảnh nhúng từ Word sang Cloudinary...`, 'info');
  for (const img of imgs) {
    const src = img.getAttribute('src');
    try {
      const res = await fetch(src);
      const blob = await res.blob();
      const file = new File([blob], `word-img-${Date.now()}.webp`, { type: blob.type || 'image/webp' });
      const cdnUrl = await courseStore.uploadImage(file);
      img.setAttribute('src', cdnUrl);
    } catch (err) {
      console.warn("Could not upload pasted base64 image to Cloudinary:", err);
    }
  }
  onInput();
  courseStore.showToast?.('Đã tối ưu và lưu toàn bộ ảnh lên Cloudinary!', 'success');
};

const cleanCurrentContent = async () => {
  if (!editorRef.value) return;
  const rawHtml = editorRef.value.innerHTML;
  if (!rawHtml) return;

  const beforeLen = rawHtml.length;
  const cleaned = cleanWordHtml(rawHtml);
  editorRef.value.innerHTML = cleaned;
  onInput();

  await uploadBase64Images();

  const afterLen = editorRef.value.innerHTML.length;
  const savedPercent = beforeLen > 0 ? Math.round(((beforeLen - afterLen) / beforeLen) * 100) : 0;
  if (savedPercent > 0) {
    courseStore.showToast?.(`Đã dọn dẹp mã Word, giảm ${savedPercent}% dung lượng bài viết!`, 'success');
  } else {
    courseStore.showToast?.('Nội dung đã được dọn sạch tối ưu!', 'success');
  }
};

const onPaste = async (e) => {
  e.preventDefault();
  const clipboardData = e.clipboardData || window.clipboardData;
  if (!clipboardData) return;

  const html = clipboardData.getData('text/html');
  const text = clipboardData.getData('text/plain');

  if (html) {
    try {
      const cleanHtml = cleanWordHtml(html);
      document.execCommand('insertHTML', false, cleanHtml);
      onInput();
      // Offload base64 images if user pasted images from Word
      uploadBase64Images();
      return;
    } catch (err) {
      console.warn('HTML sanitize error, falling back to text paste:', err);
    }
  }

  if (text) {
    const formatted = text
      .split('\n')
      .map(line => line.trim())
      .join('<br>');
    document.execCommand('insertHTML', false, formatted);
    onInput();
  }
};

const selectedImg = ref(null);
const customWidth = ref('');

const onEditorClick = (e) => {
  if (e.target && e.target.tagName === 'IMG') {
    if (selectedImg.value) {
      selectedImg.value.classList.remove('selected-editor-img');
    }
    selectedImg.value = e.target;
    selectedImg.value.classList.add('selected-editor-img');
    customWidth.value = selectedImg.value.style.width || selectedImg.value.getAttribute('width') || '';
  } else {
    if (selectedImg.value) {
      selectedImg.value.classList.remove('selected-editor-img');
    }
    selectedImg.value = null;
    customWidth.value = '';
  }
};

const resizeImage = (widthPercent) => {
  if (selectedImg.value) {
    selectedImg.value.style.width = widthPercent;
    selectedImg.value.style.maxWidth = '100%';
    customWidth.value = widthPercent;
    onInput();
  }
};

const onCustomWidthChange = () => {
  if (selectedImg.value && customWidth.value) {
    let val = customWidth.value.trim();
    if (/^\d+$/.test(val)) {
      val = val + 'px';
    }
    selectedImg.value.style.width = val;
    selectedImg.value.style.maxWidth = '100%';
    onInput();
  }
};

const alignImage = (position) => {
  if (selectedImg.value) {
    if (position === 'left') {
      selectedImg.value.style.marginLeft = '0';
      selectedImg.value.style.marginRight = 'auto';
      selectedImg.value.style.display = 'block';
    } else if (position === 'center') {
      selectedImg.value.style.marginLeft = 'auto';
      selectedImg.value.style.marginRight = 'auto';
      selectedImg.value.style.display = 'block';
    } else if (position === 'right') {
      selectedImg.value.style.marginLeft = 'auto';
      selectedImg.value.style.marginRight = '0';
      selectedImg.value.style.display = 'block';
    }
    onInput();
  }
};

const insertImage = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  isUploadingImage.value = true;
  try {
    const imgUrl = await courseStore.uploadImage(file);
    document.execCommand('insertImage', false, imgUrl);
    onInput();
    courseStore.showToast?.('Chèn ảnh thành công!', 'success');
  } catch (err) {
    console.error('Upload editor image error:', err);
    // Fallback nếu máy chủ upload gặp sự cố
    const reader = new FileReader();
    reader.onload = (evt) => {
      const imgUrl = evt.target.result;
      document.execCommand('insertImage', false, imgUrl);
      onInput();
    };
    reader.readAsDataURL(file);
    courseStore.showToast?.('Không thể tải ảnh lên máy chủ, đã chèn tạm ảnh base64', 'warning');
  } finally {
    isUploadingImage.value = false;
    e.target.value = ''; // Reset input file
  }
};
</script>

<style scoped>
.rich-editor-wrapper {
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  overflow: hidden;
  background: #ffffff;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.rich-editor-wrapper:focus-within {
  border-color: #0284c7;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
}

.rich-toolbar {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  flex-wrap: wrap;
}

.toolbar-btn {
  background: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  padding: 5px 10px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.toolbar-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.toolbar-btn:active, .toolbar-btn.active {
  background: #0284c7;
  color: #ffffff;
}

.toolbar-divider {
  width: 1px;
  height: 18px;
  background: #cbd5e1;
  margin: 0 4px;
}

.rich-editor-content {
  min-height: 180px;
  max-height: 450px;
  overflow-y: auto;
  padding: 14px 16px;
  color: #0f172a;
  font-size: 14px;
  line-height: 1.6;
  outline: none;
  word-break: break-word;
}

/* Triệt tiêu thụt lề khi nhảy xuống dòng hoặc dán văn bản */
.rich-editor-content :deep(p),
.rich-editor-content :deep(div),
.rich-editor-content :deep(span),
.rich-editor-content :deep(h1),
.rich-editor-content :deep(h2),
.rich-editor-content :deep(h3),
.rich-editor-content :deep(h4),
.rich-editor-content :deep(h5),
.rich-editor-content :deep(h6) {
  text-indent: 0 !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
}

.rich-editor-content :deep(p),
.rich-editor-content :deep(div) {
  margin-top: 0;
  margin-bottom: 0.75em;
  line-height: 1.6;
}

.rich-editor-content :deep(ul),
.rich-editor-content :deep(ol) {
  margin: 0.75em 0;
  padding-left: 24px !important;
  list-style-position: outside;
}

.rich-editor-content :deep(li) {
  text-indent: 0 !important;
  margin-left: 0 !important;
  padding-left: 4px !important;
  margin-bottom: 4px;
}

.rich-editor-content[placeholder]:empty:before {
  content: attr(placeholder);
  color: #94a3b8;
  cursor: text;
}

.rich-editor-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 12px 0;
  display: block;
  cursor: pointer;
  transition: outline 0.15s ease, transform 0.15s ease;
  resize: both;
}

.rich-editor-content :deep(img:hover) {
  outline: 2px dashed #0284c7;
}

.rich-editor-content :deep(img.selected-editor-img) {
  outline: 3px solid #0284c7;
}

/* Status & Size Bar */
.editor-status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  padding: 8px 14px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
  font-size: 12px;
  color: #64748b;
  user-select: none;
}

.status-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-left .stat-item strong {
  color: #0f172a;
}

.stat-divider {
  color: #cbd5e1;
}

.status-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.size-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 9999px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  font-size: 12px;
  transition: all 0.2s ease;
}

.size-indicator.status-optimal {
  border-color: #bbf7d0;
  background: #f0fdf4;
  color: #166534;
}

.size-indicator.status-optimal .status-badge {
  background: #dcfce7;
  color: #15803d;
}

.size-indicator.status-warning {
  border-color: #fde68a;
  background: #fffbeb;
  color: #854d0e;
}

.size-indicator.status-warning .status-badge {
  background: #fef3c7;
  color: #b45309;
}

.size-indicator.status-danger {
  border-color: #fecaca;
  background: #fef2f2;
  color: #991b1b;
  animation: pulse-danger 2s infinite ease-in-out;
}

.size-indicator.status-danger .status-badge {
  background: #fee2e2;
  color: #b91c1c;
}

.status-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  margin-left: 2px;
}

@keyframes pulse-danger {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15);
  }
}

.btn-clean-inline {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.25);
}

.btn-clean-inline:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-1px);
}
</style>