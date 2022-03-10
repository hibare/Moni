<template>
  <v-row>
    <v-col cols="12">
      <v-card elevation="1" color="transparent">
        <v-card-title>
          <h5><v-icon>mdi-lock</v-icon> Password</h5>
        </v-card-title>
        <v-card-text>
          <v-form ref="password" lazy-validation class="px-5 mt-4">
            <v-text-field
              v-model="password.old_password"
              label="Current Password"
              :rules="emptyRule"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>

            <v-text-field
              v-model="password.new_password"
              label="New Password"
              :rules="emptyRule"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>

            <v-text-field
              v-model="password.new_password_confirm"
              label="Confirm New Password"
              :rules="emptyRule"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>

            <v-btn
              :disabled="updateLoader"
              :loading="updateLoader"
              color="success"
              class="mr-4 text-capitalize"
              @click="updatePassword"
            >
              Update
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import rulesMixin from "@/mixins/rulesMixin";
import { EventBus } from "@/events/eventBus";

export default {
  name: "Password",
  mixins: [rulesMixin],

  data: () => ({
    updateLoader: false,

    showPassword: false,
    password: {
      old_password: "",
      new_password: "",
      new_password_confirm: "",
    },
  }),

  methods: {
    updatePassword() {
      if (this.$refs.password.validate()) {
        this.updateLoader = true;
        this.$http
          .put(`/api/v1/accounts/password/`, this.password)
          .then((result) => {
            if (result.status === 200) {
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Password Changed",
              });
              this.password = {
                old_password: "",
                new_password: "",
                new_password_confirm: "",
              };
            }
          })
          .catch((err) => {
            if (err.response.status === 400) {
              for (let v of Object.values(err.response.data)) {
                EventBus.$emit("showSnackbar", {
                  status: "failure",
                  message: v.join(", "),
                });
              }
            }
          })
          .finally(() => {
            this.updateLoader = false;
            this.$refs.password.resetValidation();
          });
      }
    },
  },
};
</script>

<style>
</style>