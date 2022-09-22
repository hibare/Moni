<template>
  <v-container fluid>
    <v-row class="px-4 mb-4">
      <loader v-if="notifierLoader" />
      <v-col cols="12" sm="12" lg="12" md="12">
        <v-card elevation="1" color="background">
          <v-card-title>
            <h3>
              <v-icon class="mr-1">{{ notifier.icon }}</v-icon>
              {{ notifier.title }}
            </h3>
            <v-spacer></v-spacer>
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  x-small
                  color="lime darken-1"
                  class="mx-5"
                  v-bind="attrs"
                  v-on="on"
                  :loading="testNotifierBtnLoader"
                  @click="testSavedNotifier"
                >
                  <v-icon>mdi-test-tube</v-icon>
                </v-btn>
              </template>
              <span>Test Notifier</span>
            </v-tooltip>

            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  x-small
                  v-bind="attrs"
                  v-on="on"
                  color="green darken-1"
                  @click="openEditNotifierDialog"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>
              <span>Edit Notifier</span>
            </v-tooltip>

            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  x-small
                  v-bind="attrs"
                  v-on="on"
                  color="pink darken-1"
                  class="mx-5"
                  @click="openDeleteNotifierDialog"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span>Delete Notifier</span>
            </v-tooltip>
          </v-card-title>
          <v-card-subtitle class="my-1">{{
            notifier.description
          }}</v-card-subtitle>
          <v-card-text>
            <v-text-field
              dense
              readonly
              label=""
              filled
              :value="notifier.url"
              :append-icon="showURL ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showURL ? 'text' : 'password'"
              @click:append="showURL = !showURL"
              class="webhook"
            ></v-text-field>
          </v-card-text>
        </v-card>

        <v-row align="center" class="mt-3">
          <notifier-created :created="notifier.created" />
          <notifier-modified :modified="notifier.updated" />
          <notifier-jobs-count :uuid="notifier.uuid" />
          <notifier-delivery :uuid="notifier.uuid" />
        </v-row>

        <v-row>
          <notifier-jobs :uuid="notifier.uuid" />
          <notifier-history :uuid="notifier.uuid" />
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Loader from "../Loader.vue";
import { EventBus } from "@/events/eventBus";
import NotifierJobsCount from "./NotifierJobsCount.vue";
import NotifierDelivery from "./NotifierDelivery.vue";
import NotifierCreated from "./NotifierCreated.vue";
import NotifierModified from "./NotifierModified.vue";
import NotifierJobs from "./NotifierJobs.vue";
import NotifierHistory from "./NotifierHistory.vue";
import notifiersMap from "./notifiers.js";

export default {
  name: "NotifierDetails",

  components: {
    Loader,
    NotifierJobsCount,
    NotifierDelivery,
    NotifierCreated,
    NotifierModified,
    NotifierJobs,
    NotifierHistory,
  },

  data: () => ({
    uuid: null,
    notifier: {},

    // Status flags
    showURL: false,

    // Dialogs status flags
    addNotifierDialog: false,
    editNotifierDialog: false,
    deleteNotifierDialog: false,

    // Button loader status flags
    addNotifierBtnLoader: false,
    editNotifierBtnLoader: false,
    deleteNotifierBtnLoader: false,
    testNotifierBtnLoader: false,
    notifierLoader: false,
  }),

  created() {
    this.uuid = this.$route.params.uuid;
    this.getNotifier();
  },

  watch: {
    notifier() {
      this.notifier.icon = notifiersMap[this.notifier.type].icon;
    },
  },

  methods: {
    getNotifier() {
      this.notifierLoader = true;
      this.$http
        .get(`/api/v1/notifiers/${this.uuid}/`)
        .then((result) => {
          this.notifier = result.data;
        })
        .finally(() => {
          this.notifierLoader = false;
        });
    },

    openEditNotifierDialog() {},

    testSavedNotifier() {
      const uuid = this.uuid;
      this.testNotifierBtnLoader = true;
      this.$http
        .post(`/api/v1/notifiers/${uuid}/test/`, this.notifier)
        .then((result) => {
          if (result.status === 200) {
            EventBus.$emit("showSnackbar", {
              status: "success",
              message: "Test success",
            });
          }
        })
        .finally(() => {
          this.testNotifierBtnLoader = false;
        });
    },

    testNotifier() {
      this.testNotifierBtnLoader = true;
      this.$http
        .post("/api/v1/notifiers/test/", this.notifier)
        .then((result) => {
          if (result.status === 200) {
            EventBus.$emit("showSnackbar", {
              status: "success",
              message: "Test success",
            });
            this.notifier.valid = true;
          }
        })
        .finally(() => {
          this.testNotifierBtnLoader = false;
        });
    },

    openDeleteNotifierDialog() {
      this.deleteNotifierDialog = true;
    },

    closeDeleteNotifierDialog() {
      this.deleteNotifierDialog = false;
      this.notifier = Object.assign({}, this.defaultNotifier);
    },
  },
};
</script>