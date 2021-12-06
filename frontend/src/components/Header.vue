<template>
  <nav>
    <v-app-bar color="background" class="px-4" app fixed elevate-on-scroll>
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        v-if="isLoggedin"
      ></v-app-bar-nav-icon>
      <v-app-bar-title color="primary" class="font-weight-medium">
        <h2>
          <router-link :to="{ name: 'jobs' }" class="brand">{{
            getAppName()
          }}</router-link>

          <v-icon v-if="jobsStatus.status" small class="mr-1" color="green"
            >mdi-circle-medium</v-icon
          >
          <v-icon v-else small class="mr-1" color="red"
            >mdi-circle-medium</v-icon
          >
        </h2>
      </v-app-bar-title>

      <v-spacer></v-spacer>
      <v-btn icon target="_blank" :href="getGitURL()">
        <v-icon>mdi-github</v-icon>
      </v-btn>
      <v-btn icon @click="logout()" v-if="isLoggedin">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Drawer -->
    <v-navigation-drawer
      v-model="drawer"
      app
      temporary
      bottom
      class="background"
    >
      <v-layout column align-center>
        <v-flex class="mt-6 text-center">
          <v-avatar size="60" class="avatar">
            <span class="white--text">{{ getAvatar() }}</span>
          </v-avatar>
          <p class="mt-3">
            <router-link
              :to="{ name: 'profile' }"
              class="white--text subheading text-center text-decoration-none"
              >{{ getFullname() }}</router-link
            >
          </p>
        </v-flex>
      </v-layout>

      <v-divider></v-divider>

      <v-list nav dense class="px-6">
        <v-list-item-group>
          <v-list-item link :to="{ name: 'jobs' }">
            <v-list-item-icon>
              <v-icon> mdi-memory</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Jobs</v-list-item-title>
          </v-list-item>

          <v-list-group :value="true" no-action>
            <template v-slot:activator>
              <v-list-item-icon>
                <v-icon> mdi-bell</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Notifiers</v-list-item-title>
            </template>
            <v-list-item link :to="{ name: 'telegram' }">
              <v-list-item-icon>
                <v-icon> mdi-send-circle</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Telegram</v-list-item-title>
            </v-list-item>
            <v-list-item link :to="{ name: 'slack' }">
              <v-list-item-icon>
                <v-icon> mdi-slack</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Slack</v-list-item-title>
            </v-list-item>
            <v-list-item link :to="{ name: 'discord' }">
              <v-list-item-icon>
                <v-icon> mdi-discord</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Discord</v-list-item-title>
            </v-list-item>
            <v-list-item link :to="{ name: 'gotify' }">
              <v-list-item-icon>
                <v-icon> mdi-message</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Gotify</v-list-item-title>
            </v-list-item>
            <v-list-item link :to="{ name: 'webhook' }">
              <v-list-item-icon>
                <v-icon> mdi-webhook</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Webhook</v-list-item-title>
            </v-list-item>
          </v-list-group>

          <v-list-item link href="/swagger">
            <v-list-item-icon>
              <v-icon> mdi-api</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Swagger</v-list-item-title>
          </v-list-item>
          <v-list-item link :to="{ name: 'profile' }">
            <v-list-item-icon>
              <v-icon> mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Header",

  data: () => ({
    drawer: false,
    group: null,
    jobsStatus: {
      status: null,
      jobs: null,
    },
  }),

  watch: {
    group() {
      this.drawer = false;
    },
  },

  computed: {
    ...mapGetters({
      isLoggedin: "auth/isLoggedin",
      getAccessToken: "auth/getAccessToken",
      getFirstname: "auth/getFirstname",
      getLastname: "auth/getLastname",
      getEmail: "auth/getEmail",
    }),
  },

  created() {
    this.getJobsStatus();
    setTimeout(this.getJobsStatus(), 300000);
  },

  methods: {
    getJobsStatus() {
      this.$http.get("/api/v1/jobs/status/").then((result) => {
        this.jobsStatus = result.data;
      });
    },

    logout() {
      this.$store.dispatch("auth/logout");
      this.$router.replace({ name: "login" });
    },

    getFullname() {
      var firstname = this.getFirstname || "-";
      var lastname = this.getLastname || "-";
      return firstname + " " + lastname;
    },

    getAvatar() {
      if (this.getFirstname && this.getLastname) {
        return this.getFirstname[0] + this.getLastname[0];
      } else {
        return "?";
      }
    },
  },
};
</script>
<style scoped>
.brand {
  text-decoration: none;
  color: inherit;
}

.avatar {
  border: 1px solid #ffffff;
}

.v-list-item .v-list-item__icon {
  margin-right: 12px !important;
}

.v-application--is-ltr
  .v-list--dense.v-list--nav
  .v-list-group--no-action
  > .v-list-group__items
  > .v-list-item {
  padding-left: 40px;
}
</style>