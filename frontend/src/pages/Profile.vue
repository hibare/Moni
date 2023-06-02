<template>
  <q-page container class="q-mt-md">
    <q-splitter v-model="splitterModel" style="height: 100vh" :limits="[10, 10]" class="q-pr-md">

      <template v-slot:before>
        <q-tabs vertical class="text-teal">
          <q-route-tab name="account" icon="person" label="Account" class="text-capitalize"
            :to="{ name: 'profile.account' }" exact />
          <q-route-tab name="password" icon="lock" label="Password" class="text-capitalize"
            :to="{ name: 'profile.password' }" exact />
          <q-route-tab name="api" icon="api" label="API" class="text-capitalize" :to="{ name: 'profile.api' }" exact />
        </q-tabs>
      </template>

      <template v-slot:after>
        <div class="q-pa-md bg-white">
          <router-view />
        </div>
      </template>

    </q-splitter>
  </q-page>
</template>
<script setup lang="ts">
import { ref } from 'vue'
const splitterModel = ref<number>(10)

</script>