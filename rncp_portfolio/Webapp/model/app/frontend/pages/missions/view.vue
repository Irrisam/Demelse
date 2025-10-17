<template>
  <div class=" align-items-center min-h-screen bg-gray-50">
    <Card class="w-full">
      <template #title>
        <h2 class="text-center">Voir une mission</h2>
      </template>

      <template #content>
        <form @submit.prevent="fetchMission" class="flex flex-column gap-3">
          <div class="field">
            <label>ID de la mission</label>
            <InputText v-model="missionId" type="text" placeholder="Entrez l'ID de la mission" />
            <Button label="Rechercher" icon="pi pi-search" @click="fetchMission" />
          </div>

          <p v-if="pending">Chargement...</p>
          <p v-if="error" class="text-red-500">❌ {{ error }}</p>

          <div v-if="mission" class="mt-4">
            <h3 class="text-lg font-semibold mb-2">Détails de la mission</h3>

            <p><strong>ID :</strong> {{ mission.id }}</p>
            <p><strong>ID Établissement :</strong> {{ mission.office_id }}</p>
            <p><strong>Créée le :</strong> {{ formatDate(mission.created_at) }}</p>
            <p><strong>Tags :</strong> {{ mission.tags }}</p>
            <p><strong>Heures de travail :</strong> {{ mission.hours }} h</p>
            <p><strong>Rémunération :</strong> {{ mission.pay }} €</p>
            <p><strong>Service :</strong> {{ mission.service_name }}</p>
            <p><strong>Spécialité :</strong> {{ mission.specialty_name }}</p>


          </div>
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

async function fetchMission() {
  if (!missionId.value) {
    error.value = "Veuillez entrer un ID valide."
    return
  }

  pending.value = true
  error.value = null
  mission.value = null

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

function formatDate(dateString: string) {
  if (!dateString) return "-"
  const date = new Date(dateString)
  return date.toLocaleString("fr-FR")
}
</script>
