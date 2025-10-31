<template>
  <div>
    <Navbar />
    <main class="page-container">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import Navbar from "@/components/Navbar.vue"
</script>

<style scoped>
.page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: #f1f5f9; /* 💙 ton bleu-gris clair */
}
</style>
