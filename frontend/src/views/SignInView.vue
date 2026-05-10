<script setup>
import { useRouter } from "vue-router";
import SignInForm from "../components/auth/SignInForm.vue";
import { useLibrary } from "../composables/useLibrary";

const router = useRouter();
const { loading, isLoggedIn, handleLogin } = useLibrary();

async function onSignIn(payload) {
  await handleLogin(payload.username, payload.password);
  if (isLoggedIn.value) {
    const redirect = router.currentRoute.value.query.redirect;
    router.push(typeof redirect === "string" ? redirect : "/dashboard");
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-12 col-md-7 col-lg-5">
        <SignInForm :loading="loading" @submit="onSignIn" />
        <p class="text-center text-muted small mt-3 mb-0">
          New here?
          <router-link to="/register" class="text-decoration-none">Create an account</router-link>.
        </p>
      </div>
    </div>
  </div>
</template>
