import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SignInView from "../views/SignInView.vue";
import DashboardView from "../views/DashboardView.vue";
import CatalogView from "../views/CatalogView.vue";
import DiscoverView from "../views/DiscoverView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView, meta: { title: "Home" } },
  { path: "/sign-in", name: "sign-in", component: SignInView, meta: { title: "Sign in" } },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { requiresAuth: true, title: "Dashboard" },
  },
  {
    path: "/catalog",
    name: "catalog",
    component: CatalogView,
    meta: { requiresAuth: true, title: "Catalog" },
  },
  {
    path: "/discover",
    name: "discover",
    component: DiscoverView,
    meta: { requiresAuth: true, title: "Discover" },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || "Book Library"} · Book Library`;
  const loggedIn = Boolean(localStorage.getItem("token"));
  if (to.meta.requiresAuth && !loggedIn) {
    next({ name: "sign-in", query: { redirect: to.fullPath } });
    return;
  }
  if (to.name === "sign-in" && loggedIn) {
    next({ name: "dashboard" });
    return;
  }
  next();
});

export default router;
