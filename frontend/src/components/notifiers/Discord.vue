<template>
  <v-container fluid>
    <v-row class="px-4">
      <v-col cols="12" sm="12" lg="3" md="12">
        <v-card elevation="1" color="background">
          <v-card-title class="body-2"
            >Notifiers ({{ notifiers.length }})
            <v-spacer></v-spacer>
            <v-btn icon small @click="openAddNotifierDialog"
              ><v-icon>mdi-plus</v-icon></v-btn
            >
          </v-card-title>
          <v-card-text>
            <v-list dense color="background">
              <v-list-item-group
                v-if="notifiers.length > 0"
                v-model="selectedItem"
                color="primary"
                mandatory
              >
                <v-list-item v-for="(item, i) in notifiers" :key="i">
                  <v-list-item-content>
                    <v-list-item-title v-text="item.title"></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
              <v-list-item v-else-if="fethNotiferLoader">
                <v-list-item-content>
                  <v-list-item-title>
                    <v-progress-circular
                      indeterminate
                      color="primary"
                    ></v-progress-circular>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" lg="9" md="12">
        <div v-if="notifiers.length > 0">
          <v-card elevation="1" color="background">
            <v-card-title>
              <h3>
                <v-icon class="mr-1">mdi-discord</v-icon>
                {{ selectedNotifier.title }}
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
              selectedNotifier.description
            }}</v-card-subtitle>
            <v-card-text>
              <v-text-field
                dense
                readonly
                label=""
                filled
                :value="selectedNotifier.url"
                :append-icon="showURL ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showURL ? 'text' : 'password'"
                @click:append="showURL = !showURL"
                class="webhook"
              ></v-text-field>
            </v-card-text>
          </v-card>

          <v-row align="center" class="mt-3">
            <notifier-created :created="selectedNotifier.created" />
            <notifier-modified :modified="selectedNotifier.updated" />
            <notifier-jobs-count :uuid="selectedNotifier.uuid" />
            <notifier-delivery :uuid="selectedNotifier.uuid" />
          </v-row>

          <v-row>
            <notifier-jobs :uuid="selectedNotifier.uuid" />
            <notifier-history :uuid="selectedNotifier.uuid" />
          </v-row>
        </div>
        <v-card v-else color="background">
          <v-card-title class="justify-center">
            <v-icon>mdi-bell</v-icon> &nbsp; No Notifiers Found
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add notifier -->
    <v-dialog persistent v-model="addNotifierDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5"> <v-icon>mdi-pencil</v-icon> Add Notifier</span>
          <v-spacer></v-spacer>
          <v-btn icon small @click="closeAddNotifierDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="addNotifier" lazy-validation>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Title*"
                  v-model="notifier.title"
                  required
                  counter
                  maxlength="15"
                  :rules="titleRule"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="URL*"
                  required
                  v-model="notifier.url"
                  :rules="discordUrlRule"
                  :append-icon="showURL ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showURL ? 'text' : 'password'"
                  @click:append="showURL = !showURL"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  label="Description"
                  clearable
                  clear-icon="mdi-close-circle"
                  rows="3"
                  row-height="10"
                  v-model="notifier.description"
                ></v-textarea>
              </v-col>
              <v-col><small>*indicates required field</small> </v-col>
              <v-col>
                <v-btn
                  color="teal accent-4"
                  block
                  depressed
                  class="text-capitalize"
                  :disabled="addNotifierBtnLoader"
                  :loading="addNotifierBtnLoader"
                  @click="addNotifier"
                  v-if="notifier.valid"
                >
                  Save
                </v-btn>
                <v-btn
                  v-else
                  color="indigo darken-1"
                  block
                  depressed
                  class="text-capitalize"
                  :disabled="testNotifierBtnLoader"
                  :loading="testNotifierBtnLoader"
                  @click="testNotifier"
                >
                  Test</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions> </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ./Add notifier -->

    <!-- Edit notifier -->
    <v-dialog persistent v-model="editNotifierDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5">
            <v-icon>mdi-pencil</v-icon> Edit Notifier</span
          >
          <v-spacer></v-spacer>
          <v-btn icon small @click="closeEditNotifierDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="editNotifier" lazy-validation>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Title*"
                  v-model="notifier.title"
                  required
                  :rules="titleRule"
                  counter
                  maxlength="15"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="URL*"
                  required
                  v-model="notifier.url"
                  :rules="discordUrlRule"
                  :append-icon="showURL ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showURL ? 'text' : 'password'"
                  @click:append="showURL = !showURL"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  label="Description"
                  clearable
                  clear-icon="mdi-close-circle"
                  rows="3"
                  row-height="10"
                  v-model="notifier.description"
                ></v-textarea>
              </v-col>
              <v-col><small>*indicates required field</small> </v-col>
              <v-col>
                <v-btn
                  color="teal accent-4"
                  block
                  depressed
                  class="text-capitalize"
                  :disabled="editNotifierBtnLoader"
                  :loading="editNotifierBtnLoader"
                  @click="editNotifier"
                  v-if="notifier.valid"
                >
                  Update
                </v-btn>
                <v-btn
                  v-else
                  color="indigo darken-1"
                  block
                  depressed
                  class="text-capitalize"
                  :disabled="testNotifierBtnLoader"
                  :loading="testNotifierBtnLoader"
                  @click="testNotifier"
                >
                  Test</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions> </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ./Edit notifier -->

    <!-- Delete notifier -->
    <v-dialog persistent v-model="deleteNotifierDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5">
            <v-icon>mdi-delete</v-icon> Delete Notifier</span
          >
          <v-spacer></v-spacer>
          <v-btn icon small @click="closeDeleteNotifierDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="justify-center py-10">
          Do you want to delete notifier
          <strong>{{ this.selectedNotifier.title }}</strong
          >?
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="pink darken-1"
            block
            depressed
            outlined
            class="text-capitalize"
            :disabled="deleteNotifierBtnLoader"
            :loading="deleteNotifierBtnLoader"
            @click="deleteNotifier"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ./Delete notifier -->
  </v-container>
</template>

<script>
import dateMixin from "@/mixins/dateMixin";
import rulesMixin from "@/mixins/rulesMixin";
import { EventBus } from "@/helpers/eventBus";
import NotifierJobsCount from "./utils/NotifierJobsCount.vue";
import NotifierDelivery from "./utils/NotifierDelivery.vue";
import NotifierCreated from "./utils/NotifierCreated.vue";
import NotifierModified from "./utils/NotifierModified.vue";
import NotifierJobs from "./utils/NotifierJobs.vue";
import NotifierHistory from "./utils/NotifierHistory.vue";

export default {
  name: "Slack",
  components: {
    NotifierJobsCount,
    NotifierDelivery,
    NotifierCreated,
    NotifierModified,
    NotifierJobs,
    NotifierHistory,
  },
  mixins: [dateMixin, rulesMixin],

  data: () => ({
    selectedItem: null,

    // Notifier objects
    notifiers: [],
    selectedNotifier: {},

    notifier: {
      title: "",
      url: "",
      description: "",
      type: "discord",
      valid: false,
    },
    defaultNotifier: {
      title: "",
      url: "",
      description: "",
      type: "discord",
      valid: false,
    },

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
    fethNotiferLoader: false,
  }),

  created() {
    this.getNotifiers();
  },

  watch: {
    selectedItem() {
      try {
        this.selectedNotifier = this.notifiers[this.selectedItem];
      } catch (_) {
        this.selectedNotifier = this.defaultNotifier;
      }
    },
    notifiers(val) {
      if (val.length > 0) {
        this.selectedItem = 0;
      }
    },
  },

  methods: {
    getNotifiers() {
      this.fethNotiferLoader = true;
      this.$http
        .get("/api/v1/notifiers?type=discord")
        .then((result) => {
          this.notifiers = result.data;
        })
        .finally(() => {
          this.fethNotiferLoader = false;
        });
    },

    addNotifier() {
      if (this.$refs.addNotifier.validate()) {
        this.addNotifierBtnLoader = true;

        this.$http
          .post("/api/v1/notifiers/", this.notifier)
          .then((result) => {
            if (result.status === 201) {
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Test success",
              });
              this.notifiers.push(result.data);
              this.closeAddNotifierDialog();
            }
          })
          .finally(() => {
            this.addNotifierBtnLoader = false;
          });
      }
    },
    editNotifier() {
      if (this.$refs.editNotifier.validate()) {
        this.editNotifierBtnLoader = true;
        const uuid = this.selectedNotifier.uuid;
        this.$http
          .put(`/api/v1/notifiers/${uuid}/`, this.notifier)
          .then((result) => {
            if (result.status === 200) {
              EventBus.$emit("showSnackbar", {
                status: "success",
                message: "Notifier updated",
              });
              Object.assign(this.notifiers[this.selectedItem], result.data);
              this.closeEditNotifierDialog();
            }
          })
          .finally(() => {
            this.editNotifierBtnLoader = false;
          });
      }
    },
    deleteNotifier() {
      this.deleteNotifierBtnLoader = true;

      const uuid = this.selectedNotifier.uuid;
      this.$http
        .delete(`/api/v1/notifiers/${uuid}/`)
        .then((result) => {
          if (result.status === 204) {
            EventBus.$emit("showSnackbar", {
              status: "success",
              message: "Notifier deleted",
            });
            this.notifiers.splice(this.selectedItem, 1);
            this.closeDeleteNotifierDialog();
          }
        })
        .finally(() => {
          this.deleteNotifierBtnLoader = false;
        });
    },
    testSavedNotifier() {
      const uuid = this.selectedNotifier.uuid;
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

    openAddNotifierDialog() {
      this.addNotifierDialog = true;
    },
    closeAddNotifierDialog() {
      this.addNotifierDialog = false;
      this.$refs.addNotifier.reset();
      this.$refs.addNotifier.resetValidation();
      this.notifier = Object.assign({}, this.defaultNotifier);
    },

    openEditNotifierDialog() {
      this.editNotifierDialog = true;
      this.notifier = Object.assign({}, this.selectedNotifier);
    },
    closeEditNotifierDialog() {
      this.editNotifierDialog = false;
      this.$refs.editNotifier.reset();
      this.$refs.editNotifier.resetValidation();
      this.notifier = Object.assign({}, this.defaultNotifier);
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

<style scoped>
.webhook {
  font-size: 14px;
}
</style>