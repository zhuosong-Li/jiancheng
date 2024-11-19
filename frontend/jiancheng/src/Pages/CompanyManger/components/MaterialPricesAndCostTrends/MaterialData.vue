<template>
    <div class="content">
        <el-row :gutter="20" style="margin-top: 20px; justify-content: space-between">
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                材料名称:
                <el-input v-model="materialName" placeholder="请输入材料名称" clearable />
            </el-col>
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                材料型号:
                <el-input v-model="materialModel" placeholder="请输入材料型号" clearable />
            </el-col>
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                材料规格:
                <el-input v-model="specifications" placeholder="请输入材料规格" clearable />
            </el-col>
            <el-col :span="4" :offset="0" style="white-space: nowrap">
                材料厂家:
                <el-input v-model="purchaseFactory" placeholder="请输入材料厂家" clearable />
            </el-col>
            <el-button type="primary" size="middle" @click="updateData()">查询</el-button>
            <el-button type="primary" size="middle" @click="" :icon="Download"></el-button>
        </el-row>
        <el-table
            :data="currentTableData"
            style="width: 100%; margin-bottom: 20px; height: 540px"
            row-key="id"
            border
            default-expand-all
        >
            <el-table-column>
                <el-table-column prop="materialType" label="材料类型" sortable />
                <el-table-column prop="materialName" label="材料名称" sortable />
                <el-table-column prop="materialModel" label="材料型号" sortable />
                <el-table-column prop="specifications" label="材料规格" sortable />
                <el-table-column prop="color" label="颜色" sortable />
                <el-table-column prop="purchaseFactory" label="采购厂家" sortable />
                <el-table-column prop="materialPrice" label="材料单价" sortable />
                <el-table-column prop="purchaseCount" label="采购数量" sortable />
                <el-table-column prop="purchaseCosts" label="采购成本" sortable />
                <el-table-column prop="newestDate" label="最新入库日期" sortable />
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button
                            link
                            type="primary"
                            size="small"
                            @click="
                                edit(
                                    'edit',
                                    scope.row.purchaseFactory +
                                        scope.row.materialName +
                                        scope.row.materialModel +
                                        scope.row.specifications,
                                    'add'
                                )
                            "
                        >
                            历史价格曲线
                        </el-button>
                    </template>
                </el-table-column>
            </el-table-column>
        </el-table>
        <el-row :gutter="20">
            <el-col :span="6" :offset="8">
                <el-pagination
                    @size-change="chageCurrentPageSize"
                    @current-change="changeCurrentPage"
                    :current-page="currentPage"
                    :page-sizes="[10, 20, 30, 40]"
                    :page-size="currentPageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="currentTotalRows"
                />
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useTablePagination from '../../hooks/useTablePagination'
import { Download } from '@element-plus/icons-vue'

const edit = defineEmits(['edit'])

let materialName = ref('')
let materialModel = ref('')
let specifications = ref('')
let purchaseFactory = ref('')
const routeMsg = ''

const {
    currentPage,
    currentPageSize,
    currentTotalRows,
    currentTableData,
    getTableData,
    chageCurrentPageSize,
    changeCurrentPage,
    updataParams
} = useTablePagination()

onMounted(() => {
    currentTableData.value = [
        {
            newestDate: '2024-11-14',
            materialName: '皮革',
            materialPrice: '20',
            purchaseCount: '100',
            purchaseCosts: '2000',
            materialType: '类型1',
            materialModel: '型号1',
            specifications: '规格1',
            color: '棕色',
            purchaseFactory: '厂家1'
        },
        {
            newestDate: '2024-11-14',
            materialName: '麂皮',
            materialPrice: '18',
            purchaseCount: '50',
            purchaseCosts: '900',
            materialType: '类型2',
            materialModel: '型号2',
            specifications: '规格2',
            color: '黑色',
            purchaseFactory: '厂家2'
        }
    ]
    updataParams('route', routeMsg)
})

function updateData() {
    updataParams(
        'materialData',
        materialName.value +
            '>' +
            materialModel.value +
            '>' +
            specifications.value +
            '>' +
            purchaseFactory.value
    )
}
</script>

<style scoped>
.content {
    height: calc(100% - 40px);
    width: calc(100% - 40px);
}
</style>
