<template>
  <div class="pros-missions">
    <h1>Missions disponibles</h1>

    <!-- Filtres -->
    <div class="filters">
      <button
        v-for="f in filters"
        :key="f.key"
        :class="{ active: selectedFilter === f.key }"
        @click="applyFilter(f.key)"
      >
        {{ f.label }}
      </button>
    </div>
    <!-- Tableau principal -->
    <table class="missions-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Date</th>
          <th>Service</th>
          <th>Spécialité</th>
          <th>Heures</th>
          <th>Rémunération (€)</th>
          <th>Tags</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mission in filteredMissions" :key="mission.id">
          <td>{{ mission.id }}</td>
          <td>{{ formatDate(mission.created_at) }}</td>
          <td>{{ mission.service_name }}</td>
          <td>{{ mission.specialty_name }}</td>
          <td>{{ mission.hours }}</td>
          <td>{{ mission.pay }}</td>
          <td>{{ mission.tags }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Liste des missions suggérées par le modèle -->
    <div v-if="suggestedMissions.length" class="suggested-section">
      <h2>Missions suggérées par le modèle</h2>
      <ul class="suggested-list">
        <li v-for="(s, i) in suggestedMissions" :key="i">
          <strong>{{ s.category }}</strong> — Qualité : {{ s.score }}
        </li>
      </ul>
    </div>

    <div v-else-if="!loadingCategories && !loading" class="no-suggestions">
      <p>Pas encore de suggestions générées.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import dayjs from "dayjs"
import "dayjs/locale/fr"
dayjs.locale("fr")

const { request } = useApi()
const { token } = useAuth()

const missions = ref<any[]>([])
const loading = ref(true)
const loadingCategories = ref(false)
const suggestedMissions = ref<{ category: string; score: string }[]>([])

const filters = [
  { key: "future", label: "À venir" },
  { key: "all", label: "Toutes" },
  { key: "past", label: "Passées" },
]
const selectedFilter = ref("future")
definePageMeta({ layout: 'account' })

// --- Chargement missions ---
const fetchMissions = async () => {
  loading.value = true
  try {
    missions.value = await request("/all_pro_missions_fetch", { method: "GET" })
  } catch (err) {
    console.error("Erreur chargement missions :", err)
  } finally {
    loading.value = false
  }
}
onMounted(fetchMissions)

// --- Formatage de date
const formatDate = (dateStr: string) => {
  if (!dateStr) return "—"
  const clean = dateStr.replace(" ", "T")
  const parsed = dayjs(clean)
  return parsed.isValid() ? parsed.format("DD/MM/YYYY HH:mm") : "—"
}

// --- Filtres
const filteredMissions = computed(() => {
  if (!missions.value) return []
  const now = dayjs()
  if (selectedFilter.value === "future") {
    return missions.value.filter((m) =>
      dayjs(m.created_at.replace(" ", "T")).isAfter(now)
    )
  }
  if (selectedFilter.value === "past") {
    return missions.value.filter((m) =>
      dayjs(m.created_at.replace(" ", "T")).isBefore(now)
    )
  }
  return missions.value
})
const applyFilter = (key: string) => (selectedFilter.value = key)

// --- Récupération missions suggérées via modèle
const fetchCategories = async () => {
  loadingCategories.value = true
  try {
    // 1️⃣ Récupération de l'ID utilisateur via le token
    const idResponse = await request("/account/id_fetch", {
      method: "POST",
      body: { token: token.value },
    })
    const professionalId = idResponse?.id || idResponse

    if (!professionalId) {
      console.warn("Impossible de récupérer l'ID utilisateur.")
      loadingCategories.value = false
      return
    }

    // 2️Récupération des suggestions via le modèle
    const response = await request("/algos/best_categories", {
      method: "POST",
      body: { professional_id: professionalId },
    })

    if (response && Array.isArray(response)) {
      suggestedMissions.value = response.map((entry: any) => {
        const [data, score] = entry
        const category = data[1][0]
        const formattedScore = (score / 10000).toFixed(1).replace(".", ",")
        return { category, score: formattedScore }
      })
    }
  } catch (err) {
    console.error("Erreur lors de l'appel du modèle :", err)
  } finally {
    loadingCategories.value = false
  }
}
</script>


<style scoped>
.pros-missions {
  max-width: 1000px;
  margin: 40px auto;
  padding: 20px;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filters button {
  border: 1px solid #ccc;
  background: white;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.filters button.active {
  background: #007bff;
  color: white;
}

.missions-table {
  width: 100%;
  border-collapse: collapse;
}

.missions-table th,
.missions-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.missions-table th {
  background-color: #f5f5f5;
}

.loading {
  text-align: center;
  font-style: italic;
}
</style>
