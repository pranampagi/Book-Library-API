<script setup>
import CatalogPanel from "../components/CatalogPanel.vue";
import AddBookForm from "../components/AddBookForm.vue";
import BookGenreForm from "../components/BookGenreForm.vue";
</script>

<template>
  <div class="container pb-5">
    <h1 class="h3 mb-4">Catalog</h1>
    <div class="row g-4">
      <div class="col-lg-8">
        <CatalogPanel />
      </div>
      <div class="col-lg-4">
        <div class="d-flex flex-column gap-3">
          <AddBookForm />
          <BookGenreForm />
        </div>
      </div>
    </div>
  </div>
</template>
