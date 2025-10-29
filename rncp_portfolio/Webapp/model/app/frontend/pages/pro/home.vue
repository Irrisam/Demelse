<template>
  <div>
    <h2>Bienvenue 👋</h2>
    <p>Voici votre espace professionnel.</p>

    <div class="cards">
      <div class="card" @click="goTo('/pro/missions')">
        📌 Missions adaptées
      </div>

      <div class="card" @click="goTo('/pro/profile')">
        🧑‍⚕️ Mon profil
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'pro',
  middleware: ['pro-guard']
})

const goTo = (path: string) => navigateTo(path)
</script>

<style scoped>
.cards {
  margin-top: 20px;
  display: flex;
  gap: 20px;
}
.card {
  cursor: pointer;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  padding: 20px;
  border-radius: 12px;
  width: 200px;
  text-align: center;
  font-size: 18px;
  transition: 0.2s;
}
.card:hover {
  background: #e5e7eb;
}
</style>
