import Vue from 'vue'
import axios from 'axios';

import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import globalMixin from "@/mixins/globalMixin";
import store from '@/store'
import router from '@/router'
import { EventBus } from '@/helpers/eventBus';

axios.interceptors.request.use(
  request => {
    const ignorePaths = ['/api/v1/jobs/status/']

    if (!ignorePaths.includes(request.url) && request.url.startsWith('/api/v1/')) {
      const token = store.getters['auth/getAccessToken'];
      request.headers.common["X-Access-Token"] = `JWT ${token}`;
    }

    return request;
  }, error => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(


  response => {
    if (response.status === 200 || response.status === 201 || response.status === 204) {
      return Promise.resolve(response);
    } else {
      return Promise.reject(response);
    }
  }, error => {

    if (error.response.status) {

      var data = {
        status: 'failure',
        message: 'Unknown Error'
      }

      switch (error.response.status) {
        case 400:
          data.status = 'failure'
          data.message = 'Bad request'
          EventBus.$emit("showSnackbar", data);
          break;

        case 401:
          data.status = 'failure'
          data.message = 'Unauthorised'
          EventBus.$emit("showSnackbar", data);
          break;

        case 403:
          data.status = 'failure'
          data.message = 'Forbidden'
          EventBus.$emit("showSnackbar", data);
          break;

        case 404:
          data.status = 'warning'
          data.message = 'Resource not found'
          // EventBus.$emit("showSnackbar", data);
          break;

        case 500:
          data.status = 'failure'
          data.message = 'Internal Server Error'
          EventBus.$emit("showSnackbar", data);
          break;

        case 501:
          data.status = 'failure'
          data.message = 'Not Implemented'
          EventBus.$emit("showSnackbar", data);
          break;

        case 502:
          data.status = 'failure'
          data.message = 'Bad Gateway'
          EventBus.$emit("showSnackbar", data);
          break;

        case 503:
          data.status = 'failure'
          data.message = 'Service Unavailable'
          EventBus.$emit("showSnackbar", data);
          break;

        case 504:
          data.status = 'failure'
          data.message = 'Gateway Timeout'
          EventBus.$emit("showSnackbar", data);
          break;

        default:
          data.status = 'failure'
          data.message = 'Unknown Error'
          EventBus.$emit("showSnackbar", data);
      }
    }
    return Promise.reject(error);
  }
);

Vue.prototype.$http = axios

Vue.config.productionTip = true

Vue.mixin(globalMixin);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
