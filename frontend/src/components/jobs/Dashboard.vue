<template>
  <v-container fluid>
    <v-row v-if="!jobLoader" align="center" justify="center" dense class="">
      <v-col cols="12" sm="12" md="12" lg="12">
        <job-add @jobAddedEvent="jobAddedEventHandler" />
      </v-col>
      <v-col
        cols="12"
        sm="4"
        md="3"
        lg="3"
        class="ma-1 mt-md-8"
        v-for="item in jobs"
        :key="item.uuid"
      >
        <v-hover v-slot="{ hover }">
          <v-card
            :elevation="hover ? 5 : 1"
            :class="{ 'on-hover': hover }"
            outlined
            color="secondary"
            :to="{ name: 'jobDetails', params: { uuid: item.uuid } }"
            class="mx-6 ma-sm-0 ma-lg-0"
          >
            <v-card-title>
              <v-icon class="mr-2" v-if="item.favicon_url === null"
                >mdi-web</v-icon
              >
              <img
                v-else
                :src="item.favicon_url"
                alt=""
                height="24"
                width="24"
                class="mr-2"
              />{{ item.title }}
              <v-spacer></v-spacer>
              <v-icon
                small
                class="mr-1"
                color="blue-grey lighten-2"
                v-if="!item.state"
                >mdi-circle-medium</v-icon
              >
              <v-icon small class="mr-1" color="green" v-else-if="item.healthy"
                >mdi-circle-medium</v-icon
              >
              <v-icon small class="mr-1" color="red" v-else
                >mdi-circle-medium</v-icon
              >
            </v-card-title>
            <v-card-text>{{ item.url }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>

    <loader v-else />
  </v-container>
</template>

<script>
import Loader from "../Loader.vue";
import JobAdd from "./JobAdd.vue";
export default {
  components: { JobAdd, Loader },
  name: "JobsDashboard",

  data: () => ({
    items: [1, 2, 3, 4, 5, 6, 7],
    jobs: [],
    jobLoader: false,
  }),

  created() {
    this.getJobs();
  },

  methods: {
    getJobs() {
      this.jobLoader = true;
      this.$http
        .get("/api/v1/jobs/")
        .then((result) => {
          this.jobs = result.data;
          console.log(this.jobs);
        })
        .finally(() => {
          this.jobLoader = false;
        });
    },

    jobAddedEventHandler(data) {
      this.jobs.push(data);
    },
  },
};
</script>
<style scoped>
.on-hover {
  cursor: pointer;
}
</style>
