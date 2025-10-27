<template>
 <div v-if="data && data.firstname">
  <h2>Bonjour {{ data.lastname }} {{ data.firstname }}</h2>

  <div class="user-infos-boxes">
    <label>
      Nom :
      <input v-if="editMode" v-model="editForm.firstname" />
      <strong v-else>{{ data.firstname }}</strong>
    </label>

    <label>
      Prénom :
      <input v-if="editMode" v-model="editForm.lastname" />
      <strong v-else>{{ data.lastname }}</strong>
    </label>

    <label>
      Email :
      <input v-if="editMode" v-model="editForm.email" />
      <strong v-else>{{ data.email }}</strong>
    </label>
  </div>


  <button v-if="!editMode" @click="enableEdit">Modifier mes infos</button>

  <div v-else class="edit-actions">
    <button @click="saveChanges">Enregistrer</button>
    <button @click="cancelEdit">Annuler</button>
  </div>
</div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'account' })

import { ref, watch, onMounted } from 'vue'
import { useUserIdFromToken } from '@/composables/useUserIdFromToken'

const { request } = useApi()
const { userId, error, fetchUserId } = useUserIdFromToken()
const token = ref('')
const data = ref({
  firstname: '',
  lastname: '',
  email: '',
})
const editMode = ref(false)
const editForm = ref({
  firstname: '',
  lastname: '',
  email: '',
})

function enableEdit() {
  editForm.value = {
    firstname: data.value.firstname,
    lastname: data.value.lastname,
    email: data.value.email,
  }
  editMode.value = true
}

function cancelEdit() {
  editMode.value = false
}

async function saveChanges() {
  try {
    const result = await request('/auth/info_update', {
      method: 'PUT',
      body: {
        user_id: userId.value,
        name: editForm.value.lastname,
        first_name: editForm.value.firstname,
        email: editForm.value.email,
      },
    })

    if (result.success) {
      data.value = { ...data.value, ...editForm.value }
      editMode.value = false
      alert('✅ Informations mises à jour')
    }
  } catch (err) {
    console.error(err)
    alert('❌ Erreur lors de la mise à jour')
  }
}

async function getUserId() {
  if (token.value) {
    await fetchUserId(token.value)
  }
}

async function fetchUserData() {
  if (!userId.value) return
  try {
    const response = await request(`/account/user_info/`, {
      method: 'POST',
      body: { userId: userId.value },
    })
    data.value = response
    console.log('✅ Données utilisateur :', data.value)
  } catch (err) {
    console.error('Erreur lors de la récupération des infos utilisateur :', err)
  }
}

// 🔹 Déconnexion
async function handleLogout() {
  try {
    await request('/auth/logout', { method: 'POST' })
    localStorage.removeItem('token')
    await navigateTo('/auth/login')
  } catch (err) {
    console.error('Erreur lors de la déconnexion :', err)
  }
}

// 🔹 Lifecycle
onMounted(async () => {
  token.value = localStorage.getItem('token') || ''

  if (!token.value) {
    return navigateTo('/auth/login')
  }

  await fetchUserId(token.value)
})

watch(userId, async (newVal) => {
  if (newVal) await fetchUserData()
})

// 🔹 Réagit au changement de userId
watch(userId, async (newVal) => {
  if (newVal) {
    console.log('✅ ID utilisateur :', newVal)
    await fetchUserData()
  }
})

watch(error, (err) => {
  if (err) {
    console.warn('❌ Erreur lors de la récupération de l’ID :', err)
  }
})
</script>
