<script setup lang="ts">
const { isLoggedIn } = useAuth()
</script>

<template>
  <nav class="navbar">
    <NuxtLink to="/" class="nav-logo">Mission Manager</NuxtLink>

    <ul class="nav-links">
      <li><NuxtLink to="/missions/create">Créer une mission</NuxtLink></li>
      <li><NuxtLink to="/missions/view">Voir une mission</NuxtLink></li>
      <li><NuxtLink to="/missions/delete">Supprimer une mission</NuxtLink></li>

      <template v-if="!isLoggedIn">
        <li><NuxtLink to="/auth/login">Se connecter</NuxtLink></li>
        <li><NuxtLink to="/auth/register">Créer un compte</NuxtLink></li>
      </template>

      <template v-else>
        <li><NuxtLink to="/account">Mon compte</NuxtLink></li>
      </template>
    </ul>
  </nav>
</template>


<script setup lang="ts">

</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #3b82f6;
  padding: 12px 24px;
  border-radius: 8px;
}

.nav-logo {
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 20px;
  list-style: none;
}

.nav-links a {
  color: white;
  text-decoration: none;
  transition: opacity 0.2s;
}

.nav-links a:hover {
  opacity: 0.8;
}

.router-link-active {
  text-decoration: underline;
  font-weight: bold;
}
</style>
