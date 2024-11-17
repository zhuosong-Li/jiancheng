import { ref } from 'vue';
import axios from 'axios';

let apiBaseUrl = '';
fetch('/frontend_config.json')
.then((response) => response.json())
.then((config) => {
    apiBaseUrl = config.api_base_url;
})

export default function () {
    // 放进来是为了独立数据，防止因为响应式特性造成数据污染
    let currentPage = ref(1);
    let currentPageSize = ref(10);
    let currentTotalRows = ref(0);
    let currentTableData = ref([]);
    let routeMsg = '';

    async function getTableData(value, route) {
        const params = {
            page: currentPage.value,
            pageSize: currentPageSize.value,
            id: value || ''
        };
        routeMsg = route;
        const response = await axios.get(
            `${apiBaseUrl}/${route}`,
            { params }
        );
        currentTableData.value = response.data.result;
        currentTotalRows.value = response.data.total;
    }

    function chageCurrentPageSize(val) {
        currentPageSize.value = val;
        getTableData('', routeMsg);
    }

    function changeCurrentPage(val) {
        currentPage.value = val;
        getTableData('', routeMsg);
    }

    return {
        currentPage,
        currentPageSize,
        currentTotalRows,
        currentTableData,
        getTableData,
        chageCurrentPageSize,
        changeCurrentPage
    };
}
