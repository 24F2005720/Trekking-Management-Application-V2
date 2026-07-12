<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiFetch } from "../../api";
import { auth, clearAuth } from "../../stores/auth";

const treks = ref([]);
const route = useRoute();
const router = useRouter();

async function load() {
  treks.value = await apiFetch("/api/staff/treks");
}
onMounted(load);

function logout() {
  clearAuth();
  router.push("/login");
}
</script>

<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
    <span class="navbar-brand">Staff - {{ auth.name }}</span>
    <router-link class="nav-link me-auto" to="/staff">My Treks</router-link>
    <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
  </nav>

  <div class="container my-4">
    <table v-if="route.path === '/staff'" class="table table-bordered">
      <thead>
        <tr>
          <th>Name</th>
          <th>Location</th>
          <th>Slots</th>
          <th>Registered</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in treks" :key="t.id">
          <td>{{ t.name }}</td>
          <td>{{ t.location }}</td>
          <td>{{ t.slots }}</td>
          <td>{{ t.participant_count }}</td>
          <td>{{ t.status }}</td>
          <td>
            <router-link class="btn btn-sm btn-primary" :to="`/staff/treks/${t.id}`">Manage</router-link>
          </td>
        </tr>
        <tr v-if="!treks.length">
          <td colspan="6" class="text-center text-muted">No treks assigned yet.</td>
        </tr>
      </tbody>
    </table>
    <router-view v-else />
  </div>
</template>
