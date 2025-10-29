<script setup lang="ts">
const { isAdmin } = useAuth()
</script>

<template>
  <nav class="side-menu">
    <ul>

      <!-- 👤 Visible pour tous -->
      <li>
        <NuxtLink to="/account/home">Mon profil</NuxtLink>
      </li>

      <!-- 👑 Menu Admin -->
      <template v-if="isAdmin">
        <li><NuxtLink to="/account/pros">Professionnels</NuxtLink></li>
        <li><NuxtLink to="/account/missions">Missions</NuxtLink></li>
        <li><NuxtLink to="/account/refresher">Réentrainer IA</NuxtLink></li>
      </template>

      <!-- 🧑‍⚕️ Menu Pro -->
      <template v-else>
        <li><NuxtLink to="/pro/missions">Missions adaptées</NuxtLink></li>
        <li><NuxtLink to="/pro/profile">Modifier mon profil</NuxtLink></li>
      </template>

    </ul>
  </nav>
</template>

<style scoped>
.side-menu {
  width: 240px;
  background: #1e293b;
  height: 100vh;
  padding: 20px;
}

.side-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side-menu li {
  margin: 12px 0;
}

.side-menu a {
  display: block;
  padding: 10px 16px;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 15px;
  transition: background 0.2s;
}

.side-menu a:hover,
.side-menu .router-link-active {
  background: #3b82f6;
}
</style>
