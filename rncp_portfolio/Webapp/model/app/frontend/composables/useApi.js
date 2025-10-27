// Hook personnalisé pour gérer les appels API
export const useApi = () => {

    const baseURL = "http://localhost:8000"

    const token = useState("token", () => null)


    const request = async (endpoint, options = {}) => {

        const headers = options.headers || {}


        if (token.value) {
            headers["Authorization"] = `Bearer ${token.value}`
        }


        const res = await $fetch(`${baseURL}${endpoint}`, {
            ...options,
            headers,
        })


        return res
    }

    return { request, token }
}
