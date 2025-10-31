<template>
  <div class="home-layout">
    <Navbar />
    <main class="home-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import Navbar from "@/components/Navbar.vue"
</script>

<style scoped>
.home-layout {
  background: #e9effd; /* ✅ bleu pastel accessible */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Le contenu principal */
.home-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 80px;
  padding-left: 16px;
  padding-right: 16px;
}

/* Optionnel : effet subtil de gradient */
.home-layout {
  background: linear-gradient(180deg, #e9effd 0%, #f8fafc 100%);
}
</style>

