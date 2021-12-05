<template>
  <v-footer color="transparent" class="px-8">
    <v-row no-gutters>
      <v-col
        class="text-center text-md-left text-xl-left font-weight-light"
        cols="12"
        sm="4"
        lg="4"
        md="4"
      >
        <small
          >Made with <v-icon small color="#f30093">mdi-heart</v-icon> &amp;
          Vuetify</small
        >
      </v-col>
      <v-col
        class="text-center font-weight-light"
        cols="12"
        sm="4"
        lg="4"
        md="4"
      >
        <small>&copy; {{ getCurrentYear() }} - Moni - {{ version }} </small>
      </v-col>
      <v-col
        class="text-center text-md-right text-xl-right font-weight-light"
        cols="12"
        sm="4"
        lg="4"
        md="4"
      >
        <v-btn
          icon
          class="font-weight-light"
          :href="getGitURL()"
          target="_blank"
        >
          <v-icon small>mdi-star</v-icon>
          <small>{{ getGitStars }}</small>
        </v-btn>
        <v-btn
          icon
          class="font-weight-light"
          :href="getGitURL()"
          target="_blank"
        >
          <v-icon small>mdi-git</v-icon>
          <small>{{ getGitForks }}</small>
        </v-btn>
        <!-- <v-btn icon :href="getGitURL()" target="_blank">
          <v-icon small>mdi-github</v-icon>
        </v-btn> -->
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",

  data: () => ({
    version: "",
  }),

  created() {
    this.getVersion();
  },

  methods: {
    getVersion() {
      this.$http
        .get(`/__version/`)
        .then((result) => {
          if (result.status === 200) {
            this.version = result.data.version;
          }
        })
        .catch(() => {})
        .finally(() => {});
    },
  },
};
</script>