<template>
  <div class="pros-missions">
    <h1>Missions suggérées par le modèle</h1>

    <div class="actions">
      <button class="model-button" @click="fetchSuggestedMissions" :disabled="loading">
        <span v-if="!loading">Charger les missions suggérées</span>
        <span v-else>Chargement en cours...</span>
      </button>
    </div>

    <div v-if="suggestedMissions.length" class="suggested-section">
      <ul class="suggested-list">
        <li v-for="(m, i) in suggestedMissions" :key="i" class="suggested-item">
          <div class="category">
            <strong>{{ m.categories.join(' / ') }}</strong>
            <div class="score">Qualité : {{ m.score }}</div>
          </div>
          <button
            class="show-button"
            @click="fetchMatchingMissions(m.categories)"
            :disabled="loadingMatches"
          >
            Voir les missions
          </button>
        </li>
      </ul>
    </div>

    <!-- Résultats des missions correspondantes -->
<div v-if="matchingMissions.length" class="matches-section">
  <h2>📋 Missions correspondantes</h2>
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
      <tr v-for="m in matchingMissions" :key="m.id">
        <td>{{ m.id }}</td>
        <td>{{ formatDate(m.created_at) }}</td>
        <td>{{ m.service_name }}</td>
        <td>{{ m.specialty_name }}</td>
        <td>{{ m.hours }}</td>
        <td>{{ m.pay }}</td>
        <td>{{ m.tags }}</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Message “aucune mission” -->
<div
  v-else-if="!loadingMatches && suggestedMissions.length && noResults"
  class="no-results"
>
  <p>💭 Aucune mission correspondante pour ces critères pour le moment.</p>
  <p class="sub">🔄 N’hésite pas à réessayer plus tard !</p>
</div>

    <div v-else-if="!loadingMatches && !loading && !suggestedMissions.length">
      <p>Aucune mission suggérée pour le moment.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import dayjs from "dayjs"
import "dayjs/locale/fr"
definePageMeta({ layout: 'account' })
dayjs.locale("fr")

const { request } = useApi()
const { token } = useAuth()

const loading = ref(false)
const loadingMatches = ref(false)
const suggestedMissions = ref<any[]>([])
const matchingMissions = ref<any[]>([])



const fetchSuggestedMissions = async () => {
  loading.value = true
  suggestedMissions.value = []
  matchingMissions.value = []

  try {
    const idResponse = await request("/account/id_fetch", {
      method: "POST",
      body: { token: token.value },
    })
    const professionalId = idResponse?.id || idResponse

    const response = await request("/algos/best_categories", {
      method: "POST",
      body: { professional_id: professionalId },
    })

    if (response && Array.isArray(response)) {
      suggestedMissions.value = response.map((entry: any) => {
        const cats = entry.categories?.map((c: any) => c.name) || []
        const formattedScore = (entry.final_score / 1000).toFixed(1).replace(".", ",")
        return { categories: cats, score: formattedScore }
      })
    }
  } catch (err) {
    console.error("Erreur modèle :", err)
  } finally {
    loading.value = false
  }
}

const noResults = ref(false)

const fetchMatchingMissions = async (categories: string[]) => {
  loadingMatches.value = true
  matchingMissions.value = []
  noResults.value = false

  try {
    const response = await request("/algos/missions_by_categories", {
      method: "POST",
      body: { categories },
    })

    if (Array.isArray(response) && response.length > 0) {
      matchingMissions.value = response
    } else {
      noResults.value = true
    }
  } catch (err) {
    console.error("Erreur lors du fetch des missions :", err)
    noResults.value = true
  } finally {
    loadingMatches.value = false
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return "—"
  const parsed = dayjs(dateStr.replace(" ", "T"))
  return parsed.isValid() ? parsed.format("DD/MM/YYYY HH:mm") : "—"
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
.no-results {
  margin-top: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  text-align: center;
  color: #444;
}

.no-results .sub {
  font-size: 0.9rem;
  color: #777;
  margin-top: 4px;
}
</style>
