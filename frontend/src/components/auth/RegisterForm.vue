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

function submitRegister() {
  emit("submit", { username: form.username, password: form.password });
}
</script>

<template>
  <div class="card h-100 border-0 shadow-sm">
    <div class="card-body p-4 d-flex flex-column">
      <h3 class="h5 mb-2">Register</h3>
      <p class="text-muted small mb-3">Create a new account to start cataloging books.</p>

      <label class="form-label">Username</label>
      <input
        v-model="form.username"
        class="form-control mb-3"
        type="text"
        placeholder="At least 3 characters"
        autocomplete="username"
      />

      <label class="form-label">Password</label>
      <input
        v-model="form.password"
        class="form-control"
        type="password"
        placeholder="At least 6 characters"
        autocomplete="new-password"
      />

      <p class="small text-muted mt-2 mb-0">Username minimum 3 chars, password minimum 6 chars.</p>

      <div class="mt-auto pt-4 d-grid">
        <button
          type="button"
          class="btn btn-outline-primary"
          :disabled="props.loading"
          @click="submitRegister"
        >
          Register
        </button>
      </div>
    </div>
  </div>
</template>
