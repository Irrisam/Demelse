<template>
  <div>
    <h2>Bonjour {{ userName }}</h2>
    <p>Bienvenue sur votre espace personnel.</p>
    <button @click="handleLogout">Se déconnecter</button>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'account',
})

import { ref, watch, onMounted } from 'vue'
import { useUserIdFromToken } from '@/composables/useUserIdFromToken'

const { request } = useApi()
const userName = ref('Jean Dupont') // à remplacer plus tard
const token = ref(localStorage.getItem('token') || '') // par ex. récupéré depuis le localStorage
const { userId, error, pending, fetchUserId } = useUserIdFromToken()
const handleLogout = async () => {
  try {
    await request('/auth/logout', { method: 'POST' })
    localStorage.removeItem('token') // au cas où
    await navigateTo('/auth/login')
  } catch (err) {
    console.error('Erreur lors de la déconnexion :', err)
  }
}
async function getId() {
  await fetchUserId(token.value)
}
console.log("🔹 Token actuel :", token.value)
onMounted(() => {
  if (token.value) getId()
})
// 🔹 On surveille les changements de userId
watch(userId, (newVal) => {
  if (newVal) {
    console.log("✅ ID utilisateur :", newVal)
  }
watch(error, (err) => {
  if (err) {
    console.warn("❌ Erreur lors de la récupération de l'ID :", err)
    // Optionnel : rediriger ou notifier l'utilisateur
  }
})
 
})
</script>
