<template>
  <q-page container class="q-mt-md ">

    <q-tabs :vertical="false" class="text-teal">
      <q-route-tab name="account" icon="person" label="Account" class="text-capitalize" :to="{ name: 'profile.account' }"
        exact />
      <q-route-tab name="password" icon="lock" label="Password" class="text-capitalize" :to="{ name: 'profile.password' }"
        exact />
      <q-route-tab name="api" icon="api" label="API" class="text-capitalize" :to="{ name: 'profile.api' }" exact />
    </q-tabs>


    <div class="row justify-center items-center bg-white">
      <div class="row justify-center q-px-lg q-py-md">
        <router-view />
      </div>
    </div>


  </q-page>
</template>
<script setup lang="ts"></script>