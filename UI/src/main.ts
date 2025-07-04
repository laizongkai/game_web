import './assets/main.css'
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css';

const app = createApp(App)

app.use(router)
app.mount('#app')

// @ts-nocheck