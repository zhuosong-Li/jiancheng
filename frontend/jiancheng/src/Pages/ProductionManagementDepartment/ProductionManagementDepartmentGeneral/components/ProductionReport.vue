<template>
    <div class="production-report">
        <el-card>
            <el-tabs v-model="activeTab" @tab-click="handleTabClick">
                <el-tab-pane label="生产报表" name="productionAmount">
                    <el-row :gutter="20">
                        <el-col :span="2">日期范围</el-col>
                        <el-col :span="6">
                            <el-date-picker v-model="filters.productionAmount.dateRange" type="daterange"
                                value-format="YYYY-MM-DD" placeholder="Select Date" @change="getProductionSummary"
                                clearable />
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <production-table :data="productionSummaryData" :loading="loading"
                                report-type="productionAmount" />
                        </el-col>
                        <el-col :span="12">
                            <production-table :data="outsourceSummaryData" :loading="loading"
                                report-type="outsourceAmount" />
                        </el-col>
                    </el-row>
                </el-tab-pane>
            </el-tabs>
        </el-card>
    </div>
</template>

<script>
import { ref, reactive, onMounted, getCurrentInstance } from 'vue';
import {
    ElCard,
    ElTabs,
    ElTabPane,
    ElDatePicker,
    ElButton,
    ElMessage,
} from 'element-plus';
import ProductionTable from './ProductionTable.vue';
import axios from 'axios'
export default {
    name: 'ProductionReport',
    components: {
        ElCard,
        ElTabs,
        ElTabPane,
        ElDatePicker,
        ElButton,
        ProductionTable,
    },
    setup() {
        const activeTab = ref('productionAmount');
        const today = (new Date()).toISOString().split('T')[0]
        const filters = reactive({
            productionAmount: {
                dateRange: [today, today],
            },
        });

        const loading = ref(false)
        const productionSummaryData = ref([])
        const outsourceSummaryData = ref([])
        const proxy = getCurrentInstance()
        const apiBaseUrl = proxy.appContext.config.globalProperties.$apiBaseUrl

        const getProductionSummary = async () => {
            try {
                let params = { "startDate": filters.productionAmount.dateRange[0], "endDate": filters.productionAmount.dateRange[1] }
                let response = await axios.get(`${apiBaseUrl}/production/getselfproductionsummary`, { params })
                productionSummaryData.value = response.data
            }
            catch (error) {
                console.log(error)
                ElMessage.error(error.response.data.message)
            }
        }

        const getOutsourceSummary = async () => {
            try {
                let params = { "startDate": filters.productionAmount.dateRange[0], "endDate": filters.productionAmount.dateRange[1] }
                let response = await axios.get(`${apiBaseUrl}/production/getoutsourcesummary`, { params })
                outsourceSummaryData.value = response.data
            }
            catch (error) {
                console.log(error)
                ElMessage.error(error.response.data.message)
            }
        }

        const resetFilters = (reportType) => {
            filters[reportType].dateRange = null;
            if (reportType === 'productionAmount') {
                productionSummaryData.value = [];
            }
        };

        const handleTabClick = (tab) => {
            // Optionally, fetch data when tab changes
            // fetchData();
        };

        onMounted(() => {
            // Optionally, fetch initial data
            getProductionSummary()
            getOutsourceSummary()
        });

        return {
            activeTab,
            filters,
            loading,
            productionSummaryData,
            outsourceSummaryData,
            getProductionSummary,
            getOutsourceSummary,
            resetFilters,
            handleTabClick,
        };
    },
};
</script>

<style scoped>
.production-report {
    padding: 20px;
}

.no-data {
    text-align: center;
    margin-top: 20px;
    color: #999;
}

.tables-container {
    display: flex;
    justify-content: space-between;
    /* Adjust spacing between tables */
    gap: 16px;
    /* Optional: Adds space between tables */
}

.el-table {
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    /* Optional: Adds shadow effect */
    border-radius: 8px;
    /* Optional: Rounds corners */
}
</style>