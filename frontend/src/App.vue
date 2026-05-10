<script setup>
import { onMounted } from "vue";
import { RouterView } from "vue-router";
import AppNavbar from "./components/AppNavbar.vue";
import AlertToasts from "./components/AlertToasts.vue";
import { useLibrary } from "./composables/useLibrary";

const { bootstrapSession } = useLibrary();

onMounted(() => {
  bootstrapSession();
});
</script>

<template>
  <div class="d-flex flex-column min-vh-100 bg-body-secondary">
    <AppNavbar />
    <AlertToasts />
    <RouterView />
    <footer class="mt-auto py-4 text-center text-muted small border-top bg-white">
      <div class="container">Book Library · Vue client · FastAPI server</div>
    </footer>
  </div>
</template>
