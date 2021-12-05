<template>
  <v-col cols="12" sm="3" lg="3" md="3" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle>Jobs</v-card-subtitle>
      <v-card-text class="justify-center">
        <v-progress-circular
          indeterminate
          v-if="jobsLoading"
        ></v-progress-circular>
        <h3 v-else>
          {{
            Object.prototype.toString.call(notifierJobs) === "[object String]"
              ? notifierJobs
              : notifierJobs.length
          }}
        </h3>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "NotifierJobsCount",
  props: {
    uuid: String,
  },
  data: () => ({
    notifierJobs: [],
    jobsLoading: false,
  }),

  created() {
    this.getNotifierJobs();
  },

  watch: {
    uuid() {
      this.getNotifierJobs();
    },
  },

  methods: {
    getNotifierJobs() {
      this.jobsLoading = true;
      this.$http
        .get(`/api/v1/notifiers/${this.uuid}/jobs/`)
        .then((result) => {
          if (result.status === 200) {
            this.notifierJobs = result.data;
          } else {
            this.notifierJobs = "Failed";
          }
        })
        .catch(() => {
          this.notifierJobs = "Failed";
        })
        .finally(() => {
          this.jobsLoading = false;
        });
    },
  },
};
</script>

<style>
</style>