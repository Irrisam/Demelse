<template>
  <div>
    <h2>Liste des Professionnels</h2>

    <p v-if="loading">Chargement...</p>

    <table v-if="!loading && pros.length > 0" class="pros-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Prénom</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pro in pros" :key="pro.id">
          <td>{{ pro.id }}</td>
          <td>{{ pro.firstname }}</td>
          <td>{{ pro.lastname }}</td>
          <td>{{ pro.email }}</td>
          <td>
            <button @click="runModelFor(pro.id)">
              Catégories adaptées
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="!loading && pros.length === 0">Aucun professionnel trouvé 🙁</p>
    <p v-if="error" style="color:red">{{ error }}</p>

    <!-- ✅ MODAL -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h3>Catégories recommandées</h3>

        <p v-if="loadingModel">Analyse en cours...</p>

          <p v-else-if="errorModel" class="alert-error">
            ⚠️ {{ errorModel }}
          </p>

          <div v-else>
            <ul>
              <li v-for="(r, i) in selectedCategories" :key="i" class="result-block">
                <strong>Score global : {{ (r.final_score * 100).toFixed(1) }}%</strong>
                <ul>
                  <li v-for="c in r.categories" :key="c.name">
                    {{ c.name }} — {{ (c.score * 100).toFixed(1) }}%
                  </li>
                </ul>
              </li>
            </ul>
          </div>


        <button @click="closeModal">Fermer</button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'account' })

import { ref, onMounted, watch } from 'vue'
import { useUserIdFromToken } from '@/composables/useUserIdFromToken'

const { request } = useApi()
const { userId, fetchUserId } = useUserIdFromToken()

const pros = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

// ✅ Modal state
const showModal = ref(false)
const loadingModel = ref(false)
const selectedCategories = ref<any[]>([])
const errorModel = ref<string | null>(null)

async function loadPros() {
  try {
    const response = await request('/datas/list/pros', {
      method: 'POST',
      body: { userId: userId.value }
    })
    pros.value = response
  } catch (err) {
    error.value = "Erreur lors de la récupération des professionnels"
  } finally {
    loading.value = false
  }
}

async function runModelFor(proId: number) {
  showModal.value = true
  loadingModel.value = true
  selectedCategories.value = []
  errorModel.value = null

  try {
    console.log(`➡️ Running model for pro ${proId}`)
    const result = await request("/algos/best_categories", {
      method: "POST",
      body: { professional_id: proId }
    })

    if (result.error) {
      selectedCategories.value = []
      errorModel.value = result.message + " " + result.detail
      loadingModel.value = false
      return
    }

    console.log("✅ Résultats modèle :", result)
    selectedCategories.value = result

  } catch (err) {
    console.error(err)
    errorModel.value = "Erreur interne"
  } finally {
    loadingModel.value = false
  }
}

function closeModal() {
  showModal.value = false
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return navigateTo('/auth/login')
  await fetchUserId(token)
})

watch(userId, async (val) => {
  if (val) loadPros()
})
</script>

<style scoped>
.pros-table {
  width: fit-content;
  border-collapse: collapse;
  margin-top: 20px;
}

.pros-table th,
.pros-table td {
  border: 1px solid #e5e7eb;
  padding: 10px 14px;
  text-align: left;
}

.pros-table th {
  background-color: #1f2937;
  color: white;
}

.pros-table tr:nth-child(even) {
  background-color: #f3f4f6;
}

/* ✅ MODAL STYLE */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 12px;
  min-width: 300px;
}

.result-block {
  margin-bottom: 10px;
}
</style>
