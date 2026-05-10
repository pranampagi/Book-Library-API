<script setup>
import { useRouter } from "vue-router";
import { useLibrary } from "../composables/useLibrary";

const router = useRouter();
const {
  authForm,
  loading,
  isLoggedIn,
  handleRegister,
  handleLogin,
} = useLibrary();

async function onLogin() {
  await handleLogin();
  if (isLoggedIn.value) {
    const redirect = router.currentRoute.value.query.redirect;
    router.push(typeof redirect === "string" ? redirect : "/dashboard");
  }
}
</script>

<template>
  <div class="card shadow-sm border-0">
    <div class="card-body p-4">
      <h2 class="card-title h4 mb-3">Authentication</h2>
      <p class="text-muted small mb-4">Create an account or sign in to manage your library.</p>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Username</label>
          <input
            v-model="authForm.username"
            type="text"
            class="form-control"
            placeholder="e.g. admin"
            autocomplete="username"
          />
        </div>
        <div class="col-md-6">
          <label class="form-label">Password</label>
          <input
            v-model="authForm.password"
            type="password"
            class="form-control"
            placeholder="Password"
            autocomplete="current-password"
          />
        </div>
      </div>
      <p class="text-muted small mb-0 mt-2">Username at least 3 characters; password at least 6.</p>
      <div class="d-flex flex-wrap gap-2 mt-4">
        <button type="button" class="btn btn-outline-secondary" :disabled="loading" @click="handleRegister">
          Register
        </button>
        <button type="button" class="btn btn-primary px-4" :disabled="loading" @click="onLogin">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
          Sign in
        </button>
      </div>
    </div>
  </div>
</template>
