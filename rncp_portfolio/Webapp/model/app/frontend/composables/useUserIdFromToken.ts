// composables/useUserIdFromToken.ts
import { ref } from "vue"
import { useApi } from "@/composables/useApi"

export function useUserIdFromToken() {
    const { request } = useApi()
    const userId = ref<string | null>(null)
    const error = ref<string | null>(null)
    const pending = ref(false)

    /**
     * Récupère l'ID utilisateur à partir d'un token JWT
     */
    async function fetchUserId(token: string) {
        if (!token) {
            error.value = "Token manquant."
            return
        }

        pending.value = true
        error.value = null
        userId.value = null

        try {
            const data = await request(`/account/id_fetch`, {
                method: "POST",
                body: { token }
            })
            console.log("📨 Réponse API :", data)
            if (data?.error) {
                error.value = data.error
            } else {
                userId.value = data.user_id ?? data
            }
        } catch (err: any) {
            error.value = err?.message || "Erreur lors de la récupération de l'ID utilisateur."
        } finally {
            pending.value = false
        }
    }

    return { userId, error, pending, fetchUserId }
}
