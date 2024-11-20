import { ref, reactive, watch, getCurrentInstance } from 'vue'
import axios from 'axios'

export default function () {
    // 放进来是为了独立数据，防止因为响应式特性造成数据污染
    let currentPage = ref(1)
    let currentPageSize = ref(10)
    let currentTotalRows = ref(0)
    let currentTableData = ref([])
    let tableData = ref([])
    let type = ref('GET')
    let route = ref('')
    let orderRIdSearch = ref('')
    let materialName = ref('')
    let materialModel = ref('')
    let materialSpecification = ref('')
    let supplierName = ref('')
    let orderType = ref(0)

    let params = reactive({
        orderRid: orderRIdSearch.value,
        type: type.value,
        route: route.value,
        materialName: materialName.value,
        materialModel: materialModel.value,
        materialSpecification: materialSpecification.value,
        supplierName: supplierName.value,
        orderType: orderType.value
    })

    async function getTableData() {
        if (params.type === 'GET') {
            const response = await axios.get(`${params.route}`, { params })
            tableData.value = response.data
            currentTotalRows.value = response.data.length
            dataCut()
        }
        if (params.type === 'POST') {
            await axios.post(`${route}`, { params })
        }
    }

    function chageCurrentPageSize(val) {
        if (currentPageSize.value !== val) {
            currentPageSize.value = val
            dataCut()
        }
    }

    function changeCurrentPage(val) {
        if (currentPage.value !== val) {
            currentPage.value = val
            dataCut()
        }
    }

    function updataParams(key, value) {
        if (key === 'materialData' || key === 'orderStatus') {
            Object.assign(params, value)
        } else {
            params[key] = value
        }
    }
    watch(params, () => {
        getTableData()
    })

    function dataCut() {
        currentTableData.value = tableData.value.slice(
            (currentPage.value - 1) * currentPageSize.value,
            currentPageSize.value * currentPage.value
        )
    }

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
