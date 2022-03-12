<template>
  <v-app>
    <Header />
    <v-main>
      <v-snackbar
        v-model="snackbar.status"
        :timeout="snackbar.timeout"
        :color="snackbar.color"
        absolute
        top
        right
        elevation="5"
        transition="scroll-x-transition"
      >
        {{ snackbar.message }}
        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            icon
            v-bind="attrs"
            @click="snackbar.status = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </template>
      </v-snackbar>
      <router-view @showSnackbar="showSnackbarEvent" />
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import { EventBus } from "@/events/eventBus";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "App",

  components: {
    Footer,
    Header,
  },

  data: () => ({
    snackbar: {
      status: false,
      message: null,
      color: null,
      timeout: 5000,
    },
    publicPath: process.env.BASE_URL,
  }),

  created() {
    EventBus.$on("showSnackbar", this.showSnackbarEvent);
    this.setGitData();
  },

  watch: {
    $route: {
      immediate: true,
      handler(to) {
        if (to.meta.title) {
          document.title = to.meta.title + " - " + this.getAppName();
        } else {
          document.title = this.getAppName();
        }
      },
    },
  },

  methods: {
    showSnackbarEvent(data) {
      var colors = {
        success: "green",
        failure: "pink darken-1",
        warning: "lime darken-2",
      };
      this.snackbar.status = true;
      this.snackbar.message = data.message;
      this.snackbar.color = colors[data.status];
    },
  },
};
</script>

<style >
#app {
  background-color: var(--v-background-base);
}

.icon-cursor {
  cursor: pointer;
}

@font-face {
  font-family: "Merienda-Regular";
  src: local("Merienda"),
    url(./assets/fonts/Merienda/Merienda-Regular.ttf) format("truetype");
}
@font-face {
  font-family: "Merienda-Bold";
  src: local("Merienda"),
    url(./assets/fonts/Merienda/Merienda-Bold.ttf) format("truetype");
}

.brand {
  text-decoration: none;
  color: inherit;
  font-family: Merienda-Bold;
}
</style>