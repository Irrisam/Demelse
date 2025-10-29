<template>
  <nav class="side-menu">
    <ul>
      <li><NuxtLink to="/pro/home">🏠 Accueil</NuxtLink></li>
      <li><NuxtLink to="/pro/missions">📌 Missions adaptées</NuxtLink></li>
      <li><NuxtLink to="/pro/profile">👤 Mon profil</NuxtLink></li>
    </ul>
  </nav>
</template>

<style scoped>
.side-menu {
  padding: 16px;
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
  padding: 12px;
  text-decoration: none;
  border-radius: 6px;
  color: #ffffff;
}

.side-menu a:hover,
.side-menu .router-link-active {
  background: rgba(255,255,255,.25);
}
</style>
