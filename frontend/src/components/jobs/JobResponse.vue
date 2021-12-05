<template>
  <v-col cols="12" sm="3" lg="3" md="3" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle
        ><v-icon small>mdi-clock-outline</v-icon> Response Time</v-card-subtitle
      >
      <v-card-text class="justify-center">
        <v-progress-circular
          indeterminate
          color="primary"
          v-if="responseLoading"
        ></v-progress-circular>
        <h3>{{ jobResponse }}</h3>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "JobUptime",
  props: {
    uuid: String,
  },

  data: () => ({
    jobResponse: null,
    responseLoading: false,
  }),

  created() {
    this.getJobResponse();
  },

  watch: {
    uuid() {
      this.getJobResponse();
    },
  },

  methods: {
    getJobResponse() {
      this.responseLoading = true;
      this.$http
        .get(`/api/v1/jobs/${this.uuid}/response/`)
        .then((result) => {
          if (result.status === 200) {
            this.jobResponse = result.data.response;
          } else {
            this.jobResponse = "Failed";
          }
        })
        .catch(() => {
          this.jobResponse = "Failed";
        })
        .finally(() => {
          this.responseLoading = false;
        });
    },
  },
};
</script>

<style>
</style>