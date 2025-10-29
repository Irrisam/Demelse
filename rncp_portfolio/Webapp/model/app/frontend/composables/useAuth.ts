// useAuth.ts
export const useAuth = () => {
    const token = useCookie<string | null>('token', {
        default: () => null,
        watch: true,
    })

    const isAdmin = useCookie<boolean | null>('is_admin', {
        default: () => null,
        watch: true,
    })

    const isLoggedIn = computed(() => !!token.value)

    const login = (newToken: string) => {
        token.value = newToken

        try {
            const payload = JSON.parse(atob(newToken.split('.')[1]))
            // le backend renvoie { "is_admin": { "is_admin": false } }
            isAdmin.value = typeof payload.is_admin === 'object'
                ? payload.is_admin.is_admin
                : payload.is_admin
        } catch (err) {
            console.error('Erreur décodage JWT:', err)
            isAdmin.value = false
        }
    }

    const logout = () => {
        token.value = null
        isAdmin.value = null
    }

    return {
        token,
        isAdmin,
        isLoggedIn,
        login,
        logout,
    }
}
