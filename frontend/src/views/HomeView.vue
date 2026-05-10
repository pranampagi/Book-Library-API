<script setup>
import { RouterLink } from "vue-router";
import { useLibrary } from "../composables/useLibrary";

const { apiBaseUrl, isLoggedIn } = useLibrary();
</script>

<template>
  <div class="container pb-5">
    <div class="row align-items-center py-5">
      <div class="col-lg-7">
        <h1 class="display-5 fw-bold mb-3">Your personal book library</h1>
        <p class="lead text-muted mb-4">
          A Vue front end talks to your FastAPI backend over HTTPS-friendly JSON APIs. Sign in to catalog books,
          filter your collection, and discover titles from external providers.
        </p>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink v-if="!isLoggedIn" class="btn btn-primary btn-lg" to="/sign-in">Get started</RouterLink>
          <RouterLink v-else class="btn btn-primary btn-lg" to="/dashboard">Open dashboard</RouterLink>
          <a class="btn btn-outline-secondary btn-lg" :href="`${apiBaseUrl}/docs`" target="_blank" rel="noopener">
            API documentation
          </a>
        </div>
      </div>
      <div class="col-lg-5 mt-4 mt-lg-0">
        <div class="card border-0 shadow">
          <div class="card-body p-4">
            <h2 class="h6 text-muted mb-3">Backend endpoint</h2>
            <code class="d-block p-3 bg-light rounded small text-break">{{ apiBaseUrl }}</code>
            <p class="small text-muted mt-3 mb-0">
              Configure <code>VITE_API_BASE_URL</code> in <code>frontend/.env</code> for different environments.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
