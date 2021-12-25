<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" lg="7" md="12" class="" align="center">
        left
      </v-col>
      <v-col cols="12" sm="12" lg="5" md="12" align="center" justify="center">
        <v-col sm="9" lg="9" md="9">
          <v-form
            ref="loginForm"
            @submit.prevent="login"
            v-model="loginFormValid"
            lazy-validation
          >
            <h2>Jump-in</h2>
            <v-text-field
              v-model="username"
              :rules="nameRules"
              label="Username"
              required
              autofocus
            ></v-text-field>

            <v-text-field
              v-model="password"
              :rules="emptyRule"
              label="Password"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
              required
            ></v-text-field>

            <v-btn
              class="mt-4 text-capitalize"
              block
              rounded
              outlined
              depressed
              type="submit"
              color="primary"
              :loading="loginLoader"
              :disabled="!loginFormValid"
            >
              Jump
            </v-btn>
          </v-form>
        </v-col>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import rulesMixin from "@/mixins/rulesMixin";
import { EventBus } from "@/helpers/eventBus";

export default {
  mixins: [rulesMixin],

  data: () => ({
    loginFormValid: true,
    username: "",
    password: "",
    showPassword: false,
    loginLoader: false,
  }),

  methods: {
    login() {
      if (this.$refs.loginForm.validate()) {
        this.loginLoader = true;
        this.$http
          .post("/api/v1/accounts/jwt/", {
            username: this.username,
            password: this.password,
          })
          .then((response) => {
            if (response.status === 200) {
              this.$store.dispatch("auth/login", response.data);
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Logged in",
              });
              this.reset();
              this.resetValidation();
              this.$router.push("jobs");
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
      this.loginLoader = false;
    },
    reset() {
      this.$refs.loginForm.reset();
    },
    resetValidation() {
      this.$refs.loginForm.resetValidation();
    },
  },
};
</script>