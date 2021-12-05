<template>
  <v-col cols="12" sm="3" lg="3" md="3" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle>
        <v-icon small>mdi-calendar</v-icon> Created On</v-card-subtitle
      >
      <v-card-text class="justify-center">
        <h3>
          {{ getPrettyDate(created) }}
        </h3>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import dateMixin from "@/mixins/dateMixin";

export default {
  name: "JobCreated",
  mixins: [dateMixin],
  props: {
    created: String,
  },
  data: () => ({}),
};
</script>

<style>
</style>