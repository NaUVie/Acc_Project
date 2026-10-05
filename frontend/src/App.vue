<template>
  <div class="app-wrapper">
    <Header />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Footer />
    <ZaloChatWidget />
    <ToastNotification />
    <ConfirmModal />
  </div>
</template>

<script setup>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import ZaloChatWidget from './components/ZaloChatWidget.vue';
import ToastNotification from './components/ToastNotification.vue';
import ConfirmModal from './components/ConfirmModal.vue';
</script>

<style scoped src="@/styles/App.css"></style>
