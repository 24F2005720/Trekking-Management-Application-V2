<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const treks = ref([]);
const difficulty = ref("");
const location = ref("");
const duration = ref("");
const message = ref("");

async function load() {
  const params = new URLSearchParams();
  if (difficulty.value) params.set("difficulty", difficulty.value);
  if (location.value) params.set("location", location.value);
  if (duration.value) params.set("duration", duration.value);
  treks.value = await apiFetch(`/api/user/treks?${params}`);
}
onMounted(load);

async function book(trek) {
  message.value = "";
  try {
    await apiFetch(`/api/user/treks/${trek.id}/book`, { method: "POST" });
    message.value = `Booked "${trek.name}"!`;
    await load();
  } catch (e) {
    message.value = e.message;
  }
}
</script>

<template>
  <div class="d-flex gap-2 mb-3">
    <select class="form-select w-auto" v-model="difficulty" @change="load">
      <option value="">All difficulties</option>
      <option>Easy</option>
      <option>Moderate</option>
      <option>Hard</option>
    </select>
    <input class="form-control w-auto" v-model="location" @keyup.enter="load" placeholder="Location" />
    <input class="form-control w-auto" type="number" v-model="duration" @keyup.enter="load" placeholder="Duration (days)" />
    <button class="btn btn-secondary" @click="load">Filter</button>
  </div>

  <p v-if="message">{{ message }}</p>

  <div class="row g-3">
    <div class="col-4" v-for="t in treks" :key="t.id">
      <div class="card p-3">
        <h5>{{ t.name }}</h5>
        <p class="mb-1">{{ t.location }} - {{ t.difficulty }} - {{ t.duration_days }} days</p>
        <p class="mb-1">₹{{ t.price }} | {{ t.slots }} slots left</p>
        <button class="btn btn-primary" :disabled="t.slots <= 0" @click="book(t)">
          {{ t.slots > 0 ? "Book" : "Sold out" }}
        </button>
      </div>
    </div>
    <p v-if="!treks.length" class="text-muted">No treks match your filters.</p>
  </div>
</template>
