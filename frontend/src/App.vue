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
    <SamitaLock />
  </div>
</template>

<script setup>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import ZaloChatWidget from './components/ZaloChatWidget.vue';
import SamitaLock from './components/SamitaLock.vue';
</script>

<style scoped src="@/styles/App.css"></style>
