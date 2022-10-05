import '@mdi/font/css/materialdesignicons.css' 
import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        themes: {
            light: {
                primary: '#1976D2',
                secondary: '#424242',
                accent: '#82B1FF',
                error: '#FF5252',
                info: '#2196F3',
                success: '#4CAF50',
                warning: '#FFC107',
            },
            dark: {
                primary: '#1bcbf2',
                secondary: '#112240',
                accent: '#8c9eff',
                error: '#FF3131',
                background: '#18293d'
            }
        },
        options: {
            customProperties: true
        },
    },
    icons: {
        iconfont: 'mdi',
    },
});
