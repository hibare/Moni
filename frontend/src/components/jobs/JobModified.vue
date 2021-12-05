<template>
  <v-col cols="12" sm="3" lg="3" md="3" class="center">
    <v-card elevation="1" color="transparent">
      <v-card-subtitle
        ><v-icon small>mdi-calendar</v-icon> Modified On</v-card-subtitle
      >
      <v-card-text class="justify-center">
        <h3>
          {{ getPrettyDate(modified) }}
        </h3>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import dateMixin from "@/mixins/dateMixin";

export default {
  name: "JobModified",
  mixins: [dateMixin],
  props: {
    modified: String,
  },
  data: () => ({}),
};
</script>

<style>
</style>