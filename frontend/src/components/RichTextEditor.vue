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
    </div>

    <!-- Editable Content Area -->
    <div
      ref="editorRef"
      class="rich-editor-content"
      contenteditable="true"
      @input="onInput"
      @blur="onBlur"
      @click="onEditorClick"
      :placeholder="placeholder"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
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
</style>
