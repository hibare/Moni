import { createApp } from "vue";
import { createPinia } from "pinia";
import { Quasar, Notify } from "quasar";
import "@quasar/extras/fontawesome-v6/fontawesome-v6.css";
import "quasar/src/css/index.sass";
import piniaPluginPersistedState from "pinia-plugin-persistedstate";
import router from "./router";
import "./styles/index.scss";
import { resetStore } from "./utils/resetStore";

import App from "./App.vue";

const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPluginPersistedState);
pinia.use(resetStore);

app
  .use(Quasar, {
    plugins: {
      Notify,
    },
  })
  .use(router)
  .use(pinia)
  .mount("#app");
