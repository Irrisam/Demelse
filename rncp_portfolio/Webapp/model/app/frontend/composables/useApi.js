// Hook personnalisé pour gérer les appels API
export const useApi = () => {
    // URL de base de ton backend Python (ici en local)
    const baseURL = "http://localhost:8000"

    // useState crée une variable réactive partagée dans Nuxt
    // Ici, on s'en sert pour stocker le token JWT d'authentification
    const token = useState("token", () => null)

    // Fonction générique pour faire une requête API
    const request = async (endpoint, options = {}) => {
        // On récupère les headers donnés ou on crée un objet vide
        const headers = options.headers || {}

        // Si un token est présent, on ajoute automatiquement l'Authorization
        if (token.value) {
            headers["Authorization"] = `Bearer ${token.value}`
        }

        // Appel à l'API avec $fetch (helper de Nuxt qui simplifie fetch)
        const res = await $fetch(`${baseURL}${endpoint}`, {
            ...options,  // method, body, etc.
            headers,     // headers avec ou sans token
        })

        // On retourne la réponse de l'API
        return res
    }

    // On expose la fonction request + le token
    return { request, token }
}
