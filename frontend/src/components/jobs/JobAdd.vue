<template>
  <v-row justify="center">
    <v-btn
      color="pink"
      small
      fab
      fixed
      bottom
      right
      class="mb-8 mx-4"
      @click="openAddJobDialog"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-dialog v-model="addJobDialog" persistent max-width="750px">
      <v-stepper v-model="step" elevation="0" class="secondary">
        <v-stepper-header>
          <v-stepper-step :complete="step > 1" step="1" editable>
            Basic Details
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="step > 2" step="2" editable>
            Advanced
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step step="3" editable> Notifiers </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-form ref="addJobForm" lazy-validation>
            <v-stepper-content step="1">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="jobItem.title"
                    label="Title*"
                    required
                    counter
                    maxlength="15"
                    :rules="titleRule"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="jobItem.url"
                    label="URL*"
                    required
                    :rules="UrlRule"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-slider
                    v-model="jobItem.interval"
                    hint="Min."
                    max="180"
                    min="5"
                    label="Interval"
                    persistent-hint
                    thumb-label="always"
                  ></v-slider>
                </v-col>
              </v-row>

              <v-col class="text-right">
                <v-btn text class="text-capitalize" @click="closeAddJobDialog">
                  Cancel
                </v-btn>
                <v-btn color="primary" @click="step = 2" icon>
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-col>
            </v-stepper-content>

            <v-stepper-content step="2">
              <v-row class="mb-4">
                <v-col cols="6">
                  <v-label>Headers</v-label>
                  <v-btn @click="addHeader" icon
                    ><v-icon small>mdi-plus</v-icon></v-btn
                  >
                </v-col>
                <v-col cols="6"> </v-col>

                <v-row v-for="(textField, i) in headers" :key="i" class="ml-5">
                  <v-col cols="4">
                    <v-text-field
                      label="Key"
                      dense
                      v-model="textField.key"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="4">
                    <v-text-field
                      label="Value"
                      dense
                      v-model="textField.value"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="4">
                    <v-btn @click="removeHeader(i)" icon color="pink"
                      ><v-icon>mdi-close</v-icon></v-btn
                    >
                  </v-col>
                </v-row>

                <v-col cols="12" class="mt-3">
                  <v-select
                    label="Success Status"
                    v-model="jobItem.success_status"
                    :items="success_status"
                    filled
                    dense
                    clearable
                    multiple
                    deletable-chips
                    small-chips
                    :rules="[(v) => !!v || 'Item is required']"
                  ></v-select>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model="jobItem.failure_threshold"
                    label="Failure Threshold"
                    required
                    min="1"
                    :rules="numberRule"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="12" md="4" lg="4">
                  <v-switch
                    v-model="jobItem.state"
                    label="Enabled"
                    color="primary"
                    hide-details
                  ></v-switch>
                </v-col>
                <v-col cols="12" sm="12" md="4" lg="4">
                  <v-switch
                    v-model="jobItem.verify_ssl"
                    label="Verify SSL"
                    color="red"
                    hide-details
                  ></v-switch>
                </v-col>
                <v-col cols="12" sm="12" md="4" lg="4">
                  <v-switch
                    v-model="jobItem.check_redirect"
                    label="Check Redirect"
                    color="green"
                    hide-details
                  ></v-switch>
                </v-col>
              </v-row>

              <v-col class="text-right">
                <v-btn text class="text-capitalize" @click="closeAddJobDialog">
                  Cancel
                </v-btn>
                <v-btn color="primary" @click="step = 3" icon>
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-col>
            </v-stepper-content>

            <v-stepper-content step="3">
              <v-row class="mb-4">
                <v-col cols="12">
                  <v-select
                    label="Notifiers"
                    v-model="jobItem.notifiers"
                    :items="notifiers"
                    item-text="title"
                    item-value="uuid"
                    filled
                    clearable
                    multiple
                    deletable-chips
                    small-chips
                    counter="5"
                    prepend-icon="mdi-bell"
                  >
                    <template v-slot:selection="data">
                      <v-chip
                        v-bind="data.attrs"
                        :input-value="data.selected"
                        close
                        @click="data.select"
                        @click:close="removeChip(data.item)"
                      >
                        <v-avatar left>
                          <v-icon>{{ getIcon(data.item.type) }}</v-icon>
                        </v-avatar>
                        {{ data.item.title }}
                      </v-chip>
                    </template>
                    <template v-slot:item="data">
                      <template>
                        <v-list-item-icon>
                          <v-icon>{{ getIcon(data.item.type) }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title
                            v-html="data.item.title"
                          ></v-list-item-title>
                        </v-list-item-content>
                      </template>
                    </template>
                  </v-select>
                </v-col>
              </v-row>

              <v-col class="text-right">
                <v-btn text class="text-capitalize" @click="closeAddJobDialog">
                  Cancel
                </v-btn>
                <v-btn
                  color="pink"
                  class="text-capitalize"
                  :loading="addJobBtnLoader"
                  :disabled="addJobBtnLoader"
                  @click="addJob"
                >
                  Submit
                </v-btn>
              </v-col>
            </v-stepper-content>
          </v-form>
        </v-stepper-items>
      </v-stepper>
    </v-dialog>
  </v-row>
</template>

<script>
import rulesMixin from "@/mixins/rulesMixin";
import { EventBus } from "@/helpers/eventBus";

export default {
  name: "JobAdd",

  mixins: [rulesMixin],

  data: () => ({
    step: 1,
    addJobDialog: false,
    addJobBtnLoader: false,
    success_status: [
      200, 201, 202, 203, 204, 100, 101, 102, 205, 206, 207, 208, 226, 300, 301,
      302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408,
      409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 426,
      428, 429, 431, 444, 451, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508,
      510, 511, 599,
    ],
    notifiers: [],
    headers: [],
    jobItem: {
      title: "",
      url: "",
      interval: 15,
      state: true,
      verify_ssl: true,
      check_redirect: false,
      headers: {},
      notifiers: [],
      success_status: [200],
      failure_threshold: 1,
    },
    jobDefaultItem: {
      title: "",
      url: "",
      interval: 15,
      state: true,
      verify_ssl: true,
      check_redirect: false,
      headers: {},
      notifiers: [],
      success_status: [200],
      failure_threshold: 1,
    },
  }),

  created() {
    this.loadNotifiers();
  },

  methods: {
    loadNotifiers() {
      this.$http
        .get(`/api/v1/notifiers`)
        .then((result) => {
          this.notifiers = result.data;
        })
        .finally(() => {});
    },

    addHeader() {
      this.headers.push({ key: "", value: "" });
    },
    removeHeader(index) {
      this.headers.splice(index, 1);
    },
    openAddJobDialog() {
      this.addJobDialog = true;
    },
    closeAddJobDialog() {
      this.addJobDialog = false;
      this.$refs.addJobForm.reset();
      this.jobItem = Object.assign({}, this.jobDefaultItem);
      this.step = 1;
      this.$refs.addJobForm.resetValidation();
    },

    addJob() {
      if (this.$refs.addJobForm.validate()) {
        this.addJobBtnLoader = true;

        for (let header of this.headers) {
          this.jobItem.headers[header.key] = header.value;
        }

        this.$http
          .post("/api/v1/jobs/", this.jobItem)
          .then((result) => {
            if (result.status === 201) {
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Job Added",
              });
              this.$emit("jobAddedEvent", result.data);
              this.closeAddJobDialog();
            }
          })
          .finally(() => {
            this.addJobBtnLoader = false;
          });
      }
    },

    getIcon(val) {
      switch (val) {
        case "slack":
          return "mdi-slack";
        case "telegram":
          return "mdi-send";
        case "discord":
          return "mdi-discord";
        case "gotify":
          return "mdi-message";
        case "webhook":
          return "mdi-webhook";
      }
    },

    removeChip(item) {
      const index = this.jobItem.notifiers.indexOf(item.uuid);
      if (index >= 0) this.jobItem.notifiers.splice(index, 1);
    },
  },
};
</script>

<style>
</style>