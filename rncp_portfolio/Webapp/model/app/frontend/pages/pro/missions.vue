<template>
  <div>
    <h2>Missions adaptées pour vous</h2>

    <p v-if="loading">Analyse en cours... 🔍</p>

    <ul v-if="!loading && recommendedMissions.length > 0" class="missions-list">
      <li v-for="m in recommendedMissions" :key="m.id" class="mission-item">
        <strong>{{ m.service_name }}</strong> — {{ m.specialty_name }}
        <br>
        {{ m.pay }}€ pour {{ m.hours }}h 📍 ({{ formatDate(m.created_at) }})
      </li>
    </ul>

    <p v-if="!loading && recommendedMissions.length === 0">
      Aucune mission ne correspond pour le moment 😕
    </p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'account',
  middleware: ['pro-guard']
})

import { ref, onMounted, watch } from 'vue'
import { useUserIdFromToken } from '@/composables/useUserIdFromToken'

const { request } = useApi()
const { userId, fetchUserId } = useUserIdFromToken()

const recommendedMissions = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

function formatDate(date: string) {
  return new Date(date).toLocaleDateString()
}

// ✅ On réutilise le modèle ML comme sur la page admin
async function loadRecommendedMissions() {
  loading.value = true

  try {
    const reco = await request("/algos/best_categories", {
      method: "POST",
      body: { professional_id: userId.value }
    })

    if (!Array.isArray(reco)) {
      recommendedMissions.value = []
      return
    }

    const serviceId = reco[0]?.categories?.find((c: any) => c.name !== "day" && c.name !== "night")?.name
    if (!serviceId) {
      recommendedMissions.value = []
      return
    }

    const missions = await request("/datas/list/missions", {
      method: "POST",
      body: { userId: userId.value }
    })

    recommendedMissions.value = missions.filter((m: any) =>
      m.service_name.toLowerCase() === serviceId.toLowerCase()
    )
  } catch (err) {
    error.value = "Erreur lors de la récupération des missions"
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
  if (val) await loadRecommendedMissions()
})
</script>

<style scoped>
.missions-list {
  list-style: none;
  padding: 0;
}

.mission-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  background: #f8fafc;
  margin-bottom: 10px;
}

.error {
  color: red;
}
</style>
