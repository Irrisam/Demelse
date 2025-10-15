<template>
  <div class="mission-view">
    <h1>Supprimer une mission</h1>

    <div class="input-section">
      <input
        v-model="missionId"
        type="text"
        placeholder="Entrez l'ID de la mission"
      />
      <button @click="fetchMission">Rechercher</button>
    </div>

    <p v-if="pending">Chargement...</p>
    <p v-if="error" class="error">Erreur : {{ error }}</p>

    <div v-if="mission" class="mission-details">
      <h2>Détails de la mission</h2>

      <p><strong>ID :</strong> {{ mission.id }}</p>
      <p><strong>ID Établissement :</strong> {{ mission.office_id }}</p>
      <p><strong>ID Service :</strong> {{ mission.service_id }}</p>
      <p><strong>Créée le :</strong> {{ formatDate(mission.created_at) }}</p>
      <p><strong>Tags :</strong> {{ mission.tags }}</p>
      <p><strong>Heures de travail :</strong> {{ mission.hours }} h</p>
      <p><strong>Rémunération :</strong> {{ mission.pay }} €</p>
      <p><strong>Rôle :</strong> {{ mission.role }}</p>

       <button class="delete-btn" @click="confirmDelete">Supprimer cette mission</button>
       
    </div>
     <p v-if="successMessage" class="success">{{ successMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const { request } = useApi()

const missionId = ref<string>("")
const mission = ref<any>(null)
const error = ref<string | null>(null)
const pending = ref<boolean>(false)
const successMessage = ref<string | null>(null)

async function fetchMission() {
  if (!missionId.value) {
    error.value = "ID introuvable."
    return
  }
  try {
  const data = await request(`/missions/view/${missionId.value}`, {
    method: "GET",
  })
  console.log("Mission récupérée :", data)
  mission.value = data
} catch (err: any) {
  error.value = err?.message || "Erreur lors du chargement."
}
  pending.value = true
  error.value = null
  mission.value = null
  successMessage.value = null
  

  try {
    const data = await request(`/missions/view/${missionId.value}`, {
      method: "GET",
    })
    mission.value = data
  } catch (err: any) {
    error.value = err?.message || "Erreur lors du chargement."
  } finally {
    pending.value = false
  }
}

async function confirmDelete() {
  if (!mission.value) return

  const confirmed = window.confirm(
    `Voulez-vous vraiment supprimer la mission #${mission.value.id} ?`
  )

  if (!confirmed) return

  try {
    await request(`/missions/delete/${mission.value.id}`, {
      method: "DELETE",
    })

    successMessage.value = `Mission #${mission.value.id} supprimée avec succès ✅`
    mission.value = null
  } catch (err: any) {
    error.value = err?.message || "Erreur lors de la suppression."
  }
}

function formatDate(dateString: string) {
  if (!dateString) return "-"
  const date = new Date(dateString)
  return date.toLocaleString("fr-FR")
}
</script>

<style scoped>
.mission-view {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.input-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 8px;
}

button {
  padding: 8px 12px;
  cursor: pointer;
}

.error {
  color: red;
}

.mission-details {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}
</style>
