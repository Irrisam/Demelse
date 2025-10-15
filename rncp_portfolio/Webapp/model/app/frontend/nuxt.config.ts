export default defineNuxtConfig({
  modules: ['@primevue/nuxt-module'],
  primevue: {
    options: {
      ripple: true,
      // theme: { preset: Aura } // temporairement désactivé
    }
  },

  css: [
    'primeicons/primeicons.css',
    'primeflex/primeflex.css',
    '@/assets/css/global.css',
    'primeicons/primeicons.css',
    'primeflex/primeflex.css'
  ],

  compatibilityDate: '2025-07-15',

  devtools: { enabled: true }
})
