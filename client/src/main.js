// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import moment from 'moment-timezone';
import VueMoment from 'vue-moment';

import Vue from 'vue';
import App from './App';
import router from './router';

moment.locale('ja');
moment().tz('Asia/Tokyo').format();

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(VueMoment);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
