<template>
  <div class="missions_index">
    <h1>Missions</h1>
    
    <p v-if="error" style="color: red;">Erreur : {{ error }}</p>

    <nuxt-link to="/missions/view" class="mission-link">
      Go lookup une mission
    </nuxt-link>

    <nuxt-link to="/missions/create" class="mission-link">
      Go créer une mission
    </nuxt-link>
  </div>
</template>

<style scoped>
.missions_index {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.mission-link {
  display: block;
  margin-bottom: 10px;
  color: #007bff;
  text-decoration: none;
}

.mission-link:hover {
  text-decoration: underline;
}
</style>
