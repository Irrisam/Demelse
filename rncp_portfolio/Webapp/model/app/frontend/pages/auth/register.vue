<template>
  <div class="register-page">
    <h1>Inscription</h1>

    <form @submit.prevent="handleRegister">
      <label>Email :</label>
      <input v-model="email" type="email" required />

        <label>Name :</label>
        <input v-model="name"/>

        <label>First Name :</label>
      <input v-model="first_name"/>

      <label>Mot de passe :</label>
      <input v-model="password" type="password" required />

      <label>Confirmer mot de passe :</label>
      <input v-model="confirmPassword" type="password" required />

      <button type="submit">S’inscrire</button>

        <NuxtLink to="/auth/login">
      Déjà un compte ? Se connecter
    </NuxtLink>
    </form>

    <p v-if="error" style="color: red;">Erreur : {{ error }}</p>
    <pre>{{ response }}</pre>
  </div>
</template>

<script setup lang="ts">
const { request } = useApi()

const name = ref("")
const first_name = ref("")
const email = ref("")
const password = ref("")
const confirmPassword = ref("")
const error = ref<string | null>(null)
const response = ref<unknown>(null)

const handleRegister = async () => {
  error.value = null
  response.value = null

  if (password.value !== confirmPassword.value) {
    error.value = "Les mots de passe ne correspondent pas."
    return
  }

  try {
    const data = await request("/auth/register", {
      method: "POST",
      body: { name: name.value, first_name: first_name.value, email: email.value, password: password.value }
    })
    response.value = data
  } catch (err) {
    error.value = "Erreur lors de l’inscription"
    console.error(err)
  }
}
</script>

<style scoped>
.register-page {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.register-page input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}
</style>
