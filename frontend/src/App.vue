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

const authForm = reactive({
  username: "",
  password: "",
});

const bookForm = reactive({
  title: "",
  author: "",
  isbn: "",
  published_year: "",
  genre: "",
  description: "",
});

const updateForm = reactive({
  id: "",
  genre: "",
});

const externalForm = reactive({
  query: "",
  provider: "google",
});

const isLoggedIn = computed(() => Boolean(token.value));

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
  }, "Login successful.");
}

function handleLogout() {
  token.value = "";
  user.value = null;
  books.value = [];
  searchResults.value = [];
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
      published_year: bookForm.published_year
        ? Number(bookForm.published_year)
        : null,
      isbn: bookForm.isbn || null,
      genre: bookForm.genre || null,
      description: bookForm.description || null,
    });
    books.value = await listBooks(token.value, user.value?.role !== "admin");
    bookForm.title = "";
    bookForm.author = "";
    bookForm.isbn = "";
    bookForm.published_year = "";
    bookForm.genre = "";
    bookForm.description = "";
  }, "Book added.");
}

async function handleUpdateGenre() {
  await runRequest(async () => {
    await updateBook(token.value, Number(updateForm.id), { genre: updateForm.genre });
    books.value = await listBooks(token.value, user.value?.role !== "admin");
  }, "Book updated.");
}

async function handleDeleteBook(id) {
  await runRequest(async () => {
    await deleteBook(token.value, id);
    books.value = books.value.filter((book) => book.id !== id);
  }, "Book deleted.");
}

async function handleExternalSearch() {
  await runRequest(async () => {
    searchResults.value = await externalSearch(
      token.value,
      externalForm.query,
      externalForm.provider,
    );
  });
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
  <main class="layout">
    <section class="panel backend">
      <h1>Book Library Backend (FastAPI)</h1>
      <p>Server URL: <code>{{ apiBaseUrl }}</code></p>
      <p>
        OpenAPI docs:
        <a :href="`${apiBaseUrl}/docs`" target="_blank">/docs</a>
      </p>
    </section>

    <section class="panel frontend">
      <h2>Book Library Client (Vue)</h2>

      <p v-if="message" class="success">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>

      <div class="grid">
        <div class="card">
          <h3>Auth</h3>
          <label>Username <input v-model="authForm.username" /></label>
          <label>Password <input v-model="authForm.password" type="password" /></label>
          <div class="row">
            <button :disabled="loading" @click="handleRegister">Register</button>
            <button :disabled="loading" @click="handleLogin">Login</button>
            <button :disabled="!isLoggedIn || loading" @click="handleLogout">Logout</button>
          </div>
          <p v-if="user">Logged in as <strong>{{ user.username }}</strong> ({{ user.role }})</p>
        </div>

        <div class="card" v-if="isLoggedIn">
          <h3>Add Book</h3>
          <label>Title <input v-model="bookForm.title" /></label>
          <label>Author <input v-model="bookForm.author" /></label>
          <label>ISBN <input v-model="bookForm.isbn" /></label>
          <label>Published Year <input v-model="bookForm.published_year" type="number" /></label>
          <label>Genre <input v-model="bookForm.genre" /></label>
          <label>Description <textarea v-model="bookForm.description" /></label>
          <button :disabled="loading" @click="handleCreateBook">Create Book</button>
        </div>

        <div class="card" v-if="isLoggedIn">
          <h3>Quick Update Genre</h3>
          <label>Book ID <input v-model="updateForm.id" type="number" /></label>
          <label>New Genre <input v-model="updateForm.genre" /></label>
          <button :disabled="loading" @click="handleUpdateGenre">Update</button>
        </div>

        <div class="card" v-if="isLoggedIn">
          <h3>External Search</h3>
          <label>Query <input v-model="externalForm.query" /></label>
          <label
            >Provider
            <select v-model="externalForm.provider">
              <option value="google">Google Books</option>
              <option value="openlibrary">Open Library</option>
            </select>
          </label>
          <button :disabled="loading" @click="handleExternalSearch">Search</button>
          <ul>
            <li v-for="book in searchResults" :key="`${book.source}-${book.title}-${book.isbn}`">
              {{ book.title }} - {{ book.authors.join(", ") || "Unknown author" }}
            </li>
          </ul>
        </div>
      </div>

      <div class="card" v-if="isLoggedIn">
        <div class="row header">
          <h3>Your Books</h3>
          <button :disabled="loading" @click="refreshBooks">Refresh</button>
        </div>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th>Genre</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book.id">
              <td>{{ book.id }}</td>
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>{{ book.isbn }}</td>
              <td>{{ book.genre }}</td>
              <td><button :disabled="loading" @click="handleDeleteBook(book.id)">Delete</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</template>
