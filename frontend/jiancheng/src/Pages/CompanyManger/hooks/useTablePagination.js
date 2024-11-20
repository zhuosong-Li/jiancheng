import { ref,reactive, watch, getCurrentInstance } from 'vue'
import axios from 'axios'

const $api_baseUrl = getCurrentInstance().appContext.config.globalProperties.$api_baseUrl

export default function () {
    // 放进来是为了独立数据，防止因为响应式特性造成数据污染
    let currentPage = ref(1)
    let currentPageSize = ref(10)
    let currentTotalRows = ref(0)
    let currentTableData = ref([])
    let type = ref('GET');
    let route = ref('');
    let orderRIdSearch = ref('');
    let materialName = ref('')
    let materialModel = ref('')
    let specifications = ref('')
    let purchaseFactory = ref('')

    let params = reactive({
            'page': currentPage.value,
            'pageSize': currentPageSize.value,
            'orderRId': orderRIdSearch.value,
            'currentTotalRows': currentTotalRows.value,
            'type': type.value,
            'route': route.value,
            'materialName': materialName.value,
            'materialModel': materialModel.value,
            'specifications': specifications.value,
            'purchaseFactory': purchaseFactory.value
        });

    async function getTableData() {
        if (params.type === 'GET') {
            const response = await axios.get(`${api_baseUrl}/${route}`, { params })
            currentTableData.value = response.data.result
            currentTotalRows.value = response.data.total
        }
        if (params.type === 'POST') {
            await axios.post(`${api_baseUrl}/${route}`, { params })
        }
    }

    function chageCurrentPageSize(val) {
        params.currentPageSize.value = val
        currentPageSize.value = val
    }

    function changeCurrentPage(val) {
        params.currentPage.value = val
        currentPage.value = val
    }

    function updataParams(key, value){
        if (key === 'materialData') {
            const updateVal = value.split('>');
            // params['materialName'] = updateVal[0];
            // params['materialModel'] = updateVal[1];
            // params['specifications'] = updateVal[2];
            // params['purchaseFactory'] = updateVal[3];
            params.$patch({
                'page': currentPage.value,
                'pageSize': currentPageSize.value,
                'orderRId': orderRIdSearch.value,
                'currentTotalRows': currentTotalRows.value,
                'type': type.value,
                'route': route.value,
                'materialName': updateVal[0],
                'materialModel': updateVal[1],
                'specifications': updateVal[2],
                'purchaseFactory': updateVal[3]
            });
        } else {
            params[key] = value;
        }
    }
    watch(params, () => {
        getTableData();
    });

    return {
        currentPage,
        currentPageSize,
        currentTotalRows,
        currentTableData,
        getTableData,
        chageCurrentPageSize,
        changeCurrentPage,
        updataParams
    }
}
