<template>
  <div class="flex justify-content-center align-items-center min-h-screen bg-gray-50">
    <Card class="w-full md:w-8 lg:w-8 xl:w-7 2xl:w-6 shadow-2">
      <template #title>
        <h2 class="text-center">Supprimer une mission</h2>
      </template>

      <template #content>
        <form @submit.prevent="fetchMission" class="flex flex-column gap-3">

          <div class="field">
            <label>ID de la mission</label>
            <InputText v-model="missionId" type="text" placeholder="Entrez l'ID de la mission" />
            <Button label="Rechercher" icon="pi pi-search" class="mt-2" @click="fetchMission" />
          </div>

          <p v-if="pending">Chargement...</p>
          <p v-if="error" class="text-red-500">❌ {{ error }}</p>

          <div v-if="mission" class="mt-4">
            <h3 class="text-lg font-semibold mb-2">Détails de la mission</h3>

            <p><strong>ID :</strong> {{ mission.id }}</p>
            <p><strong>ID Établissement :</strong> {{ mission.office_id }}</p>
            <p><strong>ID Service :</strong> {{ mission.service_id }}</p>
            <p><strong>Créée le :</strong> {{ formatDate(mission.created_at) }}</p>
            <p><strong>Tags :</strong> {{ mission.tags }}</p>
            <p><strong>Heures de travail :</strong> {{ mission.hours }} h</p>
            <p><strong>Rémunération :</strong> {{ mission.pay }} €</p>
            <p><strong>Rôle :</strong> {{ mission.role }}</p>

            <Button label="Supprimer cette mission" severity="danger" class="mt-3" @click="confirmDelete" />
          </div>

          <p v-if="successMessage" class="text-green-600 mt-3">✅ {{ successMessage }}</p>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
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
