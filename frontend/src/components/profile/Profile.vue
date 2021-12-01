<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" sm="6" md="7" lg="7">
        <account />
      </v-col>
      <v-col cols="12" sm="6" md="5" lg="5">
        <password />
        <api />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Account from "./Account.vue";
import Password from "./Password.vue";
import Api from "./API.vue";

export default {
  components: {
    Account,
    Password,
    Api,
  },
  data: () => ({}),
};
</script>

<style>
</style>