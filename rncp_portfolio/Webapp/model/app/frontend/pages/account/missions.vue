<template>
  <div>
    <h2>Bonjour {{ userName }}</h2>
    <p>Bienvenue sur votre espace personnel.</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'account',
})

const userName = 'Jean Dupont' // à remplacer par une donnée réelle plus tard
</script>
