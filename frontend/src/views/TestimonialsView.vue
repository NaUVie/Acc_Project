<template>
  <div class="testimonials-page">
    <StudentTestimonials />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import StudentTestimonials from '@/components/StudentTestimonials.vue';

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>

<style scoped src="@/styles/views/TestimonialsView.css"></style>
