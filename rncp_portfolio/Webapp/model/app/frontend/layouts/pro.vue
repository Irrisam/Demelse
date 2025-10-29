<template>
  <div class="pro-layout">
    <Navbar />

    <!-- Bouton mobile -->
    <button class="hamburger" @click="toggleSidebar" aria-label="Ouvrir le menu">
      ☰
    </button>

    <!-- Drawer mobile -->
    <div class="drawer" :class="{ open: isOpen }">
      <ProSidebar />
    </div>
    <div v-if="isOpen" class="overlay" @click="closeSidebar"></div>

    <div class="content-grid">
      <!-- Sidebar desktop -->
      <aside class="sidebar-desktop">
        <ProSidebar />
      </aside>

      <!-- Contenu -->
      <main class="pro-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '@/components/Navbar.vue'
import ProSidebar from '@/components/ProSidebar.vue'

const isOpen = ref(false)
const toggleSidebar = () => (isOpen.value = !isOpen.value)
const closeSidebar = () => (isOpen.value = false)
</script>

<style scoped>
@import "~/layouts/account.css"; /* ✅ Réutilise ton style existant */
.pro-layout {
  --sidebar-w: 220px;
  --navbar-h: 64px;
}
.pro-content { background:#fff; padding:32px; border-radius:10px; }
.hamburger { position:fixed; top:12px; left:12px; display:none; }
@media (max-width:768px) {
  .hamburger { display:block; }
}
</style>
