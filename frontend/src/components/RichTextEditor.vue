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
      <button type="button" class="toolbar-btn" @click="format('insertUnorderedList')" title="Danh sách gạch đầu dòng">• Danh sách</button>
      <button type="button" class="toolbar-btn" @click="format('insertOrderedList')" title="Danh sách đánh số">1. Danh sách</button>
      <span class="toolbar-divider"></span>
      <button type="button" class="toolbar-btn" @click="addLink" title="Chèn đường dẫn (Link)">🔗 Link</button>
      <button type="button" class="toolbar-btn" @click="format('removeFormat')" title="Xóa định dạng">🧹 Xóa định dạng</button>
    </div>

    <!-- Editable Content Area -->
    <div
      ref="editorRef"
      class="rich-editor-content"
      contenteditable="true"
      @input="onInput"
      @blur="onBlur"
      :placeholder="placeholder"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

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
  max-height: 400px;
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
</style>
