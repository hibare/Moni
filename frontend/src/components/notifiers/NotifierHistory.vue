<template>
  <v-col cols="12" sm="6" md="6" lg="6">
    <v-card elevation="1" color="transparent">
      <v-card-title>
        <h5><v-icon>mdi-history</v-icon> History</h5>
        <v-spacer></v-spacer>
        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              x-small
              v-bind="attrs"
              v-on="on"
              color="pink darken-1"
              class="mx-5"
              :disabled="items.length === 0"
              @click="openDeleteHistoryDialog"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
          <span>Delete History</span>
        </v-tooltip>
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
        <template v-slot:[`item.timestamp`]="{ item }">
          {{ getPrettyDate(item.timestamp) }}
        </template>
        <template v-slot:[`item.status`]="{ item }">
          <v-icon small :color="getStatusColor(item.status)">{{
            getPrettyStatusIcon(item.status)
          }}</v-icon>
        </template>
        <template v-slot:[`item.error`]="{ item }">
          {{ fillEmptyValue(item.error) }}
        </template>
      </v-data-table>
    </v-card>

    <!-- Delete notifier -->
    <v-dialog persistent v-model="deleteHistoryDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5">
            <v-icon>mdi-delete</v-icon> Delete History</span
          >
          <v-spacer></v-spacer>
          <v-btn icon small @click="closeDeleteHistoryDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="justify-center py-10">
          Do you want to delete notifier history?
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="pink darken-1"
            block
            depressed
            outlined
            class="text-capitalize"
            :disabled="deleteHistoryBtnLoader"
            :loading="deleteHistoryBtnLoader"
            @click="deleteNotifierHistory"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ./Delete notifier -->
  </v-col>
</template>

<script>
import dateMixin from "@/mixins/dateMixin";

export default {
  name: "NotifierHistory",
  mixins: [dateMixin],
  props: {
    uuid: String,
  },
  data: () => ({
    search: "",
    tableLoading: true,
    headers: [
      {
        text: "Timestamp",
        align: "start",
        value: "timestamp",
      },
      { text: "Status", value: "status" },
      { text: "Status Code", value: "status_code" },
      { text: "Error", value: "error" },
    ],
    items: [],
    deleteHistoryDialog: false,
    deleteHistoryBtnLoader: false,
  }),
  watch: {
    uuid() {
      this.getNotifierhistory();
    },
  },
  created() {
    this.getNotifierhistory();
  },
  methods: {
    getNotifierhistory() {
      this.tableLoading = true;
      this.$http
        .get(`/api/v1/notifiers/${this.uuid}/history/`)
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

    openDeleteHistoryDialog() {
      this.deleteHistoryDialog = true;
    },
    closeDeleteHistoryDialog() {
      this.deleteHistoryDialog = false;
    },

    deleteNotifierHistory() {
      this.deleteHistoryBtnLoader = true;
      this.$http
        .delete(`/api/v1/notifiers/${this.uuid}/history`)
        .then((result) => {
          if (result.status === 204) {
            this.closeDeleteHistoryDialog();
            this.items = [];
            this.getNotifierhistory();
          }
        })
        .finally(() => {
          this.deleteHistoryBtnLoader = false;
        });
    },
  },
};
</script>

<style>
</style>