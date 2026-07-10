<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const success = ref(false);
const router = useRouter();

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
  <form @submit.prevent="submit">
    <h1>Register</h1>
    <input v-model="name" placeholder="Name" required />
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Password" required minlength="6" />
    <button type="submit">Register</button>
    <p v-if="error">{{ error }}</p>
    <p v-if="success">Registered! Redirecting to login...</p>
    <router-link to="/login">Already have an account? Login</router-link>
  </form>
</template>
