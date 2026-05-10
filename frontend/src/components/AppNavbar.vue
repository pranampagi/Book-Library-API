<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useLibrary } from "../composables/useLibrary";

const route = useRoute();
const router = useRouter();
const { user, isLoggedIn, handleLogout, clearAlerts } = useLibrary();

const navClass = computed(() =>
  route.meta.requiresAuth ? "navbar-dark bg-primary shadow-sm" : "navbar-dark bg-dark",
);

function onLogout() {
  clearAlerts();
  handleLogout();
  router.push({ name: "home" });
}
</script>

<template>
  <nav class="navbar navbar-expand-lg mb-4" :class="navClass">
    <div class="container">
      <router-link class="navbar-brand fw-semibold" to="/">Book Library</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navMain"
        aria-controls="navMain"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="navMain" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" active-class="active" to="/">Home</router-link>
          </li>
          <template v-if="isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link" active-class="active" to="/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" active-class="active" to="/catalog">Catalog</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" active-class="active" to="/discover">Discover</router-link>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" active-class="active" to="/sign-in">Sign in</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" active-class="active" to="/register">Register</router-link>
            </li>
          </template>
        </ul>
        <div v-if="isLoggedIn && user" class="d-flex align-items-center gap-2 text-white small">
          <span class="text-white-50">Signed in as</span>
          <span class="fw-medium">{{ user.username }}</span>
          <span class="badge bg-light text-primary">{{ user.role }}</span>
          <button type="button" class="btn btn-outline-light btn-sm" @click="onLogout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>
