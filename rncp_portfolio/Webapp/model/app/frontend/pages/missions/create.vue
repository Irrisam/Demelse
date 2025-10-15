<template>
  <div class="flex justify-content-center align-items-center min-h-screen bg-gray-50">
+   <Card class="w-full md:w-8 lg:w-8 xl:w-7 2xl:w-6 shadow-2">
      <template #title>
        <h2 class="text-center">Créer une mission</h2>
      </template>

      <template #content>
        <form @submit.prevent="handleCreation" class="flex flex-column gap-3">

          <div class="field">
            <label>ID Établissement </label>
            <InputText v-model.number="office_id" type="number" placeholder=" Ex : 12" class="input-bordered" />
          </div>
          <div class="field">
            <label>ID du service</label>
            <InputText v-model.number="service_id" type="number" placeholder=" Ex : 3" />
          </div>

          <div class="field">
            <label>Heure de création</label>
            <InputText v-model="created_at" type="datetime-local" />
          </div>

          <div class="field">
            <label>Tags</label>
            <InputText v-model="tags" placeholder="Ex : urgent, médical..." />
          </div>

          <div class="field">
            <label>Heures de travail</label>
            <InputText v-model.number="hours" type="number" step="0.1" placeholder="Ex : 8.5" />
          </div>

          <div class="field">
            <label>Rémunération (€)</label>
            <InputText v-model.number="pay" type="number" step="0.01" placeholder="Ex : 120.50" />
          </div>

          <div class="field">
            <label>Rôle</label>
            <InputText v-model="role" placeholder="Ex : Infirmier, Enseignant..." />
          </div>

          <Button type="submit" label="Créer la mission" class="mt-3" />

          <p v-if="error" class="text-red-500 text-center">⚠️ {{ error }}</p>
          <p v-if="response" class="text-green-600 text-center">✅ Mission créée : {{ response }}</p>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">

const { request } = useApi()

const office_id = ref<number>()
const service_id = ref<number>()
const pay = ref<number>()
const role = ref<string>("")
const tags = ref<string>("")
const hours = ref<number>()
const created_at = ref<string>("")

const error = ref<string | null>(null)
const response = ref<unknown>(null)

const handleCreation = async () => {
  error.value = null
  response.value = null
  try {
    const data = await request("/missions/create", {
      method: "POST",
      body: {office_id: office_id.value,
      service_id: service_id.value,
      pay: pay.value,
      role: role.value,
      tags: tags.value,
      hours: hours.value,
      created_at: created_at.value
    }})
    response.value = data
  } catch (err) {
    error.value = "Erreur lors de la création de la mission"
    console.error(err)
  }
}
</script>