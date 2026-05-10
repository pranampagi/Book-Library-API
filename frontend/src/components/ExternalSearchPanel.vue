<script setup>
import { useLibrary } from "../composables/useLibrary";

const { externalForm, searchResults, loading, handleExternalSearch } = useLibrary();
</script>

<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <h2 class="card-title h5 mb-3">External discovery</h2>
      <p class="text-muted small mb-3">Search Google Books or Open Library, then add titles from the catalog.</p>
      <div class="mb-3">
        <label class="form-label">Query</label>
        <input v-model="externalForm.query" type="search" class="form-control" placeholder="e.g. Atomic Habits" />
      </div>
      <div class="mb-3">
        <label class="form-label">Provider</label>
        <select v-model="externalForm.provider" class="form-select">
          <option value="google">Google Books</option>
          <option value="openlibrary">Open Library</option>
        </select>
      </div>
      <button type="button" class="btn btn-primary" :disabled="loading" @click="handleExternalSearch">
        Search
      </button>
      <ul v-if="searchResults.length" class="list-group list-group-flush mt-4 border rounded overflow-hidden">
        <li
          v-for="book in searchResults"
          :key="`${book.source}-${book.title}-${book.isbn}`"
          class="list-group-item"
        >
          <strong class="d-block">{{ book.title }}</strong>
          <span class="small text-muted">{{ book.authors.join(", ") || "Unknown author" }}</span>
          <span v-if="book.isbn" class="badge bg-secondary ms-2">{{ book.isbn }}</span>
        </li>
      </ul>
      <p v-else class="text-muted small mt-4 mb-0">Results appear here after you search.</p>
    </div>
  </div>
</template>
