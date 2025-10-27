<template>
    <div class="logout-container">
        <h1>Déconnexion</h1>
        <p>Vous avez été déconnecté avec succès.</p>
    </div>
</template>

<script setup lang="ts">

import { useAuth } from '@/composables/useAuth'

const { logout } = useAuth()
logout()


</script>
