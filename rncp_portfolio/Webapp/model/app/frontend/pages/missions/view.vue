<template>
  <div class="mission-view-page">
    <h1>Détails de la mission</h1>

    <p v-if="pending">Chargement...</p>

    <p v-if="error" class="text-red-600">Erreur : {{ error }}</p>

    <div v-if="mission">
      <p><strong>ID :</strong> {{ mission.id }}</p>
      <p><strong>Établissement :</strong> {{ mission.office_id }}</p>
      <p><strong>Service :</strong> {{ mission.service_id }}</p>
      <p><strong>Créée le :</strong> {{ mission.created_at }}</p>
      <p><strong>Tags :</strong> {{ mission.tags }}</p>
      <p><strong>Heures :</strong> {{ mission.hours }}</p>
      <p><strong>Rémunération :</strong> {{ mission.pay }} €</p>
      <p><strong>Rôle :</strong> {{ mission.role }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { request } = useApi()

const mission_id = computed(() => route.params.id)

const mission = ref<any>(null)
const error = ref<string | null>(null)
const pending = ref(false)

onMounted(async () => {
  pending.value = true
  try {
    mission.value = await request(`/missions/view/${mission_id.value}`)
  } catch (err) {
    error.value = "Impossible de charger la mission"
    console.error(err)
  } finally {
    pending.value = false
  }
})
</script>

<style scoped>
.mission-view-page {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>
