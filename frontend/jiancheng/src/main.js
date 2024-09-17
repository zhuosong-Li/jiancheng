import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios';



const app = createApp(App)
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$setAxiosToken = function () {
  const token = localStorage.getItem('token'); // Get token from localStorage
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`; // Set the Authorization header globally
  } else {
    delete axios.defaults.headers.common['Authorization']; // Remove the Authorization header if no token is found
    router.push({ name: 'login' }); // Redirect to the login page
  }
};
const token = localStorage.getItem('token'); // Get token from localStorage
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`; // Set the Authorization header globally
} else {
  delete axios.defaults.headers.common['Authorization']; // Remove the Authorization header if no token is found
  router.push({ name: 'login' }); // Redirect to the login page
}
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn });
app.mount('#app')
