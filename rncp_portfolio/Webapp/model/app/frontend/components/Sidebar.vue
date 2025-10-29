<template>
  <nav class="side-menu">
    <ul>
      <li><NuxtLink to="/account/home">Mon profil</NuxtLink></li>

      <template v-if="auth.isAdmin.value === true">
      <li><NuxtLink to="/account/pros">Pros</NuxtLink></li>
      <li><NuxtLink to="/account/missions">Missions</NuxtLink></li>
      </template>

      <template v-if="auth.isAdmin.value === false">
      <li><NuxtLink to="/pros/missions">Liste des missions</NuxtLink></li>
      <li><NuxtLink to="/pros/missions_suggested">Missions suggérées par IA</NuxtLink></li>
      </template>
    </ul>
  </nav>
</template>

<script setup lang="ts">
const auth = useAuth()
</script>
<style scoped>
.side-menu ul { list-style: none; padding: 0; margin: 0; }
.side-menu li { margin: 12px 0; }
.side-menu a {
  display: block;
  padding: 10px 16px;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
.side-menu a:hover, .side-menu .router-link-active { background: #3b82f6; }
</style>
