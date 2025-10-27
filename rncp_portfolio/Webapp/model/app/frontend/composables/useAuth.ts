export const useAuth = () => {
    const token = useCookie<string | null>('token', {
        default: () => null,
        watch: true,
    })

    const isLoggedIn = computed(() => !!token.value)

    const login = (newToken: string) => {
        token.value = newToken
    }

    const logout = () => {
        token.value = null
    }

    return {
        token,
        isLoggedIn,
        login,
        logout,
    }
}
