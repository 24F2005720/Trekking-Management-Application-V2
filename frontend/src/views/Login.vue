<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { roleHome } from "../router.js";
import { setAuth } from "../stores/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const validated = ref(false);
const router = useRouter();

async function onSubmit(e) {
  validated.value = true;
  if (!e.target.checkValidity()) return;
  await submit();
}

async function submit() {
  error.value = "";
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email.value, password: password.value }),
  });
  const data = await res.json();
  if (!res.ok) {
    error.value = data.error || "Login failed";
    return;
  }
  setAuth(data);
  router.push(roleHome[data.role]);
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <form novalidate :class="{ 'was-validated': validated }" class="card p-4 shadow-sm" style="width: 22rem" @submit.prevent="onSubmit">
      <h1 class="h4 mb-3 text-center">Login</h1>
      <div class="mb-2">
        <input class="form-control" v-model="email" type="email" placeholder="Email" required />
        <div class="invalid-feedback">Enter a valid email.</div>
      </div>
      <div class="mb-2">
        <input class="form-control" v-model="password" type="password" placeholder="Password" required />
        <div class="invalid-feedback">Password is required.</div>
      </div>
      <button class="btn btn-primary w-100" type="submit">Login</button>
      <p v-if="error" class="text-danger mt-2 mb-0">{{ error }}</p>
      <router-link class="d-block text-center mt-3" to="/register">Need an account? Register</router-link>
    </form>
  </div>
</template>
