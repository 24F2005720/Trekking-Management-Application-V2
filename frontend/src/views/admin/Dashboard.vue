<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { apiFetch } from "../../api";
import { auth, clearAuth } from "../../stores/auth";

const stats = ref(null);
const router = useRouter();

onMounted(async () => {
  stats.value = await apiFetch("/api/admin/stats");
});

function logout() {
  clearAuth();
  router.push("/login");
}
</script>

<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
    <span class="navbar-brand">Admin - {{ auth.name }}</span>
    <div class="navbar-nav me-auto">
      <router-link class="nav-link" to="/admin">Overview</router-link>
      <router-link class="nav-link" to="/admin/treks">Treks</router-link>
      <router-link class="nav-link" to="/admin/staff">Staff</router-link>
      <router-link class="nav-link" to="/admin/users">Users</router-link>
      <router-link class="nav-link" to="/admin/bookings">Bookings</router-link>
    </div>
    <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
  </nav>

  <div class="container my-4">
    <div v-if="$route.path === '/admin'" class="row g-3">
      <div class="col-3" v-for="(value, key) in stats" :key="key">
        <div class="card text-center p-3">
          <div class="fs-3">{{ value }}</div>
          <div class="text-muted text-capitalize">{{ key }}</div>
        </div>
      </div>
    </div>
    <router-view v-else />
  </div>
</template>
