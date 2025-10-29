export const useApi = () => {
    const baseURL = "http://localhost:8000"
    const authToken = useState("authToken", () => null) // ✅ renommé

    const request = async (endpoint, options = {}) => {
        const headers = options.headers || {}

        if (authToken.value) {
            headers["Authorization"] = `Bearer ${authToken.value}`
        }

        const res = await $fetch(`${baseURL}${endpoint}`, {
            ...options,
            headers,
        })

        return res
    }

    return { request, authToken } // ✅ exporte sous le nouveau nom
}