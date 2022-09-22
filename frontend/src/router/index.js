import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '@/store'
import Login from "@/components/Login.vue";
import JobsDashboard from "@/components/jobs/Jobs.vue";
import JobDetails from "@/components/jobs/JobDetails.vue";
import Notifiers from "@/components/notifiers/Notifiers.vue";
import NotifierDetails from "@/components/notifiers/NotifierDetails.vue";
import Profile from "@/components/profile/Profile.vue";
import Error404 from "@/components/Error404.vue";

Vue.use(VueRouter)

const routes = [
    { path: '/', name: 'root', redirect: '/jobs', meta: { title: 'Home' } },
    { path: '/jobs', name: 'jobs', component: JobsDashboard, meta: { title: 'Jobs' } },
    { path: '/jobs/:uuid', name: 'jobDetails', component: JobDetails, meta: { title: 'Job' } },
    { path: '/login', name: 'login', component: Login, meta: { title: 'Login' } },
    { path: '/notifiers', name: 'notifiers', component: Notifiers, meta: { title: 'Notifiers' } },
    { path: '/notifiers/:uuid', name: 'notifierDetails', component: NotifierDetails, meta: { title: 'Notifier' } },
    { path: '/profile', name: 'profile', component: Profile, meta: { title: 'Profile' } },
    { path: '*', name: 'error404', component: Error404, meta: { title: '404' } }
]

const router = new VueRouter({
    routes
})

router.beforeEach((to, from, next) => {
    if (to.name !== "login" && !store.state.auth.isLoggedin) next({ name: 'login' })
    else next();
})

export default router
