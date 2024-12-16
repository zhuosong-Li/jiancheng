<template>
    <el-table :data="data" style="width: 100%" v-loading="loading" element-loading-text="Loading..." border default-expand-all>
        <el-table-column type="expand" width="55">
            <template #default="meta">
                <el-table :data="meta.row.productionLines" border stripe style="width: 100%">
                    <el-table-column width="55"></el-table-column>
                    <el-table-column align="center" prop="productionLineName" label="车间线号" />
                    <el-table-column align="center" :label="productionAmountLabel" prop="productionLineAmount"/>
                </el-table>
            </template>
        </el-table-column>
        <el-table-column align="center" prop="team" label="车间"></el-table-column>
        <el-table-column align="center" prop="totalAmount" label="车间产量"></el-table-column>
    </el-table>
</template>

<script>
import { computed } from 'vue';
import { ElTable, ElTableColumn } from 'element-plus';

export default {
    name: 'ProductionTable',
    components: {
        ElTable,
        ElTableColumn,
    },
    props: {
        data: {
            type: Array,
            required: true,
        },
        loading: {
            type: Boolean,
            default: false,
        },
        reportType: {
            type: String,
            required: true, // 'productionAmount', 'monthly', 'yearly'
        },
    },
    setup(props) {
        const previousStockLabel = computed(() => {
            if (props.reportType === 'productionAmount') return '昨天库存';
            if (props.reportType === 'monthly') return "Previous Month's Stock";
            if (props.reportType === 'yearly') return "Previous Year's Stock";
            return 'Previous Stock';
        });

        const productionAmountLabel = computed(() => {
            if (props.reportType === 'productionAmount') return '日期范围产量';
            if (props.reportType === 'monthly') return "This Month's Production Amount";
            if (props.reportType === 'yearly') return "This Year's Production Amount";
            return 'Production Amount';
        });

        const todayStockLabel = computed(() => {
            if (props.reportType === 'productionAmount') return 'Today Stock';
            if (props.reportType === 'monthly') return "This Month's Stock";
            if (props.reportType === 'yearly') return "This Year's Stock";
            return 'Stock';
        });

        const getSummaries = (SummaryMethodProps) => {
            console.log(SummaryMethodProps)
        }

        return {
            previousStockLabel,
            productionAmountLabel,
            todayStockLabel,
            getSummaries
        };
    },
};
</script>

<style scoped>
/* Add any specific styles if needed */
</style>