<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const treks = ref([]);
const q = ref("");
const editing = ref(null);
const showModal = ref(false);
const staffList = ref([]);
const error = ref("");

const empty = () => ({ name: "", location: "", difficulty: "Easy", duration_days: 1, price: 0, slots: 1 });
const form = ref(empty());

async function load() {
  treks.value = await apiFetch(`/api/admin/treks${q.value ? `?q=${encodeURIComponent(q.value)}` : ""}`);
}

onMounted(async () => {
  await load();
  staffList.value = await apiFetch("/api/admin/staff");
});

function openCreate() {
  editing.value = null;
  form.value = empty();
  error.value = "";
  showModal.value = true;
}

function openEdit(trek) {
  editing.value = trek;
  form.value = { ...trek };
  error.value = "";
  showModal.value = true;
}

async function save() {
  try {
    if (editing.value) {
      await apiFetch(`/api/admin/treks/${editing.value.id}`, { method: "PUT", body: JSON.stringify(form.value) });
    } else {
      await apiFetch("/api/admin/treks", { method: "POST", body: JSON.stringify(form.value) });
    }
    showModal.value = false;
    await load();
  } catch (e) {
    error.value = e.message;
  }
}

async function remove(trek) {
  if (!confirm(`Delete trek "${trek.name}"?`)) return;
  await apiFetch(`/api/admin/treks/${trek.id}`, { method: "DELETE" });
  await load();
}

async function assign(trek, event) {
  const staff_id = event.target.value || null;
  await apiFetch(`/api/admin/treks/${trek.id}/assign`, { method: "PATCH", body: JSON.stringify({ staff_id }) });
  await load();
}
</script>

<template>
  <div class="d-flex justify-content-between mb-3">
    <input v-model="q" @keyup.enter="load" class="form-control w-auto" placeholder="Search by name/location" />
    <button class="btn btn-primary" @click="openCreate">+ New Trek</button>
  </div>

  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Name</th>
        <th>Location</th>
        <th>Difficulty</th>
        <th>Days</th>
        <th>Price</th>
        <th>Slots</th>
        <th>Status</th>
        <th>Staff</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="t in treks" :key="t.id">
        <td>{{ t.name }}</td>
        <td>{{ t.location }}</td>
        <td>{{ t.difficulty }}</td>
        <td>{{ t.duration_days }}</td>
        <td>{{ t.price }}</td>
        <td>{{ t.slots }}</td>
        <td>{{ t.status }}</td>
        <td>
          <select class="form-select form-select-sm" :value="t.staff_id ?? ''" @change="assign(t, $event)">
            <option value="">Unassigned</option>
            <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </td>
        <td>
          <button class="btn btn-sm btn-secondary me-1" @click="openEdit(t)">Edit</button>
          <button class="btn btn-sm btn-danger" @click="remove(t)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>

  <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content p-3">
        <h5>{{ editing ? "Edit Trek" : "New Trek" }}</h5>
        <form @submit.prevent="save">
          <input class="form-control mb-2" v-model="form.name" placeholder="Name" required />
          <input class="form-control mb-2" v-model="form.location" placeholder="Location" required />
          <select class="form-select mb-2" v-model="form.difficulty">
            <option>Easy</option>
            <option>Moderate</option>
            <option>Hard</option>
          </select>
          <input class="form-control mb-2" type="number" min="1" v-model.number="form.duration_days" placeholder="Duration (days)" required />
          <input class="form-control mb-2" type="number" min="0" step="0.01" v-model.number="form.price" placeholder="Price" required />
          <input class="form-control mb-2" type="number" min="0" v-model.number="form.slots" placeholder="Slots" required />
          <p v-if="error" class="text-danger">{{ error }}</p>
          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button type="submit" class="btn btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
