<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const success = ref(false);
const validated = ref(false);
const router = useRouter();

async function onSubmit(e) {
  validated.value = true;
  if (!e.target.checkValidity()) return;
  await submit();
}

async function submit() {
  error.value = "";
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name.value, email: email.value, password: password.value }),
  });
  const data = await res.json();
  if (!res.ok) {
    error.value = data.error || "Registration failed";
    return;
  }
  success.value = true;
  setTimeout(() => router.push("/login"), 1000);
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <form novalidate :class="{ 'was-validated': validated }" class="card p-4 shadow-sm" style="width: 22rem" @submit.prevent="onSubmit">
      <h1 class="h4 mb-3 text-center">Register</h1>
      <div class="mb-2">
        <input class="form-control" v-model="name" placeholder="Name" required />
        <div class="invalid-feedback">Name is required.</div>
      </div>
      <div class="mb-2">
        <input class="form-control" v-model="email" type="email" placeholder="Email" required />
        <div class="invalid-feedback">Enter a valid email.</div>
      </div>
      <div class="mb-2">
        <input
          class="form-control"
          v-model="password"
          type="password"
          placeholder="Password"
          required
          minlength="6"
        />
        <div class="invalid-feedback">Password must be at least 6 characters.</div>
      </div>
      <button class="btn btn-primary w-100" type="submit">Register</button>
      <p v-if="error" class="text-danger mt-2 mb-0">{{ error }}</p>
      <p v-if="success" class="text-success mt-2 mb-0">Registered! Redirecting to login...</p>
      <router-link class="d-block text-center mt-3" to="/login">Already have an account? Login</router-link>
    </form>
  </div>
</template>
