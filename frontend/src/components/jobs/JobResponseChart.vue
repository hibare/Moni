<template>
  <v-col cols="12" sm="12" lg="12" md="12" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle
        ><v-icon small>mdi-clock-outline</v-icon> Response Time</v-card-subtitle
      >
      <v-card-text class="justify-center">
        <v-progress-circular
          indeterminate
          color="primary"
          v-if="loading"
        ></v-progress-circular>
        <v-sparkline
          :gradient="selectedGradient"
          :line-width="width"
          :padding="padding"
          :smooth="radius || false"
          :value="values"
          height="30"
          auto-draw
          class="py-2"
          v-else-if="values.length > 0"
        ></v-sparkline>
        <v-card-subtitle v-else>No data found.</v-card-subtitle>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "JobResponseChart",
  props: {
    uuid: String,
  },
  data: () => ({
    selectedGradient: ["#00c6ff", "#F0F", "#FF0"],
    width: 1,
    padding: 0,
    radius: 4,
    values: [],
    loading: false,
  }),

  watch: {
    uuid() {
      this.getJobhistory();
    },
  },
  created() {
    this.getJobhistory();
  },
  methods: {
    getJobhistory() {
      this.loading = true;
      this.$http
        .get(`/api/v1/jobs/${this.uuid}/history/`)
        .then((result) => {
          if (result.status === 200) {
            for (var item of result.data) {
              if (item.response_time !== null)
                this.values.push(item.response_time);
            }
          }
        })
        .catch(() => {})
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
</style>