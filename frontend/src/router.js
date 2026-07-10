import { createRouter, createWebHistory } from "vue-router";
import { auth } from "./stores/auth";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import AdminDashboard from "./views/admin/Dashboard.vue";
import AdminTreks from "./views/admin/Treks.vue";
import AdminStaff from "./views/admin/Staff.vue";
import AdminUsers from "./views/admin/Users.vue";
import StaffDashboard from "./views/staff/Dashboard.vue";
import StaffTrekManage from "./views/staff/TrekManage.vue";
import UserDashboard from "./views/user/Dashboard.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/admin",
    component: AdminDashboard,
    meta: { role: "admin" },
    children: [
      { path: "treks", component: AdminTreks },
      { path: "staff", component: AdminStaff },
      { path: "users", component: AdminUsers },
    ],
  },
  {
    path: "/staff",
    component: StaffDashboard,
    meta: { role: "staff" },
    children: [{ path: "treks/:id", component: StaffTrekManage }],
  },
  { path: "/user", component: UserDashboard, meta: { role: "trekker" } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  if (to.meta.role && !auth.token) return "/login";
  if (to.meta.role && auth.role !== to.meta.role) return `/${auth.role}`;
});

export default router;
