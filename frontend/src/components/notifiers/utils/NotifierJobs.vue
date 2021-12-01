<template>
  <v-col cols="12" sm="6" md="6" lg="6">
    <v-card elevation="1" color="transparent">
      <v-card-title>
        <h5><v-icon>mdi-memory</v-icon> Jobs</h5>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="items"
        :search="search"
        :items-per-page="5"
        :loading="tableLoading"
        :loader-height="1"
        loading-text="Fetching data..."
        class="transparent mt-2"
      >
        <template v-slot:[`item.state`]="{ item }">
          <v-icon small :color="getStatusColor(item.state)">{{
            getPrettyStatusIcon(item.state)
          }}</v-icon>
        </template>
        <template v-slot:[`item.healthy`]="{ item }">
          <v-icon small :color="getStatusColor(item.healthy)">{{
            getPrettyStatusIcon(item.healthy)
          }}</v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "NotifierJobs",
  props: {
    uuid: String,
  },
  data: () => ({
    search: "",
    tableLoading: true,
    headers: [
      {
        text: "Title",
        align: "start",
        value: "title",
      },
      { text: "State", value: "state" },
      { text: "Healthy", value: "healthy" },
    ],
    items: [],
  }),
  watch: {
    uuid() {
      this.getNotifierJobs();
    },
  },
  created() {
    this.getNotifierJobs();
  },
  methods: {
    getNotifierJobs() {
      this.tableLoading = true;
      this.$http
        .get(`/api/v1/notifiers/${this.uuid}/jobs/`)
        .then((result) => {
          if (result.status === 200) {
            this.items = result.data;
          }
        })
        .catch(() => {})
        .finally(() => {
          this.tableLoading = false;
        });
    },
  },
};
</script>

<style>
</style>