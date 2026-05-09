<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import {
  createBook,
  deleteBook,
  externalSearch,
  getCurrentUser,
  listBooks,
  login,
  registerUser,
  updateBook,
} from "./api";

const token = ref(localStorage.getItem("token") || "");
const user = ref(null);
const books = ref([]);
const searchResults = ref([]);
const message = ref("");
const error = ref("");
const loading = ref(false);
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const catalogQuery = ref("");
const genreFilter = ref("all");

const authForm = reactive({ username: "", password: "" });
const bookForm = reactive({
  title: "",
  author: "",
  isbn: "",
  published_year: "",
  genre: "",
  description: "",
});
const updateForm = reactive({ id: null, genre: "" });
const externalForm = reactive({ query: "", provider: "google" });

const isLoggedIn = computed(() => Boolean(token.value));
const isAdmin = computed(() => user.value?.role === "admin");
const genres = computed(() => {
  const unique = new Set(books.value.map((book) => book.genre).filter(Boolean));
  return ["all", ...Array.from(unique)];
});
const filteredBooks = computed(() => {
  const query = catalogQuery.value.trim().toLowerCase();
  return books.value.filter((book) => {
    const matchesQuery =
      !query ||
      [book.title, book.author, book.isbn, book.genre]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(query));
    const matchesGenre =
      genreFilter.value === "all" || (book.genre || "unknown") === genreFilter.value;
    return matchesQuery && matchesGenre;
  });
});
const stats = computed(() => {
  const total = books.value.length;
  const withIsbn = books.value.filter((book) => book.isbn).length;
  const uniqueAuthors = new Set(books.value.map((book) => book.author)).size;
  return { total, withIsbn, uniqueAuthors };
});

function setSuccess(text) {
  message.value = text;
  error.value = "";
}

function setError(text) {
  error.value = text;
  message.value = "";
}

async function runRequest(action, successMessage) {
  loading.value = true;
  try {
    await action();
    if (successMessage) {
      setSuccess(successMessage);
    }
  } catch (err) {
    setError(err.message);
  } finally {
    loading.value = false;
  }
}

async function handleRegister() {
  await runRequest(async () => {
    await registerUser(authForm.username, authForm.password);
  }, "User registered. You can now log in.");
}

async function handleLogin() {
  await runRequest(async () => {
    const payload = await login(authForm.username, authForm.password);
    token.value = payload.access_token;
    localStorage.setItem("token", token.value);
    user.value = await getCurrentUser(token.value);
    books.value = await listBooks(token.value, user.value.role !== "admin");
    authForm.password = "";
  }, "Login successful.");
}

function handleLogout() {
  token.value = "";
  user.value = null;
  books.value = [];
  searchResults.value = [];
  catalogQuery.value = "";
  genreFilter.value = "all";
  localStorage.removeItem("token");
  setSuccess("Logged out.");
}

async function refreshBooks() {
  await runRequest(async () => {
    books.value = await listBooks(token.value, user.value?.role !== "admin");
  });
}

async function handleCreateBook() {
  await runRequest(async () => {
    await createBook(token.value, {
      ...bookForm,
      published_year: bookForm.published_year ? Number(bookForm.published_year) : null,
      isbn: bookForm.isbn || null,
      genre: bookForm.genre || null,
      description: bookForm.description || null,
    });
    books.value = await listBooks(token.value, user.value?.role !== "admin");
    Object.assign(bookForm, {
      title: "",
      author: "",
      isbn: "",
      published_year: "",
      genre: "",
      description: "",
    });
  }, "Book added.");
}

async function handleUpdateGenre() {
  if (!updateForm.id || !updateForm.genre.trim()) {
    setError("Choose a book and provide a genre.");
    return;
  }
  await runRequest(async () => {
    await updateBook(token.value, Number(updateForm.id), { genre: updateForm.genre.trim() });
    books.value = await listBooks(token.value, user.value?.role !== "admin");
    updateForm.id = null;
    updateForm.genre = "";
  }, "Book updated.");
}

async function handleDeleteBook(id) {
  await runRequest(async () => {
    await deleteBook(token.value, id);
    books.value = books.value.filter((book) => book.id !== id);
  }, "Book deleted.");
}

async function handleExternalSearch() {
  if (!externalForm.query.trim()) {
    setError("Enter a search query.");
    return;
  }
  await runRequest(async () => {
    searchResults.value = await externalSearch(
      token.value,
      externalForm.query,
      externalForm.provider,
    );
  });
}

function selectBookForGenreUpdate(book) {
  updateForm.id = book.id;
  updateForm.genre = book.genre || "";
}

onMounted(async () => {
  if (!token.value) {
    return;
  }
  await runRequest(async () => {
    user.value = await getCurrentUser(token.value);
    books.value = await listBooks(token.value, user.value.role !== "admin");
  });
});
</script>

<template>
  <main class="app-shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">Client-Server Application</p>
        <h1>Book Library Control Center</h1>
        <p class="muted">
          Backend:
          <code>{{ apiBaseUrl }}</code>
          ·
          <a :href="`${apiBaseUrl}/docs`" target="_blank">API docs</a>
        </p>
      </div>
      <div class="status-card">
        <p class="muted">Session</p>
        <p v-if="user">
          <strong>{{ user.username }}</strong>
          <span class="pill">{{ user.role }}</span>
        </p>
        <p v-else>Not logged in</p>
      </div>
    </header>

    <section v-if="message" class="toast success">{{ message }}</section>
    <section v-if="error" class="toast error">{{ error }}</section>

    <section class="grid auth-grid">
      <article class="card">
        <h2>Authentication</h2>
        <p class="muted">Register or sign in to manage your library.</p>
        <div class="form-grid">
          <label>Username <input v-model="authForm.username" placeholder="e.g. admin" /></label>
          <label
            >Password
            <input v-model="authForm.password" type="password" placeholder="Password"
          /></label>
        </div>
        <div class="actions">
          <button :disabled="loading" @click="handleRegister">Register</button>
          <button class="primary" :disabled="loading" @click="handleLogin">Login</button>
          <button class="ghost" :disabled="!isLoggedIn || loading" @click="handleLogout">
            Logout
          </button>
        </div>
      </article>

      <article v-if="isLoggedIn" class="card stats">
        <h2>Library Insights</h2>
        <div class="stat-grid">
          <div>
            <p class="stat-number">{{ stats.total }}</p>
            <p class="muted">Total books</p>
          </div>
          <div>
            <p class="stat-number">{{ stats.uniqueAuthors }}</p>
            <p class="muted">Unique authors</p>
          </div>
          <div>
            <p class="stat-number">{{ stats.withIsbn }}</p>
            <p class="muted">With ISBN</p>
          </div>
          <div>
            <p class="stat-number">{{ isAdmin ? "Admin" : "User" }}</p>
            <p class="muted">Access level</p>
          </div>
        </div>
      </article>
    </section>

    <section v-if="isLoggedIn" class="workspace">
      <article class="card">
        <div class="section-head">
          <h2>Catalog</h2>
          <button class="ghost" :disabled="loading" @click="refreshBooks">Refresh</button>
        </div>
        <div class="toolbar">
          <input v-model="catalogQuery" placeholder="Search by title, author, ISBN, genre..." />
          <select v-model="genreFilter">
            <option v-for="genre in genres" :key="genre" :value="genre">
              {{ genre === "all" ? "All genres" : genre }}
            </option>
          </select>
        </div>
        <div v-if="filteredBooks.length === 0" class="empty-state">No books match your filters.</div>
        <div v-else class="book-list">
          <article v-for="book in filteredBooks" :key="book.id" class="book-item">
            <div>
              <h3>{{ book.title }}</h3>
              <p class="muted">{{ book.author }} · {{ book.genre || "Unknown genre" }}</p>
              <p class="meta">ID {{ book.id }} · ISBN {{ book.isbn || "N/A" }}</p>
            </div>
            <div class="actions">
              <button class="ghost" :disabled="loading" @click="selectBookForGenreUpdate(book)">
                Edit Genre
              </button>
              <button class="danger" :disabled="loading" @click="handleDeleteBook(book.id)">
                Delete
              </button>
            </div>
          </article>
        </div>
      </article>

      <aside class="side-stack">
        <article class="card">
          <h2>Add Book</h2>
          <div class="form-grid">
            <label>Title <input v-model="bookForm.title" /></label>
            <label>Author <input v-model="bookForm.author" /></label>
            <label>ISBN <input v-model="bookForm.isbn" /></label>
            <label>Published Year <input v-model="bookForm.published_year" type="number" /></label>
            <label>Genre <input v-model="bookForm.genre" /></label>
            <label class="full"
              >Description <textarea v-model="bookForm.description" rows="3"
            /></label>
          </div>
          <button class="primary" :disabled="loading" @click="handleCreateBook">Create Book</button>
        </article>

        <article class="card">
          <h2>Update Genre</h2>
          <label>
            Book
            <select v-model="updateForm.id">
              <option :value="null">Select a book</option>
              <option v-for="book in books" :key="book.id" :value="book.id">
                {{ book.id }} - {{ book.title }}
              </option>
            </select>
          </label>
          <label>Genre <input v-model="updateForm.genre" placeholder="e.g. Fiction" /></label>
          <button :disabled="loading" @click="handleUpdateGenre">Save Genre</button>
        </article>

        <article class="card">
          <h2>External Discovery</h2>
          <label>Query <input v-model="externalForm.query" placeholder="e.g. Atomic Habits" /></label>
          <label>
            Provider
            <select v-model="externalForm.provider">
              <option value="google">Google Books</option>
              <option value="openlibrary">Open Library</option>
            </select>
          </label>
          <button :disabled="loading" @click="handleExternalSearch">Search</button>
          <ul v-if="searchResults.length" class="results">
            <li v-for="book in searchResults" :key="`${book.source}-${book.title}-${book.isbn}`">
              <strong>{{ book.title }}</strong>
              <p class="muted">{{ book.authors.join(", ") || "Unknown author" }}</p>
            </li>
          </ul>
        </article>
      </aside>
    </section>
  </main>
</template>
