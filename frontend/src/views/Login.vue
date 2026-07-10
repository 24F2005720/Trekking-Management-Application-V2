<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { setAuth } from "../stores/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();

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
  router.push(`/${data.role}`);
}
</script>

<template>
  <form @submit.prevent="submit">
    <h1>Login</h1>
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
    <p v-if="error">{{ error }}</p>
    <router-link to="/register">Need an account? Register</router-link>
  </form>
</template>
