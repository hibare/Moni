<template>
  <v-col cols="12" sm="6" md="6" lg="6">
    <v-card elevation="1" color="transparent">
      <v-card-title>
        <h5><v-icon>mdi-bell</v-icon> Notifiers</h5>
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
        <template v-slot:[`item.type`]="{ item }">
          {{ item.type }}
        </template>
      </v-data-table>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "JobNotifiers",
  props: {
    uuids: Array,
  },
  data: () => ({
    search: "",
    tableLoading: false,
    headers: [
      {
        text: "Type",
        value: "type",
      },
      { text: "Title", value: "title" },
    ],
    items: [],
  }),
  watch: {
    uuids() {
      this.getJobNotifiers();
      console.log(this.uuids);
    },
  },
  created() {
    this.getJobNotifiers();
  },
  methods: {
    getJobNotifiers() {
      for (var uuid of this.uuids) {
        this.tableLoading = true;
        this.$http
          .get(`/api/v1/notifiers/${uuid}/`)
          .then((result) => {
            if (result.status === 200) {
              this.items.push(result.data);
            }
          })
          .catch(() => {})
          .finally(() => {
            this.tableLoading = false;
          });
      }
    },
  },
};
</script>

<style>
</style>