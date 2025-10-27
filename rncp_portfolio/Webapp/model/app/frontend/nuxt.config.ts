import Aura from '@primevue/themes/aura'

export default defineNuxtConfig({
  modules: ['@primevue/nuxt-module'],
  primevue: {
    options: {
      ripple: true,
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: false, // empêche la détection du mode sombre
          cssLayer: false
        }
      }
    }
  },

  css: [
    'primeicons/primeicons.css',
    'primeflex/primeflex.css',
    '@/assets/css/global.css'
  ],

  compatibilityDate: '2025-07-15',
  devtools: { enabled: true }
})
