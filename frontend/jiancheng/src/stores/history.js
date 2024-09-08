// src/stores/history.js
import { reactive } from 'vue';

const historyStore = reactive({
    visitedPages: [],
    addPage(page) {
        this.visitedPages.push(page);
    },
    goBack() {
        this.visitedPages.pop();
        return this.visitedPages[this.visitedPages.length - 1];
    },
});

export default historyStore;
