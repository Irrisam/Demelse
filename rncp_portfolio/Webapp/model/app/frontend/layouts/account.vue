<template>
  <div class="account-layout">
    <!-- Navbar globale (inchangée) -->
    <Navbar />

    <!-- Bouton hamburger (mobile uniquement) -->
    <button class="hamburger" @click="toggleSidebar" aria-label="Ouvrir le menu">
      ☰
    </button>

    <!-- Drawer mobile -->
    <div class="drawer" :class="{ open: isOpen }" role="dialog" aria-modal="true">
      <Sidebar />
    </div>
    <div v-if="isOpen" class="overlay" @click="closeSidebar" aria-hidden="true"></div>

    <!-- Grille principale -->
    <div class="content-grid">
      <!-- Sidebar desktop -->
      <aside class="sidebar-desktop">
        <Sidebar />
      </aside>

      <!-- Contenu -->
      <main class="account-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '~/components/Navbar.vue'
import Sidebar from '~/components/Sidebar.vue'

const isOpen = ref(false)
const toggleSidebar = () => (isOpen.value = !isOpen.value)
const closeSidebar = () => (isOpen.value = false)
</script>

<style scoped>
/* ===== Variables (adapte la hauteur si besoin) ===== */
.account-layout { --sidebar-w: 220px; --navbar-h: 64px; }

/* ===== Hamburger (mobile) ===== */
.hamburger {
  position: fixed;        /* reste en haut */
  top: 12px;
  left: 12px;
  font-size: 28px;
  background: transparent;
  border: none;
  color: #fff;
  z-index: 110;           /* au-dessus de la navbar */
  display: none;
}
@media (max-width: 768px) {
  .hamburger { display: block; }
}

/* ===== Grille principale ===== */
.content-grid {
  display: grid;
  grid-template-columns: 1fr; /* mobile: une colonne */
  gap: 0;
  background: #f3f4f6;
  min-height: calc(100vh - var(--navbar-h));
  padding: 24px;
}

/* ===== Sidebar desktop (toujours visible) ===== */
.sidebar-desktop {
  display: none;
  background: #60a5fa;
  border-radius: 8px;
  color: #fff;
  /* sticky évite tout chevauchement avec la navbar */
  position: sticky;
  top: 16px;
  align-self: start;
  height: calc(100vh - var(--navbar-h) - 32px);
  overflow: auto;
  padding: 16px 0;
}

@media (min-width: 769px) {
  .content-grid {
    grid-template-columns: var(--sidebar-w) 1fr; /* 2 colonnes */
  }
  .sidebar-desktop { display: block; }
}

/* ===== Contenu ===== */
.account-content {
  background: #f9fafb;
  border-radius: 8px;
  padding: 32px;
  min-height: 60vh;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}

/* ===== Drawer mobile ===== */
.drawer {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-w);
  height: 100vh;
  background: #60a5fa;
  padding-top: var(--navbar-h);   /* démarre sous la navbar visuelle */
  transform: translateX(-100%);
  transition: transform .3s ease-in-out;
  z-index: 120;
  overflow-y: auto;
  border-right: 1px solid rgba(0,0,0,.08);
}
.drawer.open { transform: translateX(0); }

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.4);
  z-index: 100;
}

/* Cache le drawer en desktop */
@media (min-width: 769px) {
  .drawer, .overlay, .hamburger { display: none !important; }
}

.user-infos-boxes {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
}
</style>
