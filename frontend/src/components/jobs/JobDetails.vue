<template>
  <v-container fluid>
    <loader v-if="jobLoader" />
    <v-row class="px-4" v-else>
      <v-col cols="12" sm="12" lg="12" md="12">
        <v-card elevation="1" color="background">
          <v-card-title>
            <v-col cols="12" sm="6" lg="6" md="6" class="py-0 px-0 px-sm-2">
              <h3>
                <v-icon class="mr-2" v-if="job.favicon_url === null"
                  >mdi-web</v-icon
                >
                <img
                  :src="job.favicon_url"
                  alt=""
                  height="24"
                  width="24"
                  class="mr-2 ma-0"
                  v-else
                />
                {{ job.title }}
                <v-chip
                  close-icon="mdi-delete"
                  x-small
                  outlined
                  v-if="!job.state"
                  >Disabled</v-chip
                >
                <v-icon small class="mr-1" color="green" v-else-if="job.healthy"
                  >mdi-circle-medium</v-icon
                >
                <v-icon small class="mr-1" color="red" v-else
                  >mdi-circle-medium</v-icon
                >
              </h3>

              <v-card-subtitle class="mt-2 mb-4">
                <v-row class="text-truncate">{{ job.url }}</v-row>
                <v-row class="subtitle mt-6">
                  <span class="pr-3"
                    ><v-icon small color="blue lighten-1" class="mr-1 pb-1"
                      >mdi-update</v-icon
                    >{{ job.interval }} Min.</span
                  >
                  <span class="pr-3"
                    ><v-icon small color="yellow lighten-1" class="mr-1 pb-1"
                      >mdi-format-list-checks</v-icon
                    >{{ job.success_status.join(", ") }}</span
                  >
                  <span class="pr-2"
                    ><v-icon
                      v-if="job.verify_ssl"
                      small
                      color="green lighten-1"
                      class="mr-1 pb-1"
                      >mdi-shield</v-icon
                    >
                    <v-icon v-else small color="red lighten-1" class="mr-1 pb-1"
                      >mdi-shield-alert</v-icon
                    ></span
                  >
                  <span class="pr-3"
                    ><v-icon
                      v-if="job.check_redirect"
                      small
                      color="green lighten-1"
                      class="mr-1 pb-1"
                      >mdi-repeat</v-icon
                    >
                    <v-icon v-else small color="red lighten-1" class="mr-1 pb-1"
                      >mdi-repeat-off</v-icon
                    ></span
                  >
                </v-row>
              </v-card-subtitle>
            </v-col>
            <v-col
              cols="12"
              sm="6"
              lg="6"
              md="6"
              class="
                py-0
                px-0 px-sm-2
                d-flex
                justify-lg-end justify-sm-end justify-top
              "
            >
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    x-small
                    color="amber accent-2"
                    class="mr-5"
                    v-bind="attrs"
                    v-on="on"
                    :loading="stateToggleLoader"
                    :disabled="stateToggleLoader"
                    @click="toggleJobState"
                  >
                    <v-icon v-if="job.state">mdi-pause</v-icon>
                    <v-icon v-else>mdi-play</v-icon>
                  </v-btn>
                </template>
                <span v-if="job.state">Pause Job</span>
                <span v-else>Resume Job</span>
              </v-tooltip>

              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    x-small
                    v-bind="attrs"
                    v-on="on"
                    color="blue darken-1"
                    class="mr-5"
                    :loading="reloadFaviconLoader"
                    :disabled="reloadFaviconLoader"
                    @click="reloadFavicon"
                  >
                    <v-icon>mdi-image-filter-hdr</v-icon>
                  </v-btn>
                </template>
                <span>Reload Favicon</span>
              </v-tooltip>

              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    x-small
                    v-bind="attrs"
                    v-on="on"
                    color="green darken-1"
                    @click="openEditJobDialog"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>Edit Job</span>
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
                    @click="openDeleteJobDialog"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
                <span>Delete Job</span>
              </v-tooltip>
            </v-col>
          </v-card-title>
        </v-card>

        <v-row align="center" class="mt-3">
          <job-created :created="job.created" />
          <job-modified :modified="job.updated" />
          <job-uptime :uuid="job.uuid" />
          <job-response :uuid="job.uuid" />
        </v-row>

        <v-row>
          <job-notifiers :uuids="job.notifiers" />
          <job-history :uuid="job.uuid" />
          <job-edit
            @jobEditEvent="jobEditEventHandler"
            @jobEditClose="closeEditJobDialog"
            :editJobDialog="editJobDialog"
            :job="job"
          />
        </v-row>
      </v-col>
    </v-row>

    <!-- Delete Job -->
    <v-dialog persistent v-model="deleteJobDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5"> <v-icon>mdi-delete</v-icon> Delete Job</span>
          <v-spacer></v-spacer>
          <v-btn icon small @click="closeDeleteJobDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="justify-center py-10">
          Do you want to delete job
          <strong>{{ this.job.title }}</strong
          >?
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="pink darken-1"
            block
            depressed
            outlined
            class="text-capitalize"
            :disabled="deleteJobBtnLoader"
            :loading="deleteJobBtnLoader"
            @click="deleteJob"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ./Delete Job -->
  </v-container>
</template>

<script>
import Loader from "../Loader.vue";
import { EventBus } from "@/helpers/eventBus";
import JobCreated from "./JobCreated.vue";
import JobModified from "./JobModified.vue";
import JobUptime from "./JobUptime.vue";
import JobResponse from "./JobResponse.vue";
import JobNotifiers from "./JobNotifiers.vue";
import JobHistory from "./JobHistory.vue";
import JobEdit from "./JobEdit.vue";

export default {
  name: "JobDetails",
  components: {
    Loader,
    JobCreated,
    JobModified,
    JobUptime,
    JobResponse,
    JobNotifiers,
    JobHistory,
    JobEdit,
  },

  data: () => ({
    job: {},

    jobLoader: false,
    stateToggleLoader: false,
    deleteJobBtnLoader: false,
    reloadFaviconLoader: false,

    deleteJobDialog: false,
    editJobDialog: false,
  }),

  created() {
    const uuid = this.$route.params.uuid;
    this.getJob(uuid);
  },

  methods: {
    getJob(uuid) {
      this.jobLoader = true;
      this.$http
        .get(`/api/v1/jobs/${uuid}/`)
        .then((result) => {
          this.job = result.data;
        })
        .finally(() => {
          this.jobLoader = false;
        });
    },

    deleteJob() {
      this.deleteJobBtnLoader = true;

      const uuid = this.job.uuid;
      this.$http
        .delete(`/api/v1/jobs/${uuid}/`)
        .then((result) => {
          if (result.status === 204) {
            EventBus.$emit("showSnackbar", {
              status: "success",
              message: "Job deleted",
            });
            this.closeDeleteJobDialog();
            this.$router.replace({ name: "jobs" });
          }
        })
        .finally(() => {
          this.deleteJobBtnLoader = false;
        });
    },

    toggleJobState() {
      var endpoint = "";
      const uuid = this.job.uuid;
      if (this.job.state) endpoint = `/api/v1/jobs/${uuid}/pause/`;
      else endpoint = `/api/v1/jobs/${uuid}/resume/`;

      this.stateToggleLoader = true;
      this.$http
        .post(endpoint)
        .then((result) => {
          if (result.status === 200) this.job.state = !this.job.state;
        })
        .finally(() => {
          this.stateToggleLoader = false;
        });
    },

    reloadFavicon() {
      const uuid = this.job.uuid;
      this.reloadFaviconLoader = true;
      this.$http
        .get(`/api/v1/jobs/${uuid}/favicon/`)
        .then((result) => {
          if (result.status === 200) this.getJob(uuid);
        })
        .finally(() => {
          this.reloadFaviconLoader = false;
        });
    },

    openDeleteJobDialog() {
      this.deleteJobDialog = true;
    },
    closeDeleteJobDialog() {
      this.deleteJobDialog = false;
    },

    openEditJobDialog() {
      this.editJobDialog = true;
    },

    closeEditJobDialog() {
      this.editJobDialog = false;
    },

    jobEditEventHandler() {
      this.getJob(this.job.uuid);
      this.closeEditJobDialog();
    },
  },
};
</script>

<style>
</style>