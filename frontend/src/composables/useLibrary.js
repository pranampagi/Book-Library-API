/**
 * Shared library state and API actions (singleton module state).
 */
import { computed, reactive, ref } from "vue";
import {
  createBook,
  deleteBook,
  externalSearch,
  getCurrentUser,
  listBooks,
  login,
  registerUser,
  updateBook,
} from "../api";

const token = ref(localStorage.getItem("token") || "");
const user = ref(null);
const books = ref([]);
const searchResults = ref([]);
const message = ref("");
const error = ref("");
const loading = ref(false);
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

export function useLibrary() {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

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

  function clearAlerts() {
    message.value = "";
    error.value = "";
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

  async function bootstrapSession() {
    if (!token.value) return;
    await runRequest(async () => {
      user.value = await getCurrentUser(token.value);
      books.value = await listBooks(token.value, user.value.role !== "admin");
    });
  }

  async function handleRegister() {
    const username = authForm.username.trim();
    const password = authForm.password;
    if (username.length < 3) {
      setError("Username must be at least 3 characters.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    await runRequest(async () => {
      await registerUser(username, password);
    }, "User registered. You can now log in.");
  }

  async function handleLogin() {
    const username = authForm.username.trim();
    const password = authForm.password;
    if (!username || !password) {
      setError("Enter username and password.");
      return;
    }
    await runRequest(async () => {
      const payload = await login(username, password);
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

  return {
    apiBaseUrl,
    token,
    user,
    books,
    searchResults,
    message,
    error,
    loading,
    catalogQuery,
    genreFilter,
    authForm,
    bookForm,
    updateForm,
    externalForm,
    isLoggedIn,
    isAdmin,
    genres,
    filteredBooks,
    stats,
    setSuccess,
    setError,
    clearAlerts,
    bootstrapSession,
    handleRegister,
    handleLogin,
    handleLogout,
    refreshBooks,
    handleCreateBook,
    handleUpdateGenre,
    handleDeleteBook,
    handleExternalSearch,
    selectBookForGenreUpdate,
  };
}
