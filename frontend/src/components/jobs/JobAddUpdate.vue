<template>
  <v-row justify="center">
    <v-dialog v-model="jobDialog" persistent max-width="750px">
      <v-card class="mx-auto px-2" max-width="750" color="secondary">
        <v-card-title class="text-h6 font-weight-regular justify-space-between">
          {{ currentTitle }}
          <v-spacer></v-spacer>
          <v-btn icon small color="red" @click="closeJobDialog"
            ><v-icon small>mdi-close</v-icon></v-btn
          >
        </v-card-title>
        <v-window v-model="step" elevation="0" class="secondary">
          <v-form ref="jobForm" lazy-validation>
            <v-window-item :value="1">
              <v-card-text>
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
              </v-card-text>
            </v-window-item>

            <v-window-item :value="2">
              <v-card-text>
                <v-row class="mb-4">
                  <v-col cols="6">
                    <v-label>Headers</v-label>
                    <v-btn @click="addHeader" icon
                      ><v-icon small>mdi-plus</v-icon></v-btn
                    >
                  </v-col>
                  <v-col cols="6"> </v-col>

                  <v-row
                    v-for="(textField, i) in headers"
                    :key="i"
                    class="ml-5"
                  >
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
              </v-card-text>
            </v-window-item>

            <v-window-item :value="3">
              <v-card-text>
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
              </v-card-text>
            </v-window-item>
          </v-form>
        </v-window>
        <v-divider></v-divider>

        <v-card-actions>
          <v-btn :disabled="step === 1" text @click="step--"> Back </v-btn>
          <v-spacer></v-spacer>

          <v-btn
            color="green"
            text
            class="text-capitalize"
            :loading="jobBtnLoader"
            :disabled="jobBtnLoader"
            @click="submitJob"
            v-if="step === 3"
          >
            Submit
          </v-btn>
          <v-btn v-else text @click="nextWindow"> Next </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import rulesMixin from "@/mixins/rulesMixin";
import { EventBus } from "@/events/eventBus";
import notifiersMap from "@/components/notifiers/notifiers.js";

export default {
  name: "JobAddUpdate",

  mixins: [rulesMixin],

  props: {
    jobDialog: {
      default: false,
    },
    job: {
      default: null,
    },
  },

  data: () => ({
    step: 1,
    jobBtnLoader: false,
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

  watch: {
    jobDialog(val) {
      if (val) {
        this.loadJob();
        this.loadNotifiers();
      }
    },
  },

  computed: {
    currentTitle() {
      switch (this.step) {
        case 1:
          return "Basic Details";
        case 2:
          return "Advanced";
        case 3:
          return "Notifiers";
        default:
          return "Job";
      }
    },
  },

  methods: {
    nextWindow() {
      if (this.$refs.jobForm.validate()) {
        this.step++;
      }
    },

    // Load old job for edit operation
    loadJob() {
      if (this.job !== null) {
        this.jobItem = Object.assign({}, this.job);
        this.headers = [];
        for (let [key, value] of Object.entries(this.jobItem.headers)) {
          this.headers.push({ key: key, value: value });
        }
        this.jobItem.headers = {};
      }
    },

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

    openJobDialog() {
      this.jobDialog = true;
    },

    closeJobDialog() {
      this.$refs.jobForm.reset();
      this.$refs.jobForm.resetValidation();
      this.jobItem = Object.assign({}, this.jobDefaultItem);
      this.step = 1;
      this.$emit("update:jobDialog", false);
    },

    submitJob() {
      if (this.job === null) {
        this.addJob();
      } else {
        this.editJob();
      }
    },

    addJob() {
      if (this.$refs.jobForm.validate()) {
        this.jobBtnLoader = true;

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
              EventBus.$emit("jobAddedEvent", result.data);
              this.closeJobDialog();
            }
          })
          .finally(() => {
            this.jobBtnLoader = false;
          });
      }
    },

    editJob() {
      if (this.$refs.jobForm.validate()) {
        this.jobBtnLoader = true;

        for (let header of this.headers) {
          this.jobItem.headers[header.key] = header.value;
        }

        this.$http
          .patch(`/api/v1/jobs/${this.job.uuid}/`, this.jobItem)
          .then((result) => {
            if (result.status === 200) {
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Job updated",
              });
              EventBus.$emit("jobEditEvent", result.data);
              this.closeJobDialog();
            }
          })
          .finally(() => {
            this.jobBtnLoader = false;
          });
      }
    },

    getIcon(val) {
      return notifiersMap[val]["icon"];
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