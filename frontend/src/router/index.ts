import { nextTick } from "vue";
import {
  createRouter,
  createWebHashHistory,
  RouteRecordRaw,
  Router,
} from "vue-router";
import { useAuthStore } from "../store";
import Login from "../pages/Login.vue";
import Logout from "../pages/Logout.vue";
import Jobs from "../pages/jobs/Jobs.vue";
import JobDetails from "../pages/jobs/JobDetails.vue";
import Notifiers from "../pages/notifiers/Notifiers.vue";
import NotifierDetails from "../pages/notifiers/NotifierDetails.vue";
import { AppName } from "../constants";

const routes: Readonly<RouteRecordRaw[]> = [
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      title: "Login",
    },
  },
  {
    path: "/logout",
    name: "logout",
    component: Logout,
    meta: {
      title: "Logout",
    },
  },
  {
    path: "/",
    name: "root",
    redirect: "/jobs",
    meta: {
      title: "Home",
    },
  },
  {
    path: "/jobs",
    name: "jobs",
    component: Jobs,
    meta: { title: "Jobs" },
  },
  {
    path: "/jobs/:uuid",
    name: "jobDetails",
    component: JobDetails,
    meta: { title: "Job" },
  },
  {
    path: "/notifiers/",
    name: "notifiers",
    component: Notifiers,
    meta: { title: "Notifiers" },
  },
  {
    path: "/notifiers/:uuid",
    name: "notifierDetails",
    component: NotifierDetails,
    meta: { title: "Notifier" },
  },
];

const router: Router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
});

router.beforeEach(async (to, from, next) => {
  const store = useAuthStore();
  await store.validateSession();

  if (!store.isLoggedIn && to.name !== "login") {
    next({ name: "login", query: { redirect: to.fullPath } });
  } else if (store.isLoggedIn && to.name === "login") {
    if (to.query.redirect) {
      next({ path: to.query.redirect.toString() });
    } else {
      next({ name: "jobs" });
    }
  } else next();
});

router.afterEach((to) => {
  const { title } = to.meta || {};
  const appName = AppName;

  if (title) {
    nextTick(() => {
      document.title = `${title} | ${appName}`;
    });
  }
});

export default router;
