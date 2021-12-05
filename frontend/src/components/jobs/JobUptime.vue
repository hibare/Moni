<template>
  <v-col cols="12" sm="3" lg="3" md="3" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle
        ><v-icon small>mdi-heart-pulse</v-icon> Uptime</v-card-subtitle
      >
      <v-card-text class="justify-center">
        <v-progress-circular
          indeterminate
          color="primary"
          v-if="uptimeLoading"
        ></v-progress-circular>
        <h3>{{ jobUptime }}</h3>
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
    jobUptime: null,
    uptimeLoading: false,
  }),

  created() {
    this.getJobUptime();
  },

  watch: {
    uuid() {
      this.getJobUptime();
    },
  },

  methods: {
    getJobUptime() {
      this.uptimeLoading = true;
      this.$http
        .get(`/api/v1/jobs/${this.uuid}/uptime/`)
        .then((result) => {
          if (result.status === 200) {
            this.jobUptime = result.data.uptime;
          } else {
            this.jobUptime = "Failed";
          }
        })
        .catch(() => {
          this.jobUptime = "Failed";
        })
        .finally(() => {
          this.uptimeLoading = false;
        });
    },
  },
};
</script>

<style>
</style>