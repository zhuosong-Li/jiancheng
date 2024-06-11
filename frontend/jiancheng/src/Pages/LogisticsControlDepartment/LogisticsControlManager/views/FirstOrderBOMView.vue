<template>
    <el-container :direction="vertical">
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main height="">
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">一次采购订单生成</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <el-descriptions title="订单信息" :column="2">
                        <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ testOrderData.createTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item>
                        <el-descriptions-item label="订单状态">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                    </el-descriptions></el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="24" :offset="0">
                    <el-table :data="testTableData" border style="height: 400px;">
                        <el-table-column prop="bomId" label="BOM单编号"></el-table-column>
                        <el-table-column prop="bomType" label="BOM类型"></el-table-column>
                        <el-table-column prop="bomType" label="BOM类型"></el-table-column>
                        <el-table-column prop="Status" label="状态"></el-table-column>
                        <el-table-column label="操作"> <template #default="scope">
                                <el-button v-if="scope.row.Status === '未生成采购订单'" type="primary"
                                    @click="handleGenerate(scope.row)">生成</el-button>
                                <el-button v-else-if="scope.row.Status === '已生成采购订单'" type="primary"
                                    @click="handleView(scope.row)">查看</el-button>
                                <div v-else-if="scope.row.Status === '已保存采购订单'">
                                    <el-button type="primary" @click="handleGenerate(scope.row)">编辑</el-button>
                                    <el-button type="success" @click="openPreviewDialog(scope.row)">预览</el-button>
                                    <el-button type="warning" @click="handleConfirm(scope.row)">确认下发</el-button>
                                </div>
                            </template></el-table-column>
                    </el-table></el-col>
            </el-row>
            <el-dialog title="采购订单 K2402121116202024061101F" v-model="createVis" width="90%"
                @close="handleGenerateClose">
                <el-descriptions title="订单信息" :column="2">
                    <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                    <el-descriptions-item label="订单创建时间">{{ testOrderData.createTime }}</el-descriptions-item>
                    <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                    <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                    <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item>
                    <el-descriptions-item label="订单状态">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                    <el-descriptions-item label="BOM编号">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                </el-descriptions>
                <el-table :data="bomTestData" border style="height: 400px;">
                    <el-table-column prop="partName" label="部件名称" />
                    <el-table-column prop="color" label="颜色" />
                    <el-table-column prop="materialName" label="材料名称" />
                    <el-table-column prop="unit" label="单位" />
                    <el-table-column prop="unitUsage" label="单位用量" />
                    <el-table-column prop="approvedUsage" label="核定用量" />
                    <el-table-column label="采购数量">
                        <template #default="scope">
                            <el-input-number v-model="scope.row.purchaseAmount" :min="0" />
                        </template>
                    </el-table-column>
                    <el-table-column label="工厂名称">
                        <template #default="scope">
                            <el-select v-model="scope.row.factoryName" placeholder="选择工厂">
                                <el-option v-for="factory in getFilteredFactoryOptions(scope.row.materialName)"
                                    :key="factory.factoryName" :label="factory.factoryName"
                                    :value="factory.factoryName" />
                            </el-select>
                        </template>
                    </el-table-column>
                    <el-table-column prop="internalModel" label="公司型号" />
                    <el-table-column prop="customerModel" label="客户型号" />
                </el-table>

                <template #footer>
                    <span>
                        <el-button @click="handleGenerateClose">取消</el-button>
                        <el-button type="primary" @click="">保存</el-button>
                    </span>
                </template>
            </el-dialog>

            <el-dialog
                title="预览采购订单 K2402121116202024061101F"
                v-model="isPreviewDialogVisible"
                width="90%">
                <el-descriptions title="订单信息" :column="2">
                    <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                </el-descriptions>
                <el-row :gutter="20">
                    <el-col :span="24" :offset="0"></el-col>
                </el-row>
                
                <template #footer>
                <span>
                    <el-button @click="">Cancel</el-button>
                    <el-button type="primary" @click="">OK</el-button>
                </span>
                </template>
            </el-dialog>
            






            <!-- Main content -->
        </el-main>

    </el-container>

</template>

<script>
import AllHeader from '@/components/AllHeader.vue';
export default {
    props: ['orderId'],
    components: {
        AllHeader,
    },
    data() {
        return {
            createVis: false,
            testOrderData: {
                orderId: "123456",
                createTime: "2024-06-11",
                prevTime: "2024-06-11 12:00:00",
                prevDepart: "技术部",
                prevUser: "XXX",
                orderrStatus: '未完成'
            },
            testTableData: [{
                bomId: "K24021211162020240611180001",
                bomType: "一次采购BOM",
                bomLink: "0E20620,0E20621",
                Status: "未生成采购订单"
            },
            {
                bomId: "K24021211162020240611180002",
                bomType: "一次采购BOM",
                bomLink: "0E20620,0E20621",
                Status: "已生成采购订单"
            },
            {
                bomId: "K24021211162020240611180001",
                bomType: "一次采购BOM",
                bomLink: "0E20620,0E20621",
                Status: "已保存采购订单"
            },],
            bomTestData: [{
                partName: "鞋面",
                color: "黑色",
                materialName: "黑色超软镜面PU",
                unit: "米",
                unitUsage: 10.35,
                approvedUsage: 186,
                purchaseAmount: 0,
                factoryName: "",
                internalModel: "0E202620",
                customerModel: "VRA-1020"
            }],
            originalBomTestData: [],
            factoryOptions: [
                { materialName: '黑色超软镜面PU', factoryName: '一一鞋材' },
                { materialName: '黑色超软镜面PU', factoryName: '深源皮革' },
                { materialName: '黑色超软镜面PU', factoryName: '嘉泰皮革' },
                // Add more options here
            ],
            purchaseTestData:[{
                
            }],
            isPreviewDialogVisible: false,
            selectedFile: null
        }
    },
    methods: {
        handleGenerate(row) {
            this.originalBomTestData = JSON.parse(JSON.stringify(this.bomTestData));
            this.createVis = true
        },
        handleGenerateClose() {
            this.bomTestData = JSON.parse(JSON.stringify(this.originalBomTestData)); // Restore original data
            this.createVis = false;
        },
        getFilteredFactoryOptions(materialName) {
            const filteredOptions = this.factoryOptions.filter(option => option.materialName === materialName);
            return [{ factoryName: '询价' }, ...filteredOptions];
        },
        openPreviewDialog() {
            // Replace this with the actual logic to get the file
            this.isPreviewDialogVisible = true;
        },
    }
}
</script>

<style scoped>
/* Add your styles here */
</style>