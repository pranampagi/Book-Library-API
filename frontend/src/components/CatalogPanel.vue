<script setup>
import { useLibrary } from "../composables/useLibrary";

const {
  books,
  genres,
  filteredBooks,
  catalogQuery,
  genreFilter,
  loading,
  refreshBooks,
  handleDeleteBook,
  selectBookForGenreUpdate,
} = useLibrary();
</script>

<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
        <h2 class="card-title h5 mb-0">Catalog</h2>
        <button type="button" class="btn btn-outline-primary btn-sm" :disabled="loading" @click="refreshBooks">
          <span v-if="loading" class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
          Refresh
        </button>
      </div>
      <div class="row g-2 mb-3">
        <div class="col-md-8">
          <input
            v-model="catalogQuery"
            type="search"
            class="form-control"
            placeholder="Search title, author, ISBN, genre..."
            aria-label="Search catalog"
          />
        </div>
        <div class="col-md-4">
          <select v-model="genreFilter" class="form-select" aria-label="Filter by genre">
            <option v-for="genre in genres" :key="genre" :value="genre">
              {{ genre === "all" ? "All genres" : genre }}
            </option>
          </select>
        </div>
      </div>
      <div v-if="filteredBooks.length === 0" class="text-center text-muted py-5 border rounded-3 bg-light">
        No books match your filters.
      </div>
      <div v-else class="list-group list-group-flush">
        <div
          v-for="book in filteredBooks"
          :key="book.id"
          class="list-group-item list-group-item-action d-flex flex-column flex-md-row justify-content-between gap-3 py-3"
        >
          <div class="flex-grow-1 min-w-0">
            <h3 class="h6 mb-1 text-truncate">{{ book.title }}</h3>
            <p class="mb-1 small text-muted">
              {{ book.author }} · {{ book.genre || "Unknown genre" }}
            </p>
            <p class="mb-0 small"><span class="text-muted">ID</span> {{ book.id }} · ISBN {{ book.isbn || "—" }}</p>
          </div>
          <div class="d-flex flex-shrink-0 gap-2 align-items-start">
            <button
              type="button"
              class="btn btn-outline-secondary btn-sm"
              :disabled="loading"
              @click="selectBookForGenreUpdate(book)"
            >
              Edit genre
            </button>
            <button
              type="button"
              class="btn btn-outline-danger btn-sm"
              :disabled="loading"
              @click="handleDeleteBook(book.id)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      <p v-if="books.length && filteredBooks.length" class="small text-muted mt-3 mb-0">
        Showing {{ filteredBooks.length }} of {{ books.length }} books
      </p>
    </div>
  </div>
</template>
