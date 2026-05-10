<script setup>
import { useLibrary } from "../composables/useLibrary";

const { stats, isAdmin } = useLibrary();
</script>

<template>
  <div class="card shadow-sm border-0 h-100">
    <div class="card-body">
      <h2 class="card-title h5 mb-4">Library insights</h2>
      <div class="row g-3">
        <div class="col-6 col-lg-3">
          <div class="border rounded-3 p-3 text-center bg-light">
            <div class="display-6 fw-bold text-primary">{{ stats.total }}</div>
            <div class="small text-muted">Total books</div>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="border rounded-3 p-3 text-center bg-light">
            <div class="display-6 fw-bold text-primary">{{ stats.uniqueAuthors }}</div>
            <div class="small text-muted">Authors</div>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="border rounded-3 p-3 text-center bg-light">
            <div class="display-6 fw-bold text-primary">{{ stats.withIsbn }}</div>
            <div class="small text-muted">With ISBN</div>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="border rounded-3 p-3 text-center bg-light">
            <div class="h4 fw-bold text-primary mb-0">{{ isAdmin ? "Admin" : "User" }}</div>
            <div class="small text-muted">Access</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
