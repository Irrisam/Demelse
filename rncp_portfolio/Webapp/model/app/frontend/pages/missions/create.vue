<template> 
  <div class="mission_creation_page">
    <h1>Créer une mission</h1>
    <form @submit.prevent="handleCreation">
        <label>Mission à créer :</label>

        <label> ID Etab</label>
        <input v-model.number="office_id" type="number" required >

        <label> ID du service</label>
        <input v-model.number="service_id" type="number" required />

        <label> Heure de création</label>
        <input v-model="created_at" type="datetime-local" required />
        <!-- <p class="mt-2">Horaire choisi : {{ horaire }}</p> -->

        <label> Tags</label>
        <input v-model="tags" type="text" required />

        <label> Heures de travail</label>
        <input v-model.number="hours" type="number" step="0.1" required />

        <label> Rémunération</label>
        <input v-model.number="pay" type="number" step="0.01" required />

        <label> Rôle</label>
        <input v-model="role" type="text" required />

        <button type="submit"> Créer la mission </button>
    </form>
    <p v-if="error" style="color: red;">Erreur : {{ error }}</p>
    <h2> Mission créee avec l'ID: {{ response }} </h2>
</div>
</template>

<script setup lang="ts">
console.log("mission_creator.vue chargé !")

const { request, token } = useApi()

const office_id = ref<number>()
const service_id = ref<number>()
const pay = ref<number>()
const role = ref<string>("")
const tags = ref<string>("")
const hours = ref<string>("")
const created_at = ref<string>("")

const error = ref<string | null>(null)
const response = ref<unknown>(null)

const handleCreation = async () => {
  error.value = null
  response.value = null

  try {
    const data = await request("/missions/create", {
      method: "POST",
      body: {
        office_id: office_id.value,
        service_id: service_id.value,
        pay: pay.value,
        role: role.value,
        tags: tags.value,
        hours: hours.value,
        created_at: created_at.value
      }
    })

    response.value = data
  } catch (err) {
    error.value = "Erreur lors de la création de la mission"
    console.error(err)
  }
}
</script>

<style scoped>
.mission_creation_page {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
}
.mission_creation_page input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}

</style>