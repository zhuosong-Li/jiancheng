import { ref,reactive, watch, getCurrentInstance } from 'vue'
import axios from 'axios'

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
    let materialSpecification = ref('')
    let supplierName = ref('')

    let params = reactive({
            'currentPage': currentPage.value,
            'currentPageSize': currentPageSize.value,
            'orderRid': orderRIdSearch.value,
            'currentTotalRows': currentTotalRows.value,
            'type': type.value,
            'route': route.value,
            'materialName': materialName.value,
            'materialModel': materialModel.value,
            'materialSpecification': materialSpecification.value,
            'supplierName': supplierName.value
        });

    async function getTableData() {
        if (params.type === 'GET') {
            const response = await axios.get(`${params.route}`, { params })
            currentTableData.value = response.data
            // currentTotalRows.value = response.data.total
        }
        if (params.type === 'POST') {
            await axios.post(`${route}`, { params })
        }
    }

    function chageCurrentPageSize(val) {
        params.currentPageSize = val
        currentPageSize.value = val
    }

    function changeCurrentPage(val) {
        params.currentPage = val
        currentPage.value = val
    }

    function updataParams(key, value){
        if (key === 'materialData') {
            Object.assign(params,value);
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
