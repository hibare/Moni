<template>
    <q-page container>
        <div class="row">
            <div class="col-12 col-md-4 absolute-center">
                <div class="row q-pb-md justify-center">
                    <q-avatar class="q-mr-sm">
                        <img src="/favicon.png" height="40px" width="50px" />
                    </q-avatar>
                    <span class="brand text-h4">Moni</span>


                </div>
                <div class="row q-pb-md justify-center text-center">
                    <div> You have been logged out
                        successfully.</div>
                    <div class="text-caption col-12">Redirecting to login in {{ counter }} seconds</div>
                    <div class="col-12"><q-btn outline dense size="md" class="q-px-md q-mt-md text-capitalize"
                            @click="navigateToLogin">Login
                            again</q-btn></div>
                </div>
            </div>
        </div>
    </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import router from '../router';
import { useAuthStore } from '../store';
import { useResetStore } from '../store/pinia';

const counter = ref<number>(10)
const authStore = useAuthStore()
const { logout } = authStore

const redirectCounter = () => {
    if (counter.value > 0) {
        setTimeout(() => {
            counter.value = counter.value - 1
            redirectCounter()
        }, 1000)
    } else {
        navigateToLogin()
    }
}

onMounted(() => {
    useResetStore().all()
    logout()
    redirectCounter()
})

const navigateToLogin = () => {
    router.push({ name: "login" })
}

</script>
