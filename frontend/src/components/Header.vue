<template>
    <q-header reveal elevated class="transparent text-black">
        <q-toolbar class="q-pr-lg">
            <q-btn flat @click="drawer = !drawer" round dense icon="menu" class="mobile-only" />

            <q-toolbar-title class="brand">
                <q-avatar size="md">
                    <img src="/favicon.png" />
                </q-avatar>
                Moni</q-toolbar-title>

            <q-space></q-space>

            <q-btn round outline dense color="pink-6" class="q-pt-xs">
                <span class="text-caption">{{ getBadge }}</span>
                <q-menu transition-show="scale" transition-hide="scale" anchor="bottom left">
                    <q-list style="min-width: 100px">
                        <q-item clickable :to="{ name: 'profile.account' }">
                            <q-item-section>Profile</q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>

        </q-toolbar>
    </q-header>

    <q-drawer v-model="drawer" show-if-above :mini="miniState" @mouseover="miniState = false" @mouseout="miniState = true"
        mini-to-overlay :width="200" :breakpoint="500" bordered class="transparent">
        <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: '0' }">
            <q-list padding>
                <q-item clickable v-ripple :to="{ name: 'jobs' }">
                    <q-item-section avatar>
                        <q-icon name="memory" />
                    </q-item-section>

                    <q-item-section>
                        Jobs
                    </q-item-section>
                </q-item>

                <q-item clickable v-ripple :to="{ name: 'notifiers' }">
                    <q-item-section avatar>
                        <q-icon name="notifications" />
                    </q-item-section>

                    <q-item-section>
                        Notifiers
                    </q-item-section>
                </q-item>

                <q-item clickable v-ripple>
                    <q-item-section avatar>
                        <q-icon name="lock" />
                    </q-item-section>

                    <q-item-section>
                        Secrets
                    </q-item-section>
                </q-item>

                <span class="fixed-bottom">
                    <q-separator />
                    <q-item clickable v-ripple :to="{ name: 'profile.account' }">
                        <q-item-section avatar>
                            <q-icon name="person" />
                        </q-item-section>

                        <q-item-section>
                            Profile
                        </q-item-section>
                    </q-item>
                    <q-item clickable v-ripple target="_blank" :href=AppGithub>
                        <q-item-section avatar>
                            <q-icon name="fa-brands fa-github" />
                        </q-item-section>

                        <q-item-section>
                            Github
                        </q-item-section>
                    </q-item>
                    <q-item clickable v-ripple :to="{ name: 'logout' }">
                        <q-item-section avatar>
                            <q-icon name="logout" />
                        </q-item-section>

                        <q-item-section>
                            Logout
                        </q-item-section>
                    </q-item>
                </span>

            </q-list>
        </q-scroll-area>
    </q-drawer>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useAuthStore } from '../store';
import { AppGithub } from '../constants';

const drawer = ref<boolean>(false)
const miniState = ref<boolean>(true)

const authStore = useAuthStore()

const getBadge = computed((): string => {
    if (authStore.getFirstName.value && authStore.getLastName.value) {
        return `${authStore.getFirstName.value[0]}${authStore.getLastName.value[0]}`
    }
    return 'NA'
})
</script>
