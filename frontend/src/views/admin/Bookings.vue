<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const bookings = ref([]);

onMounted(async () => {
  bookings.value = await apiFetch("/api/history/bookings");
});
</script>

<template>
  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Trek</th>
        <th>Trekker</th>
        <th>Email</th>
        <th>Booked At</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="b in bookings" :key="b.id">
        <td>{{ b.trek.name }}</td>
        <td>{{ b.user.name }}</td>
        <td>{{ b.user.email }}</td>
        <td>{{ new Date(b.booked_at).toLocaleDateString() }}</td>
        <td>{{ b.status }}</td>
      </tr>
      <tr v-if="!bookings.length">
        <td colspan="5" class="text-center text-muted">No bookings yet.</td>
      </tr>
    </tbody>
  </table>
</template>
