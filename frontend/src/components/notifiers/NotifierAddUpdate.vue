<template>
  <v-row justify="center">
    <v-dialog persistent v-model="notifierDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5"> <v-icon>mdi-bell</v-icon> Notifier</span>
          <v-spacer></v-spacer>
          <v-btn icon small color="red" @click="closeNotifierDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="mt-12">
          <v-form ref="addNotifier" lazy-validation>
            <v-row>
              <v-col cols="12">
                <v-autocomplete
                  label="Notifiers"
                  v-model="notifierItem.type"
                  :items="notifierTypes"
                  item-text="text"
                  item-value="value"
                  filled
                  clearable
                  dense
                >
                  <template v-slot:selection="data">
                    <v-avatar left>
                      <v-icon small>{{ data.item.icon }}</v-icon>
                    </v-avatar>
                    {{ data.item.text }}
                  </template>
                  <template v-slot:item="data">
                    <template>
                      <v-list-item-icon>
                        <v-icon small>{{ data.item.icon }}</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title
                          v-html="data.item.text"
                        ></v-list-item-title>
                      </v-list-item-content>
                    </template>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="Title*"
                  v-model="notifierItem.title"
                  required
                  counter
                  maxlength="15"
                  :rules="titleRule"
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  label="Description"
                  clearable
                  clear-icon="mdi-close-circle"
                  rows="3"
                  row-height="10"
                  v-model="notifierItem.description"
                  dense
                ></v-textarea>
              </v-col>
              <v-col><small>*indicates required field</small> </v-col>
              <v-col>
                <v-btn
                  color="teal accent-4"
                  block
                  depressed
                  class="text-capitalize"
                  :disabled="notifierBtnLoader"
                  :loading="notifierBtnLoader"
                  @click="submitNotifier"
                  v-if="notifierItem.valid"
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
  </v-row>
</template>
<script>
import rulesMixin from "@/mixins/rulesMixin";
import notifiersMap from "@/components/notifiers/notifiers.js";

export default {
  name: "NotifierAddUpdate",

  mixins: [rulesMixin],

  props: {
    notifierDialog: {
      default: false,
    },
    notifier: {
      default: null,
    },
  },

  data: () => ({
    showFieldContent: false,

    notifierTypes: [],
    notifierItem: {
      title: "",
      description: "",
      type: "slack",
      valid: false,
    },

    // Button loader status flags
    notifierBtnLoader: false,
    editNotifierBtnLoader: false,
    deleteNotifierBtnLoader: false,
    testNotifierBtnLoader: false,
    fethNotiferLoader: false,
  }),

  created() {
    this.notifierTypes.push({ header: "Select a Notifier type" });
    for (let [key, value] of Object.entries(notifiersMap)) {
      this.notifierTypes.push({
        value: key,
        text: value.name,
        icon: value.icon,
      });
    }
  },

  watch: {
    "notifierItem.type": function (val) {
      console.log(val);
    },
  },

  methods: {
    openNotifierDialog() {},
    closeNotifierDialog() {
      this.$emit("update:notifierDialog", false);
    },
    submitNotifier() {},
    testNotifier() {},
  },
};
</script>
