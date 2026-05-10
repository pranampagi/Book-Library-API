<script setup>
import { useLibrary } from "../composables/useLibrary";

const { books, updateForm, loading, handleUpdateGenre } = useLibrary();
</script>

<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <h2 class="card-title h6 mb-3">Update genre</h2>
      <label class="form-label small mb-0">Book</label>
      <select v-model="updateForm.id" class="form-select form-select-sm mb-2">
        <option :value="null">Select a book</option>
        <option v-for="book in books" :key="book.id" :value="book.id">{{ book.id }} — {{ book.title }}</option>
      </select>
      <label class="form-label small mb-0">Genre</label>
      <input v-model="updateForm.genre" type="text" class="form-control form-control-sm mb-3" placeholder="e.g. Fiction" />
      <button type="button" class="btn btn-outline-primary w-100 btn-sm" :disabled="loading" @click="handleUpdateGenre">
        Save genre
      </button>
    </div>
  </div>
</template>
