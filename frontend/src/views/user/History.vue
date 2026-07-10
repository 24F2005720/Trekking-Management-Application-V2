<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const bookings = ref([]);

async function load() {
  bookings.value = await apiFetch("/api/history/bookings");
}
onMounted(load);

async function cancel(b) {
  if (!confirm(`Cancel booking for "${b.trek.name}"?`)) return;
  await apiFetch(`/api/history/bookings/${b.id}/cancel`, { method: "POST" });
  await load();
}
</script>

<template>
  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Trek</th>
        <th>Location</th>
        <th>Booked At</th>
        <th>Status</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="b in bookings" :key="b.id">
        <td>{{ b.trek.name }}</td>
        <td>{{ b.trek.location }}</td>
        <td>{{ new Date(b.booked_at).toLocaleDateString() }}</td>
        <td>{{ b.status }}</td>
        <td>
          <button v-if="b.status === 'Booked'" class="btn btn-sm btn-danger" @click="cancel(b)">Cancel</button>
        </td>
      </tr>
      <tr v-if="!bookings.length">
        <td colspan="5" class="text-center text-muted">No bookings yet.</td>
      </tr>
    </tbody>
  </table>
</template>
