<script setup>
import { RouterLink } from "vue-router";
import InsightsPanel from "../components/InsightsPanel.vue";
import { useLibrary } from "../composables/useLibrary";

const { apiBaseUrl } = useLibrary();
</script>

<template>
  <div class="container pb-5">
    <h1 class="h3 mb-4">Dashboard</h1>
    <InsightsPanel class="mb-4" />
    <div class="row g-3">
      <div class="col-md-4">
        <RouterLink class="text-decoration-none" to="/catalog">
          <div class="card h-100 shadow-sm border-0 hover-shadow transition">
            <div class="card-body">
              <h2 class="h5 card-title">Catalog</h2>
              <p class="card-text text-muted small mb-0">Browse, search, add, and edit books in your library.</p>
            </div>
          </div>
        </RouterLink>
      </div>
      <div class="col-md-4">
        <RouterLink class="text-decoration-none" to="/discover">
          <div class="card h-100 shadow-sm border-0 hover-shadow transition">
            <div class="card-body">
              <h2 class="h5 card-title">Discover</h2>
              <p class="card-text text-muted small mb-0">Look up metadata from Google Books or Open Library.</p>
            </div>
          </div>
        </RouterLink>
      </div>
      <div class="col-md-4">
        <a class="text-decoration-none" :href="`${apiBaseUrl}/docs`" target="_blank" rel="noopener">
          <div class="card h-100 shadow-sm border-0 hover-shadow transition">
            <div class="card-body">
              <h2 class="h5 card-title">API docs</h2>
              <p class="card-text text-muted small mb-0">Open Swagger UI for full REST exploration.</p>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hover-shadow:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08) !important;
}
.transition {
  transition: box-shadow 0.2s ease;
}
</style>
