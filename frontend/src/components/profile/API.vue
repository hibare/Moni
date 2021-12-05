<template>
  <v-container fluid class="pt-8">
    <v-row>
      <v-col cols="12">
        <v-card elevation="1" color="transparent">
          <v-card-title>
            <h5><v-icon>mdi-api</v-icon> API Token</h5>
            <v-spacer></v-spacer>
            <v-tooltip top v-if="apiKey">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  x-small
                  v-bind="attrs"
                  v-on="on"
                  color="green darken-1"
                  :loading="tokenLoader"
                  :disabled="tokenLoader"
                  @click="generateToken"
                >
                  <v-icon>mdi-reload</v-icon>
                </v-btn>
              </template>
              <span>Regenerate</span>
            </v-tooltip>

            <v-tooltip top v-if="apiKey">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  x-small
                  v-bind="attrs"
                  v-on="on"
                  color="pink darken-1"
                  class="mx-5"
                  @click="openDeleteTokenDialog"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span>Delete Token</span>
            </v-tooltip>
          </v-card-title>
          <v-card-text>
            <loader v-if="tokenLoader" />
            <div v-else-if="apiKey === null">
              <p>No token found</p>
              <v-btn
                small
                class="text-capitalize"
                color="blue darken-3"
                @click="generateToken"
                :loading="tokenGenerateLoader"
                :disabled="tokenGenerateLoader"
                >Generate</v-btn
              >
            </div>
            <v-text-field
              dense
              readonly
              label=""
              filled
              :value="apiKey"
              :append-icon="showToken ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showToken ? 'text' : 'password'"
              @click:append="showToken = !showToken"
              class="token"
              v-else
            ></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Delete token -->
    <v-dialog persistent v-model="tokenDeleteDialog" width="500">
      <v-card color="secondary">
        <v-card-title>
          <span class="text-h5"> <v-icon>mdi-delete</v-icon> Delete Token</span>
          <v-spacer></v-spacer>
          <v-btn icon small @click="closeDeleteTokenDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="justify-center py-10">
          Do you want to delete token?
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="pink darken-1"
            block
            depressed
            outlined
            class="text-capitalize"
            :disabled="tokenDeleteLoader"
            :loading="tokenDeleteLoader"
            @click="deleteToken"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ./Delete token -->
  </v-container>
</template>

<script>
import Loader from "../Loader.vue";

export default {
  components: { Loader },
  name: "API",

  data: () => ({
    apiKey: null,
    showToken: false,

    tokenLoader: true,
    tokenDeleteLoader: false,
    tokenGenerateLoader: false,

    tokenDeleteDialog: false,
  }),

  created() {
    this.getToken();
  },

  methods: {
    getToken() {
      this.tokenLoader = true;
      this.$http
        .get(`/api/v1/accounts/token/`)
        .then((result) => {
          if (result.status === 200) {
            this.apiKey = result.data.token;
          }
        })
        .catch(() => {})
        .finally(() => {
          this.tokenLoader = false;
        });
    },

    generateToken() {
      this.tokenGenerateLoader = true;
      this.$http
        .put(`/api/v1/accounts/token/`)
        .then((result) => {
          if (result.status === 200) {
            this.apiKey = result.data.token;
          }
        })
        .catch(() => {})
        .finally(() => {
          this.tokenGenerateLoader = false;
        });
    },

    deleteToken() {
      this.tokenDeleteLoader = true;
      this.$http
        .delete(`/api/v1/accounts/token/`)
        .then((result) => {
          if (result.status === 200) {
            this.apiKey = null;
            this.closeDeleteTokenDialog();
          }
        })
        .catch(() => {})
        .finally(() => {
          this.tokenDeleteLoader = false;
        });
    },

    openDeleteTokenDialog() {
      this.tokenDeleteDialog = true;
    },
    closeDeleteTokenDialog() {
      this.tokenDeleteDialog = false;
    },
  },
};
</script>

<style scoped>
.token {
  font-size: 14px;
}
</style>