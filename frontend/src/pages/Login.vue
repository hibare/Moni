<template>
    <q-page container>
        <div class="row">
            <div class="col-12 col-md-4 absolute-center q-px-lg">
                <div class="row q-pb-md justify-center">
                    <q-avatar class="q-mr-sm">
                        <img src="/favicon.png" height="40px" width="50px" />
                    </q-avatar>
                    <span class="brand text-h4">Moni</span>
                </div>
                <q-form @submit.prevent.stop="onSubmit" @reset.prevent.stop="onReset" ref="loginForm"
                    class="q-gutter-md q-pt-xl">
                    <q-input autofocus filled v-model="username" label="Username" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Required']">
                        <template v-slot:prepend>
                            <q-icon name="account_circle" size="sm" />
                        </template></q-input>
                    <q-input filled :type="isPwd ? 'password' : 'text'" v-model="password" label="Password" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Required']">
                        <template v-slot:prepend>
                            <q-icon name="lock" size="sm" />
                        </template>
                        <template v-slot:append>
                            <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer"
                                @click="isPwd = !isPwd" size="sm" />
                        </template>
                    </q-input>
                    <div>
                        <q-btn outline rounded no-caps :loading="getIsLoggingIn" class="full-width q-mt-xs" label="Login"
                            type="submit" color="primary" />
                    </div>
                </q-form>
            </div>
        </div>
    </q-page>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import router from '../router';
import { useAuthStore } from '../store';

const username = ref('')
const password = ref('')
const isPwd = ref(true)
const loginForm = ref(null)

const authStore = useAuthStore()
const { getIsLoggingIn, login, getIsLoggedIn } = authStore

const onSubmit = async () => {
    await login(username.value, password.value)

    if (getIsLoggedIn) {
        if (router.currentRoute.value.query.redirect)
            router.push({ path: router.currentRoute.value.query.redirect.toString() })
        else
            router.push({ name: "jobs" })
    }
}
const onReset = () => { }


</script>
