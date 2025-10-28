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
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h3>Catégories recommandées</h3>

        <p v-if="loadingModel">Analyse en cours...</p>

        <p v-else-if="errorModel" class="alert-error">
          ⚠️ {{ errorModel }}
        </p>

        <div v-else-if="selectedCategories.length">
          <div
            v-for="(item, i) in selectedCategories"
            :key="i"
            class="recommendation-item"
          >
            <strong class="global-score">
              {{
                Math.round(
                  (item.final_score / selectedCategories[0].final_score) * 100
                )
              }}%
            </strong>

            <div class="badges">
              <span
                v-for="cat in item.categories"
                :key="cat.name"
                class="badge"
              >
                {{ categoryLabels[cat.name.toLowerCase()] || cat.name }}
              </span>
            </div>

            <button class="mission-btn" @click="fetchRecommendedMissions(item)">
              Voir missions adaptées
            </button>
          </div>
        </div>

        <div v-if="recommendedMissions.length" class="mission-results">
          
          <h4>Missions proposées :</h4>
          <ul>
            <li v-for="m in recommendedMissions" :key="m.id">
              📍 {{ m.service_name }} — {{ m.specialty_name }}
              ({{ m.pay }}€ / {{ m.hours }}h)
            </li>
          </ul>
        </div>
        <button class="mission-btn" @click="closeModal">Fermer</button>
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

const showModal = ref(false)
const loadingModel = ref(false)
const selectedCategories = ref<any[]>([])
const errorModel = ref<string | null>(null)
const recommendedMissions = ref<any[]>([])
const loadingMissions = ref(false)


const categoryLabels: Record<string, string> = {
  clinic: "Clinique privée",
  urgences: "Urgences",
  reanimation: "Réanimation",
  bloc_op: "Bloc opératoire",
  chirurgie: "Chirurgie",
  endocrino: "Endocrinologie",
  geriatrie: "Gériatrie",
  medecine_generale: "Médecine générale",
  medecine_interne: "Médecine interne",
  medecine_specialite: "Spécialités médicales",
  ssr: "SSR",
  unite_de_soin: "Unité de soins",
  biology: "Biologie médicale",
  day: "Jour",
  night: "Nuit",
}

const serviceIdMap: Record<string, number> = {
  urgences: 9,
  reanimation: 30,
  bloc_op: 45,
  chirurgie: 5,
  endocrino: 41,
  geriatrie: 4,
  medecine_generale: 28,
  medecine_interne: 3,
  medecine_specialite: 42,
  ssr: 32,
  unite_de_soin: 44,
  biology: 11,
}

const establishmentIdMap: Record<string, number> = {
  teleconsult: 1,
  clinic: 2,
  hospi: 3,
}

async function fetchRecommendedMissions(reco: any) {
  if (!reco) return

  loadingMissions.value = true
  recommendedMissions.value = []

  try {
    const response = await request("/datas/list/missions", {
      method: "POST",
      body: { userId: userId.value }
    })

    const service = reco.categories.find((c: any) =>
      Object.keys(serviceIdMap).includes(c.name.toLowerCase())
    )

    const rythme = reco.categories.find((c: any) =>
      ["day", "night"].includes(c.name.toLowerCase())
    )

    const etab = reco.categories.find((c: any) =>
      Object.keys(establishmentIdMap).includes(c.name.toLowerCase())
    )

    console.log("🎯 Filtrage basé sur :", {
      service: service?.name,
      rythme: rythme?.name,
      etab: etab?.name
    })

    function match(mission: any, srv = true, rtm = true, et = true) {
      const serviceMatch =
        !srv ||
        (service && mission.service_id === serviceIdMap[service.name.toLowerCase()])
      const rythmeMatch =
        !rtm ||
        (rythme && mission.tags.toLowerCase().includes(rythme.name.toLowerCase()))
      const etabMatch =
        !et ||
        (etab && mission.office_id === establishmentIdMap[etab.name.toLowerCase()])

      return serviceMatch && rythmeMatch && etabMatch
    }

    // 🔥 Priorité 1 → Full match
    recommendedMissions.value = response.filter((m: any) => match(m, true, true, true))

    if (recommendedMissions.value.length === 0) {
      console.warn("⚠️ Aucun match strict → fallback service + rythme")
      recommendedMissions.value = response.filter((m: any) => match(m, true, true, false))
    }

    if (recommendedMissions.value.length === 0) {
      console.warn("⚠️ Aucun match service + rythme → fallback service uniquement")
      recommendedMissions.value = response.filter((m: any) => match(m, true, false, false))
    }

    console.log("✅ Missions adaptées trouvées :", recommendedMissions.value)

  } catch (err) {
    console.error(err)
  } finally {
    loadingMissions.value = false
  }
}




async function loadPros() {
  try {
    const response = await request('/datas/list/pros', {
      method: 'POST',
      body: { userId: userId.value }
    })
    pros.value = response
  } catch {
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
  recommendedMissions.value = []

  try {
    console.log(`➡️ Running model for pro ${proId}`)
    const result = await request("/algos/best_categories", {
      method: "POST",
      body: { professional_id: proId }
    })

    selectedCategories.value = result
    console.log("✅ Résultats modèle :", result)

  } catch {
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
/* 🎨 Styles conservation telle quelle */
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
.recommendation-item {
  border: 1px solid #ddd;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #f8fafc;
}
.badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.badge {
  background: #e0f2fe;
  color: #0369a1;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
}
.global-score {
  font-size: 18px;
  color: #1e40af;
}
.mission-btn {
  background: #2563eb;
  color: white;
  border-radius: 6px;
  padding: 6px 10px;
  margin-top: 8px;
  font-size: 14px;
  cursor: pointer;
}
.mission-btn:hover {
  background: #1e40af;
}
.mission-results {
  margin-top: 10px;
  background: #eef2ff;
  padding: 10px;
  border-radius: 6px;
}
</style>
