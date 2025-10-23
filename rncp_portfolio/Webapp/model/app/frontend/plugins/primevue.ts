// plugins/primevue.ts
import { defineNuxtPlugin } from '#app'
import PrimeVue from 'primevue/config'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

export default defineNuxtPlugin((nuxtApp) => {
    // ✅ Empêche d'appliquer plusieurs fois le plugin
    if (!nuxtApp.vueApp._context.components.Card) {
        nuxtApp.vueApp.use(PrimeVue)

        nuxtApp.vueApp.component('Card', Card)
        nuxtApp.vueApp.component('InputText', InputText)
        nuxtApp.vueApp.component('Button', Button)
    }
})
