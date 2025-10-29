<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <h3>Admin</h3>

      <nav>
        <ul>
          <li><NuxtLink to="/account/home">Dashboard</NuxtLink></li>
          <li><NuxtLink to="/account/pros">Professionnels</NuxtLink></li>
          <li><NuxtLink to="/account/missions">Missions</NuxtLink></li>
        </ul>
      </nav>

      <button class="logout" @click="logout">Déconnexion</button>
    </aside>

    <main class="content">
      <slot />
    </main>
  </div>
</template>

<script setup>
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('is_admin')
  navigateTo('/auth/login')
}
</script>

<style>
.admin-layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 220px;
  background: #1f2937;
  color: white;
  padding: 20px;
}

.sidebar a {
  display: block;
  padding: 8px 0;
  color: #cbd5e1;
  text-decoration: none;
}

.sidebar a:hover {
  color: white;
}

.logout {
  margin-top: 20px;
  width: 100%;
  background: #ef4444;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.content {
  flex: 1;
  padding: 20px;
  background: #f9fafb;
}
</style>
