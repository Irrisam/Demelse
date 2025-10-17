<template>
  <div class="flex justify-content-center align-items-center min-h-screen">
+   <Card class="w-full">
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
            <label>Service</label>
            <InputText v-model="service_name" placeholder=" Ex: Biology" />
          </div>

          <div class="field">
            <label>Specialty</label>
            <InputText v-model="specialty_name" placeholder=" Ex: Specialty" />
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
            <InputText v-model.number="hours" type="number"  placeholder="Ex : 8.5" />
          </div>

          <div class="field">
            <label>Rémunération (€)</label>
            <InputText v-model.number="pay" type="number" placeholder="Ex : 120.50" />
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
const service_name = ref<string>("")
const specialty_name = ref<string>("")
const pay = ref<number>()
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
      body: 
        {office_id: office_id.value,
        service_name: service_name.value,
        specialty_name: specialty_name.value,
        pay: pay.value,
        tags: tags.value,
        hours: hours.value,
        created_at: created_at.value}
      })
    response.value = data
  } catch (err) {
    error.value = "Erreur lors de la création de la mission"
    console.error(err)
  }
}
</script>