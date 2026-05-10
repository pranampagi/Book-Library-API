<script setup>
import { useLibrary } from "../composables/useLibrary";

const { message, error } = useLibrary();

function dismissSuccess() {
  message.value = "";
}
function dismissError() {
  error.value = "";
}
</script>

<template>
  <div class="container mb-3">
    <div v-if="message" class="alert alert-success alert-dismissible fade show" role="alert">
      {{ message }}
      <button type="button" class="btn-close" aria-label="Close" @click="dismissSuccess"></button>
    </div>
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button type="button" class="btn-close" aria-label="Close" @click="dismissError"></button>
    </div>
  </div>
</template>
