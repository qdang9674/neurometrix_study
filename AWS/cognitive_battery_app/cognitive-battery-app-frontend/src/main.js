import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router';
import store from './store/store';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import './styles/global.css';
import './styles/background.scss';

document.addEventListener('DOMContentLoaded', () => {
    const interBubble = document.querySelector('.interactive');
    let curX = 0;
    let curY = 0;
    let tgX = 0;
    let tgY = 0;

    function move() {
        if (store.state.currentTask != 'Baseline'){
            curX += (tgX - curX) / 20;
            curY += (tgY - curY) / 20;
        }

        interBubble.style.transform = `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`;
        requestAnimationFrame(() => {
            move();
        });
    }

    window.addEventListener('mousemove', (event) => {
        tgX = event.clientX;
        tgY = event.clientY;
    });

    move();
});

const app = createApp(App);
app.use(router);
app.use(store);
app.use(ElementPlus);
app.mount('#app');
