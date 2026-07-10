<script setup>
import { onMounted, ref } from "vue";
import { apiFetch } from "../../api";

const staff = ref([]);
const showModal = ref(false);
const error = ref("");
const form = ref({ name: "", email: "", password: "" });

async function load() {
  staff.value = await apiFetch("/api/admin/staff");
}
onMounted(load);

function openCreate() {
  form.value = { name: "", email: "", password: "" };
  error.value = "";
  showModal.value = true;
}

async function save() {
  try {
    await apiFetch("/api/admin/staff", { method: "POST", body: JSON.stringify(form.value) });
    showModal.value = false;
    await load();
  } catch (e) {
    error.value = e.message;
  }
}
</script>

<template>
  <div class="d-flex justify-content-end mb-3">
    <button class="btn btn-primary" @click="openCreate">+ New Staff</button>
  </div>

  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="s in staff" :key="s.id">
        <td>{{ s.name }}</td>
        <td>{{ s.email }}</td>
      </tr>
    </tbody>
  </table>

  <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content p-3">
        <h5>New Staff</h5>
        <form @submit.prevent="save">
          <input class="form-control mb-2" v-model="form.name" placeholder="Name" required />
          <input class="form-control mb-2" type="email" v-model="form.email" placeholder="Email" required />
          <input class="form-control mb-2" type="password" v-model="form.password" placeholder="Password" minlength="6" required />
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
