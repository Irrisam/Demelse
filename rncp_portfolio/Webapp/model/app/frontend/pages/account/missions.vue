<template>
  <div>
    <h2>Liste des Missions</h2>

    <p v-if="loading">Chargement...</p>

    <table v-if="!loading && missions.length > 0" class="missions-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Office</th>
          <th>Date</th>
          <th>Tags</th>
          <th>Heures</th>
          <th>Pay (€)</th>
          <th>Service</th>
          <th>Spécialité</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in missions" :key="m.id">
          <td>{{ m.id }}</td>
          <td>{{ m.office_id }}</td>
          <td>{{ formatDate(m.created_at) }}</td>
          <td>{{ m.tags }}</td>
          <td>{{ m.hours }}</td>
          <td>{{ m.pay }}</td>
          <td>{{ m.service_name }}</td>
          <td>{{ m.specialty_name }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="!loading && missions.length === 0">
      Aucune mission trouvée 🙁
    </p>

    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'account' })

import { ref, onMounted, watch } from 'vue'
import { useUserIdFromToken } from '@/composables/useUserIdFromToken'

const { request } = useApi()
const { userId, fetchUserId } = useUserIdFromToken()

const missions = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

function formatDate(date: string) {
  return new Date(date).toLocaleDateString()
}

async function loadMissions() {
  try {
    const response = await request('/datas/list/missions', {
      method: 'POST',
      body: { userId: userId.value }
    })
    missions.value = response
  } catch (err) {
    error.value = 'Erreur lors de la récupération des missions'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return navigateTo('/auth/login')
  await fetchUserId(token)
})

watch(userId, async (val) => {
  if (val) await loadMissions()
})
</script>

<style scoped>
.missions-table {
  width: fit-content;
  border-collapse: collapse;
  margin-top: 20px;
}

.missions-table th,
.missions-table td {
  border: 1px solid #e5e7eb;
  padding: 10px 14px;
  text-align: left;
}

.missions-table th {
  background-color: #1f2937;
  color: white;
}

.missions-table tr:nth-child(even) {
  background-color: #f3f4f6;
}
</style>
