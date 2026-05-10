<script setup>
import RegisterForm from "../components/auth/RegisterForm.vue";
import { useLibrary } from "../composables/useLibrary";

const { loading, handleRegister } = useLibrary();

async function onRegister(payload) {
  await handleRegister(payload.username, payload.password);
}
</script>

<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-12 col-md-7 col-lg-5">
        <RegisterForm :loading="loading" @submit="onRegister" />
        <p class="text-center text-muted small mt-3 mb-0">
          Already have an account?
          <router-link to="/sign-in" class="text-decoration-none">Sign in</router-link>.
        </p>
      </div>
    </div>
  </div>
</template>
