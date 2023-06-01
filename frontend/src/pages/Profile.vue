<template>
    <q-page container class="q-mt-md">
    <q-splitter
      v-model="splitterModel"
      style="height: 100vh"
      :limits="[10,10]"
      class="q-pr-md"
    >

      <template v-slot:before>
        <q-tabs
          v-model="tab"
          vertical
          class="text-teal"
        >
          <q-tab name="account" icon="person" label="Account" class="text-capitalize" />
          <q-tab name="password" icon="lock" label="Password" class="text-capitalize" />
          <q-tab name="api" icon="api" label="API" class="text-capitalize" />
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab"
          animated
          swipeable
          vertical
    
          transition-prev="fade"
          transition-next="fade"
        >
          <q-tab-panel name="account">
            <Account/>
          </q-tab-panel>

          <q-tab-panel name="password">
            <Password/>
          </q-tab-panel>

          <q-tab-panel name="api">
           <API/>
          </q-tab-panel>
        </q-tab-panels>
      </template>

    </q-splitter>
    </q-page>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import Account from '../components/profile/Account.vue';
import API from '../components/profile/API.vue';
import Password from '../components/profile/Password.vue';

const tab = ref<string>('account')
const splitterModel = ref<number>(10)

</script>