<template>
  <v-footer color="transparent" class="px-8">
    <v-row no-gutters>
      <v-col
        class="text-center font-weight-light"
        cols="12"
        sm="12"
        lg="12"
        md="12"
      >
        <small>&copy; {{ getCurrentYear() }} - {{ version }} </small>
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