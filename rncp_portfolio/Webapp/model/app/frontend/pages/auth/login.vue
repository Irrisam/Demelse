<template>
  <div class="login-page">
    <h1>Connexion</h1>

    <!-- Formulaire -->
    <form @submit.prevent="handleLogin">
      <label>Email :</label>
      <input v-model="email" type="email" required />

      <label>Mot de passe :</label>
      <input v-model="password" type="password" required />

      <button type="submit">Se connecter</button>
    </form>

    <p v-if="error" style="color: red;">Erreur : {{ error }}</p>

    <nuxt-link to="/auth/register">

      Pas encore de compte ? En créer un ici !
    </nuxt-link>

  </div>
</template>

<script setup lang="ts">
const email = ref("")
const password = ref("")
const error = ref<string | null>(null)
const response = ref<unknown>(null)

const { request } = useApi()
const { login, isAdmin, token } = useAuth()

const handleLogin = async () => {
  try {
    const data = await request("/auth/login", {
      method: "POST",
      body: { email: email.value, password: password.value },
    })

    response.value = data
    const jwt = data?.access_token?.access_token

    
    if (jwt && typeof jwt === 'string') {
      localStorage.setItem('token', jwt)
      login(jwt)
      console.log("Admin ?", isAdmin.value)
      await navigateTo("/account/home")
    } else {
      error.value = "Token manquant dans la réponse."
    }

  } catch (err) {
    error.value = "Identifiants incorrects ou erreur réseau"
    console.error(err)
  }
}
</script>


<style scoped>
.login-page {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.login-page input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}
</style>
