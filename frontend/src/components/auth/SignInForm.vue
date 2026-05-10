<script setup>
import { reactive } from "vue";

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["submit"]);

const form = reactive({
  username: "",
  password: "",
});

function submitSignIn() {
  emit("submit", { username: form.username, password: form.password });
}
</script>

<template>
  <div class="card h-100 border-0 shadow-sm">
    <div class="card-body p-4 d-flex flex-column">
      <h3 class="h5 mb-2">Sign in</h3>
      <p class="text-muted small mb-3">Use your existing account credentials.</p>

      <label class="form-label">Username</label>
      <input
        v-model="form.username"
        class="form-control mb-3"
        type="text"
        placeholder="Enter username"
        autocomplete="username"
      />

      <label class="form-label">Password</label>
      <input
        v-model="form.password"
        class="form-control"
        type="password"
        placeholder="Enter password"
        autocomplete="current-password"
      />

      <div class="mt-auto pt-4 d-grid">
        <button type="button" class="btn btn-primary" :disabled="props.loading" @click="submitSignIn">
          <span v-if="props.loading" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
          Sign in
        </button>
      </div>
    </div>
  </div>
</template>
