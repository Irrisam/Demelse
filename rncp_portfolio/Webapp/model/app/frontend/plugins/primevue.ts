import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(PrimeVue, {
        theme: {
            preset: Aura
        }
    })

    nuxtApp.vueApp.component('Card', Card)
    nuxtApp.vueApp.component('InputText', InputText)
    nuxtApp.vueApp.component('Button', Button)
})
