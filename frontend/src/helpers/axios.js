import axios from 'axios';
import store from '@/store/modules/auth'
// import router from '@/router'
// import { EventBus } from '@/helpers/eventBus';


axios.interceptors.request.use(
    request => {
        const token = store.getters.getAccessToken;

        request.headers.Authorization = `Bearer ${token}`;

        return request;
    }, error => {
        return Promise.reject(error);
    }
);

axios.interceptors.response.use(
    response => {
        if (response.status === 200 || response.status === 201) {
            return Promise.resolve(response);
        } else {
            return Promise.reject(response);
        }
    }, error => {
        // if (error.response.status) {
        //     switch (error.response.status) {
        //         case 400:

        //             //do something
        //             break;

        //         case 401:
        //             EventBus.emit("showSnackbar", "error");
        //             break;
        //         case 403:
        //             router.replace({
        //                 path: "/login",
        //                 query: { redirect: router.currentRoute.fullPath }
        //             });
        //             break;
        //         case 404:
        //             alert('page not exist');
        //             break;
        //         case 502:
        //             setTimeout(() => {
        //                 router.replace({
        //                     path: "/login",
        //                     query: {
        //                         redirect: router.currentRoute.fullPath
        //                     }
        //                 });
        //             }, 1000);
        //     }
        // }
        return Promise.reject(error);
    }
);

export default axios;