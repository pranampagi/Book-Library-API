<script setup>
import { useLibrary } from "../composables/useLibrary";

const { bookForm, loading, handleCreateBook } = useLibrary();
</script>

<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <h2 class="card-title h6 mb-3">Add book</h2>
      <div class="row g-2">
        <div class="col-12">
          <label class="form-label small mb-0">Title</label>
          <input v-model="bookForm.title" type="text" class="form-control form-control-sm" />
        </div>
        <div class="col-md-6">
          <label class="form-label small mb-0">Author</label>
          <input v-model="bookForm.author" type="text" class="form-control form-control-sm" />
        </div>
        <div class="col-md-6">
          <label class="form-label small mb-0">ISBN</label>
          <input v-model="bookForm.isbn" type="text" class="form-control form-control-sm" />
        </div>
        <div class="col-md-6">
          <label class="form-label small mb-0">Year</label>
          <input v-model="bookForm.published_year" type="number" class="form-control form-control-sm" />
        </div>
        <div class="col-md-6">
          <label class="form-label small mb-0">Genre</label>
          <input v-model="bookForm.genre" type="text" class="form-control form-control-sm" />
        </div>
        <div class="col-12">
          <label class="form-label small mb-0">Description</label>
          <textarea v-model="bookForm.description" class="form-control form-control-sm" rows="2"></textarea>
        </div>
      </div>
      <button type="button" class="btn btn-primary w-100 mt-3" :disabled="loading" @click="handleCreateBook">
        Create book
      </button>
    </div>
  </div>
</template>
