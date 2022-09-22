<template>
  <v-col cols="12" sm="3" lg="3" md="3" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle>Delivery</v-card-subtitle>
      <v-card-text class="justify-center">
        <v-progress-circular
          indeterminate
          color="primary"
          v-if="deliveryLoading"
        ></v-progress-circular>
        <h3>{{ notifierDelivery }}</h3>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "NotifierDelivery",
  props: {
    uuid: String,
  },

  data: () => ({
    notifierDelivery: null,
    deliveryLoading: false,
  }),

  created() {
    this.getNotifierDelivery();
  },

  watch: {
    uuid() {
      this.getNotifierDelivery();
    },
  },

  methods: {
    getNotifierDelivery() {
      this.deliveryLoading = true;
      this.$http
        .get(`/api/v1/notifiers/${this.uuid}/delivery/`)
        .then((result) => {
          if (result.status === 200) {
            this.notifierDelivery = result.data.delivery;
          } else {
            this.notifierDelivery = "Failed";
          }
        })
        .catch(() => {
          this.notifierDelivery = "Failed";
        })
        .finally(() => {
          this.deliveryLoading = false;
        });
    },
  },
};
</script>

<style>
</style>