<template>
  <q-layout view="hHh Lpr lff">
    <q-inner-loading showing v-if="getIsVerifyingToken">
      <q-spinner-puff size="50px" color="primary" />
    </q-inner-loading>

    <template v-else>
      <Header v-if="getIsLoggedIn" />

      <q-page-container>
        <router-view />
      </q-page-container>
    </template>
  </q-layout>
</template>

<script setup lang="ts">
import Header from './components/Header.vue'
import { useAuthStore } from './store'

const authStore = useAuthStore()
const { getIsVerifyingToken, getIsLoggedIn } = authStore

</script>

<style>
body {
  background-color: rgb(241, 242, 244);
}
</style>

