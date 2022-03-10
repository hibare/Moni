<template>
  <v-row>
    <v-col cols="12">
      <v-card elevation="1" color="transparent">
        <v-card-title>
          <h5><v-icon>mdi-account-circle</v-icon> Account</h5>
        </v-card-title>
        <v-card-text>
          <loader v-if="accountsLoader" />
          <div v-else>
            <v-form ref="account" lazy-validation class="px-5 mt-4">
              <v-text-field
                v-model="account.first_name"
                :counter="10"
                :rules="nameRules"
                label="Firstname"
              ></v-text-field>

              <v-text-field
                v-model="account.last_name"
                :counter="10"
                :rules="nameRules"
                label="Lastname"
              ></v-text-field>

              <v-text-field
                v-model="account.email"
                :rules="emailRules"
                label="E-mail"
                required
              ></v-text-field>

              <v-btn
                :disabled="updateLoader"
                :loading="updateLoader"
                color="success"
                class="mr-4 text-capitalize"
                @click="updateAccount"
              >
                Update
              </v-btn>
            </v-form>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import Loader from "../Loader.vue";
import rulesMixin from "@/mixins/rulesMixin";
import { EventBus } from "@/events/eventBus";

export default {
  components: { Loader },
  name: "Account",
  mixins: [rulesMixin],

  data: () => ({
    accountsLoader: false,
    updateLoader: false,
    account: {
      first_name: "",
      last_name: "",
      email: "",
    },
  }),

  created() {
    this.getAccount();
  },

  methods: {
    getAccount() {
      this.accountsLoader = true;
      this.$http
        .get(`/api/v1/accounts/`)
        .then((result) => {
          if (result.status === 200) {
            this.account = result.data;
          }
        })
        .catch(() => {})
        .finally(() => {
          this.accountsLoader = false;
        });
    },

    updateAccount() {
      if (this.$refs.account.validate()) {
        this.accountsLoader = true;
        this.$http
          .patch(`/api/v1/accounts/`, this.account)
          .then((result) => {
            if (result.status === 200) {
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Updated",
              });
              this.account = result.data;
            }
          })
          .finally(() => {
            this.accountsLoader = false;
            this.$refs.account.resetValidation();
          });
      }
    },
  },
};
</script>

<style>
</style>