<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiFetch } from "../../api";

const route = useRoute();
const router = useRouter();
const trekId = route.params.id;

const trek = ref(null);
const participants = ref([]);
const error = ref("");

async function load() {
  const treks = await apiFetch("/api/staff/treks");
  trek.value = treks.find((t) => t.id == trekId);
  participants.value = await apiFetch(`/api/staff/treks/${trekId}/participants`);
}
onMounted(load);

async function saveSlots() {
  try {
    await apiFetch(`/api/staff/treks/${trekId}`, { method: "PUT", body: JSON.stringify({ slots: trek.value.slots }) });
    await load();
  } catch (e) {
    error.value = e.message;
  }
}

async function setStatus(status) {
  await apiFetch(`/api/staff/treks/${trekId}/status`, { method: "PATCH", body: JSON.stringify({ status }) });
  await load();
}

async function cancelTrek() {
  if (!confirm(`Cancel trek "${trek.value.name}"? This cannot be undone.`)) return;
  await setStatus("Closed");
}
</script>

<template>
  <button class="btn btn-link px-0" @click="router.push('/staff')">&larr; Back to My Treks</button>

  <div v-if="trek" class="card p-3 my-3">
    <h4>{{ trek.name }} - {{ trek.location }}</h4>
    <p>Status: <strong>{{ trek.status }}</strong></p>

    <div class="d-flex align-items-center gap-2 mb-3">
      <label>Slots:</label>
      <input type="number" class="form-control w-auto" min="0" required v-model.number="trek.slots" />
      <button class="btn btn-sm btn-secondary" @click="saveSlots">Save</button>
    </div>
    <p v-if="error" class="text-danger">{{ error }}</p>

    <div class="mb-3">
      <button class="btn btn-sm btn-warning me-2" :disabled="trek.status !== 'Open'" @click="setStatus('Started')">
        Mark Started
      </button>
      <button class="btn btn-sm btn-success me-2" :disabled="trek.status !== 'Started'" @click="setStatus('Completed')">
        Mark Completed
      </button>
      <button
        class="btn btn-sm btn-outline-danger"
        :disabled="!['Open', 'Started'].includes(trek.status)"
        @click="cancelTrek"
      >
        Cancel Trek
      </button>
    </div>

    <h5>Participants</h5>
    <ul class="list-group">
      <li class="list-group-item" v-for="p in participants" :key="p.id">{{ p.name }} - {{ p.email }}</li>
      <li class="list-group-item text-muted" v-if="!participants.length">No bookings yet.</li>
    </ul>
  </div>
</template>
