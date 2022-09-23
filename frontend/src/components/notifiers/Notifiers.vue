<template>
  <v-container fluid>
    <v-tabs v-model="tab" background-color="background" center-active centered>
      <v-tab
        class="text-capitalize"
        v-for="(notifier, code) in notifierTypes"
        :key="code"
        ><v-icon small class="mr-1">{{ notifier.icon }}</v-icon>
        {{ notifier.name }}</v-tab
      >
    </v-tabs>

    <v-tabs-items v-model="tab" class="mt-5" id="tabs">
      <v-tab-item v-for="(notifier, code) in notifierTypes" :key="code">
        <v-row align="center" justify="center" class="mx-5">
          <loader v-if="notifierLoader" />
          <v-col
            v-else-if="notifier.notifiers.length < 1"
            cols="12"
            sm="12"
            md="4"
            lg="4"
            class="mt-1 mt-md-8"
          >
            <v-alert type="info" text dense> No Notifiers found. </v-alert>
          </v-col>
          <v-col
            v-else
            cols="12"
            sm="4"
            md="3"
            lg="3"
            class="ma-1 mt-md-8"
            v-for="item in notifier.notifiers"
            :key="item.uuid"
          >
            <v-hover v-slot="{ hover }">
              <v-card
                :elevation="hover ? 5 : 1"
                :class="{ 'on-hover': hover }"
                outlined
                color="secondary"
                :to="{ name: 'notifierDetails', params: { uuid: item.uuid } }"
                class="mx-6 ma-sm-0 ma-lg-0"
              >
                <v-card-title class="justify-center text-capitalize">
                  {{ item.title }}
                </v-card-title>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import Loader from "../Loader.vue";
import notifiersMap from "./notifiers.js";

export default {
  name: "Notifiers",
  components: {
    Loader,
  },

  data: () => ({
    tab: null,
    notifierTypes: {},

    notifierLoader: false,
  }),

  created() {
    this.notifierTypes = notifiersMap;
    for (var notifier of Object.keys(this.notifierTypes)) {
      this.notifierTypes[notifier].notifiers = [];
    }
    this.getNotifiers();
  },

  methods: {
    getNotifiers() {
      this.notifierLoader = true;
      this.$http
        .get("/api/v1/notifiers/")
        .then((result) => {
          for (var notifier of result.data) {
            this.notifierTypes[notifier.type].notifiers.push(notifier);
          }
        })
        .finally(() => {
          this.notifierLoader = false;
        });
    },
  },
};
</script>
<style scoped>
#tabs {
  background-color: transparent !important;
}
</style>