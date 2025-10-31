import { vi } from 'vitest'
import { config } from '@vue/test-utils'
import { ref } from 'vue'

// ========================
// 🌐 Mocks Nuxt et Vue
// ========================
global.ref = ref
global.reactive = (val) => val
global.computed = (fn) => ({ value: fn() })
global.watch = vi.fn()
global.onMounted = vi.fn()
global.navigateTo = vi.fn() // ✅ manquait

// Mock de useState (Nuxt)
global.useState = vi.fn((key, init) => {
    const state = ref(init ? init() : null)
    return state
})

// Mock definePageMeta
global.definePageMeta = vi.fn()

// ========================
// 👤 useAuth
// ========================
global.useAuth = vi.fn(() => ({
    token: ref('fake-token'),
    user: ref({ id: 1, is_admin: false }),
    isLoggedIn: ref(true),
    isAdmin: ref(false),
    logout: vi.fn(),
}))

// ========================
// 👥 useUserIdFromToken
// ========================
global.useUserIdFromToken = vi.fn(() => ({
    userId: ref(19),
    error: ref(null),
    fetchUserId: vi.fn(),
}))

// ========================
// 🌍 useApi
// ========================
global.useApi = vi.fn(() => ({
    request: vi.fn(async (url: string) => {
        if (url.includes('pros')) {
            return [
                { id: 1, firstname: 'Jean', lastname: 'Dupont', email: 'jean@test.com' },
                { id: 2, firstname: 'Alice', lastname: 'Martin', email: 'alice@test.com' },
            ]
        }
        if (url.includes('missions')) {
            return [
                { id: 10, service_name: 'Urgences', specialty_name: 'Médecine', pay: 500, hours: 10 },
                { id: 11, service_name: 'Gériatrie', specialty_name: 'Soins', pay: 450, hours: 8 },
            ]
        }
        return []
    }),
}))

// ========================
// 🔗 Nuxt Components
// ========================
config.global.stubs = {
    NuxtLink: { template: '<a><slot /></a>' },
    NuxtPage: true,
    NuxtLayout: true,
}
