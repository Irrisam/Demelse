<script setup lang="ts">
const auth = useAuth()
</script>

<template>
  <nav class="navbar">
    <NuxtLink to="/" class="nav-logo">Demelse</NuxtLink>

    <ul class="nav-links">
      <template v-if="auth.isLoggedIn.value === false">
        <li><NuxtLink to="/auth/login">Se connecter</NuxtLink></li>
        <li><NuxtLink to="/auth/register">Créer un compte</NuxtLink></li>
      </template>
      
      <template v-if="auth.isLoggedIn.value === true"> 
              <li><NuxtLink to="/account/home">Mon compte</NuxtLink></li>
              <li><NuxtLink to="/auth/logout">Se déconnecter</NuxtLink></li>
      </template>

      <template v-if="auth.isLoggedIn.value && auth.isAdmin.value === false">
        <li><NuxtLink to="/missions/create">Créer une mission</NuxtLink></li>
      </template>

      <template v-if="auth.isAdmin.value === true && auth.isLoggedIn.value === true">
        <li><NuxtLink to="/missions/create">Créer une mission</NuxtLink></li>
        <li><NuxtLink to="/missions/view">Voir une mission</NuxtLink></li>  
        <li><NuxtLink to="/missions/delete">Supprimer une mission</NuxtLink></li>
      </template>

    </ul>
  </nav>
</template>

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
