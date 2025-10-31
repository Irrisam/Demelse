<template>
  <div class="home-sections">

    <!-- HERO -->
    <section class="hero-card">
      <h1>Bienvenue sur <span class="highlight">Demelse</span></h1>
    <p class="hero-text">
      Une plateforme moderne dédiée aux professionnels de santé et aux établissements.
      Gagnez du temps, simplifiez vos missions et découvrez des opportunités adaptées à votre profil.
    </p>

      <div class="hero-actions">
        <NuxtLink to="/auth/register" class="btn primary">Créer un compte</NuxtLink>
        <NuxtLink to="/auth/login" class="btn secondary">Se connecter</NuxtLink>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <div class="feature-card">
        <h2>👩‍⚕️ Pour les Professionnels</h2>
        <p>
          Trouvez des missions correspondant à vos disponibilités et à votre spécialité.
          Notre IA vous suggère les meilleures opportunités selon votre profil.
        </p>
      </div>

      <div class="feature-card">
        <h2>🏥 Pour les Établissements</h2>
        <p>
          Publiez facilement vos missions et recevez des candidatures de praticiens qualifiés.
          Suivez vos collaborations depuis votre espace dédié.
        </p>
      </div>

      <div class="feature-card">
        <h2>⚙️ Une expérience fluide</h2>
        <p>
          Interface simple, claire et rapide,tout est pensé pour optimiser votre temps.
        </p>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'home'
})
</script>

<style scoped>
:root {
  --blue: #2563eb;
  --blue-dark: #1e3a8a;
  --bg-page: #f8fafc;
  --text-main: #1e293b;
  --text-dim: #475569;
  --card-bg: #ffffff;
  --card-shadow: 0 4px 14px rgba(0,0,0,0.05);
  --card-radius: 16px;
}

.home-sections {
  width: 100%;
  max-width: 1000px;
  margin-top: 60px;
  display: flex;
  flex-direction: column;
  gap: 40px;
  color: var(--text-main);
}

.hero-card {
  background: var(--card-bg);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: 48px 24px;
  text-align: center;
}

.hero-card h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 16px;
  line-height: 1.2;
}

.highlight {
  color: var(--blue);
}

.hero-text {
  color: var(--text-dim);
  font-size: 1.05rem;
  line-height: 1.6;
  max-width: 650px;
  margin: 0 auto 32px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px,100%), 1fr));
  gap: 20px;
}

.feature-card {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(37, 99, 235, 0.08);
  padding: 24px 20px;
  color: var(--text-main);
  min-height: 170px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.feature-card h2 {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 10px;
}

.feature-card p {
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--text-dim);
}

.cta-card {
  background: var(--card-bg);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: 40px 24px;
  text-align: center;
  margin-bottom: 60px;
}

.cta-title {
  color: var(--text-main);
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.cta-text {
  color: var(--text-dim);
  max-width: 520px;
  margin: 0 auto 28px;
  line-height: 1.5;
  font-size: 0.95rem;
}

.cta-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
}

.btn {
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  line-height: 1.2;
  transition: all 0.15s ease;
  min-width: 150px;
  text-align: center;
  cursor: pointer;
}

.btn.primary {
  background: var(--blue);
  color: #fff !important;
  border: 2px solid var(--blue);
}

.btn.primary:hover {
  background: var(--blue-dark);
  color: #fff !important;
}

.btn.secondary {
  background: #fff;
  color: var(--blue-dark) !important;
  border: 2px solid var(--blue);
}

.btn.secondary:hover {
  background: var(--blue);
  color: #fff !important;
}

.hero-actions .btn,
.cta-actions .btn {
  display: inline-block;
  text-align: center;
  font-weight: 600;
  border-radius: 8px;
  min-width: 160px;
  padding: 12px 22px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none !important;
}


.hero-actions .btn.primary,
.cta-actions .btn.primary {
  background-color: #2563eb !important;
  color: #fff !important;
  border: 2px solid #2563eb !important;
}

.hero-actions .btn.primary:hover,
.cta-actions .btn.primary:hover {
  background-color: #1e3a8a !important;
  border-color: #1e3a8a !important;
}


.hero-actions .btn.secondary,
.cta-actions .btn.secondary {
  background-color: #ffffff !important;
  color: #1e3a8a !important;
  border: 2px solid #2563eb !important;
}

.hero-actions .btn.secondary:hover,
.cta-actions .btn.secondary:hover {
  background-color: #2563eb !important;
  color: #ffffff !important;
}

</style>
