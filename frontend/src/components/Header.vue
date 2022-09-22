<template>
  <div>
    <nav>
      <v-app-bar
        color="background"
        class="px-4"
        app
        fixed
        elevate-on-scroll
        v-if="isLoggedin"
      >
        <v-app-bar-title color="primary" class="font-weight-medium">
          <h3>
            <router-link :to="{ name: 'jobs' }" class="brand"
              ><img src="/favicon.ico" height="25px" width="50px" />
              {{ getAppName() }}</router-link
            >

            <v-icon v-if="jobsStatus.status" small class="mr-1" color="green"
              >mdi-circle-medium</v-icon
            >
            <v-icon v-else small class="mr-1" color="red"
              >mdi-circle-medium</v-icon
            >
          </h3>
        </v-app-bar-title>

        <v-spacer></v-spacer>

        <v-menu transition="scale-transition" bottom left offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              small
              color=""
              v-bind="attrs"
              v-on="on"
              class="text-capitalize"
            >
              <v-icon small>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card class="mx-auto" min-width="120px" max-width="300px" tile>
            <v-list dense flat color="secondary">
              <v-list-item-group color="primary">
                <v-list-item @click="addJobDialog = true">
                  <v-list-item-icon
                    ><v-icon dense>mdi-memory</v-icon></v-list-item-icon
                  >
                  <v-list-item-content>
                    <v-list-item-title>Job</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item @click="addNotifierDialog = true">
                  <v-list-item-icon
                    ><v-icon dense>mdi-bell</v-icon></v-list-item-icon
                  >
                  <v-list-item-content>
                    <v-list-item-title>Notifier</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-menu>

        <v-btn
          text
          plain
          class="d-none d-sm-flex text-capitalize"
          :ripple="false"
          :to="{ name: 'jobs' }"
          ><v-icon small class="mr-1">mdi-memory</v-icon>
          <span>Jobs</span></v-btn
        >
        <v-btn
          text
          plain
          class="d-none d-sm-flex text-capitalize"
          :ripple="false"
          :to="{ name: 'notifiers' }"
          ><v-icon small class="mr-1">mdi-bell</v-icon>
          <span>Notifiers </span></v-btn
        >
        <v-menu transition="scale-transition" bottom left offset-y>
          <template v-slot:activator="{ on, attrs, value }">
            <v-btn
              text
              small
              v-bind="attrs"
              v-on="on"
              class="d-none d-sm-flex text-capitalize no-hvr-btn"
              :ripple="false"
              ><v-btn outlined small fab
                >{{ getFirstname[0] }}{{ getLastname[0] }}</v-btn
              ><v-icon v-if="value" right>mdi-chevron-up</v-icon>
              <v-icon v-else right>mdi-chevron-down</v-icon>
            </v-btn>

            <v-btn
              icon
              color=""
              v-bind="attrs"
              v-on="on"
              class="d-flex d-sm-none text-capitalize"
            >
              <v-icon>mdi-menu</v-icon></v-btn
            >
          </template>
          <v-card class="mx-auto" min-width="120px" max-width="300px" tile>
            <v-list dense color="secondary">
              <v-list-item-group v-model="selectedItem" color="primary">
                <v-list-item link :to="{ name: 'profile' }">
                  <v-list-item-icon>
                    <v-icon dense>mdi-account</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Profile</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  link
                  :to="{ name: 'jobs' }"
                  class="d-flex d-sm-none"
                >
                  <v-list-item-icon>
                    <v-icon dense>mdi-memory</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Jobs</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  link
                  :to="{ name: 'notifiers' }"
                  class="d-flex d-sm-none"
                >
                  <v-list-item-icon>
                    <v-icon dense>mdi-bell</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Notifiers</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link href="/swagger">
                  <v-list-item-icon>
                    <v-icon dense>mdi-api</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>API</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link target="_blank" :href="getGitURL()">
                  <v-list-item-icon>
                    <v-icon dense>mdi-github</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Github</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider></v-divider>
                <v-list-item @click="logout()">
                  <v-list-item-icon>
                    <v-icon dense>mdi-logout</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Logout</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-menu>
      </v-app-bar>
    </nav>
    <job-add-update :jobDialog.sync="addJobDialog" />
    <notifier-add-update :notifierDialog.sync="addNotifierDialog" />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { EventBus } from "@/events/eventBus";
import JobAddUpdate from "./jobs/JobAddUpdate.vue";
import NotifierAddUpdate from "./notifiers/NotifierAddUpdate.vue";

export default {
  name: "Header",

  components: { JobAddUpdate, NotifierAddUpdate },

  data: () => ({
    drawer: false,
    group: null,
    jobsStatus: {
      status: null,
      jobs: null,
    },
    selectedItem: 0,
    currentRouteName: null,
    addJobDialog: false,
    addNotifierDialog: false,
  }),

  watch: {
    group() {
      this.drawer = false;
    },

    jobsStatus(val) {
      if (val.status === false) {
        this.$notification.show(
          "Service Down",
          {
            body: "One / More service(s) down",
          },
          {}
        );
      }
    },

    "$route.name"(val) {
      this.currentRouteName = val;
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
    setInterval(() => this.getJobsStatus(), 300000);
  },

  methods: {
    getJobsStatus() {
      this.$http.get("/api/v1/jobs/status/").then((result) => {
        this.jobsStatus = result.data;

        EventBus.$emit("loadStatusEvent", null);
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

.no-hvr-btn:before {
  display: none;
}
</style>