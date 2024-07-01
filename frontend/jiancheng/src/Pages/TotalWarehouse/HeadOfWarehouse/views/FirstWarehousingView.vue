<template>
    <el-container :direction="vertical">
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main style="overflow-x: hidden;">
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">一次采购入库</el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <span style="font-weight: bold; font-size: larger;">订单信息：</span>
                    <Arrow :status="11"></Arrow>
                    <el-descriptions title="" :column="2">

                        <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间">{{ testOrderData.createTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                        <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item>
                        <el-descriptions-item label="订单状态">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                    </el-descriptions>
                </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :span="24" :offset="0">
                    <el-table :data="testTableData" border style="height: 400px;">
                        <el-table-column prop="inheritId" label="工厂型号"></el-table-column>
                        <el-table-column prop="customerId" label="客户型号"></el-table-column>
                        <el-table-column label="鞋图">
                            <template #default="scope">
                                <el-image :src="scope.row.image" style="width: 150px; height: 100px"
                                    fit="fill"></el-image>

                            </template>
                        </el-table-column>
                        <el-table-column prop="Status" label="状态"></el-table-column>
                        <el-table-column label="操作"> <template #default="scope">
                                <div v-if="scope.row.Status === '部分未入库'">
                                    <el-button type="primary" @click="handleGenerate(scope.row)">入库</el-button>
                                    <el-button type="success" @click="openPreviewDialog(scope.row)">查看入库情况</el-button>
                                </div>
                                <div v-else-if="scope.row.Status === '已全部入库'">
                                    <el-button type="success" @click="openPreviewDialog(scope.row)">查看入库情况</el-button>
                                    <el-button type="warning" @click="handleConfirm(scope.row)">确认通知生产</el-button>
                                </div>
                            </template></el-table-column>
                    </el-table></el-col>
            </el-row>
            <el-dialog title="一次入库 K2402121116202024061101F" v-model="createVis" width="90%"
                @close="handleGenerateClose">
                <el-descriptions title="订单信息" :column="2">
                    <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                    <el-descriptions-item label="订单创建时间">{{ testOrderData.createTime }}</el-descriptions-item>
                    <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                    <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                    <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item>
                    <el-descriptions-item label="订单状态">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                    <el-descriptions-item label="采购订单编号">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                </el-descriptions>
                <el-table :data="bomTestData" border style="height: 400px;">
                    <el-table-column prop="partName" label="部件名称" />
                    <el-table-column prop="color" label="颜色" />
                    <el-table-column prop="materialName" label="材料名称" width="200" />
                    <el-table-column prop="unit" label="单位" width="60" />
                    <el-table-column prop="unitUsage" label="单位用量" />
                    <el-table-column prop="approvedUsage" label="核定用量" />
                    <el-table-column prop="purchaseAmount" label="采购数量"></el-table-column>
                    <el-table-column prop="realAmount" label="实际入库量"></el-table-column>
                    <el-table-column prop="realUnitPrice" label="入库单价"></el-table-column>
                    <el-table-column prop="realTotalPrice" label="入库总价"></el-table-column>
                    <el-table-column prop="factoryName" label="工厂名称"></el-table-column>
                    <el-table-column prop="comment" label="备注" />
                    <el-table-column prop="Status" label="状态" />
                    <el-table-column label="操作">
                        <template #default="scope">
                            <el-button type="primary" size="default" @click="handleMaterialInputOpen"
                                :disabled="scope.row.Status == '已入库'">入库</el-button>
                        </template>

                    </el-table-column>
                </el-table>

                <template #footer>
                    <span>
                        <el-button @click="handleGenerateClose">取消</el-button>
                        <el-button type="primary" @click="">保存</el-button>
                    </span>
                </template>
            </el-dialog>
            <el-dialog title="材料入库信息填写" v-model="isMaterialInput" width="30%">
                <div style="white-space: nowarp;">请输入实际入库数量：<el-input v-model="realAmountInput" placeholder=""
                        size="default" clearable @change=""></el-input></div>
                <div style="white-space: nowarp;">请输入实际入库单价：<el-input v-model="realUnitPriceInput" placeholder=""
                        size="default" clearable @change=""></el-input></div>
                <div style="white-space: nowarp;">实际入库总价：{{ realAmountInput * realUnitPriceInput }}</div>
                <template #footer>
                    <span>
                        <el-button @click="">Cancel</el-button>
                        <el-button type="primary" @click="">OK</el-button>
                    </span>
                </template>
            </el-dialog>

            <el-dialog title="预览采购订单 K2402121116202024061101F" v-model="isPreviewDialogVisible" width="90%">
                <el-descriptions title="订单信息" :column="2">
                    <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                </el-descriptions>
                <div style="height: 500px; overflow-y: scroll; overflow-x: hidden">
                    <el-row :gutter="20"
                        style="margin-bottom: 20px;">
                        <el-col :span="23">
                            <el-table :data="bomTestData" border style="width: 100%">
                                <el-table-column prop="partName" label="部件名称" />
                                <el-table-column prop="color" label="颜色" />
                                <el-table-column prop="materialName" label="材料名称" width="200" />
                                <el-table-column prop="unit" label="单位" width="60" />
                                <el-table-column prop="unitUsage" label="单位用量" />
                                <el-table-column prop="approvedUsage" label="核定用量" />
                                <el-table-column prop="purchaseAmount" label="采购数量"></el-table-column>
                                <el-table-column prop="realAmount" label="实际入库量"></el-table-column>
                                <el-table-column prop="realUnitPrice" label="入库单价"></el-table-column>
                                <el-table-column prop="realTotalPrice" label="入库总价"></el-table-column>
                                <el-table-column prop="factoryName" label="工厂名称"></el-table-column>
                                <el-table-column prop="comment" label="备注" />
                                <el-table-column prop="Status" label="状态" />
                            </el-table>
                        </el-col>
                    </el-row>
                </div>
                <template #footer>
                    <span>
                        <el-button type="primary" @click="closePreviewDialog">确认</el-button>
                    </span>
                </template>
            </el-dialog>







            <!-- Main content -->
        </el-main>

    </el-container>

</template>

<script>
import AllHeader from '@/components/AllHeader.vue';
import Arrow from '@/components/OrderArrowView.vue'
export default {
    props: ['orderId'],
    components: {
        AllHeader,
        Arrow
    },
    data() {
        return {
            isMaterialInput: false,
            createVis: false,
            realAmountInput: 0,
            realUnitPriceInput: 0.00,
            realTotalPriceInput: 0.00,
            testOrderData: {
                orderId: "123456",
                createTime: "2024-06-11",
                prevTime: "2024-06-11 12:00:00",
                prevDepart: "物控部",
                prevUser: "XXX",
                orderrStatus: '未完成'
            },
            testTableData: [{
                inheritId: "0E20620",
                customerId: "VRA-1020",
                image: "/src/components/images/testShoe1.png",
                Status: "部分未入库"
            },
            {
                inheritId: "0E20620",
                customerId: "VRA-1020",
                image: "/src/components/images/testShoe1.png",
                Status: "部分未入库"
            },
            {
                inheritId: "0E20620",
                customerId: "VRA-1020",
                image: "/src/components/images/testShoe1.png",
                Status: "已全部入库"
            },],
            bomTestData: [{
                partName: "鞋面",
                color: "黑色",
                materialName: "黑色超软镜面PU",
                unit: "米",
                unitUsage: 10.35,
                approvedUsage: 186,
                purchaseAmount: 200,
                realAmount: 220,
                realUnitPrice: null,
                realTotalPrice: null,
                factoryName: "一一鞋材",
                Status: "未入库",
                comment: ""
            },
            {
                partName: "鞋面",
                color: "黑色",
                materialName: "黑色超软镜面PU",
                unit: "米",
                unitUsage: 10.35,
                approvedUsage: 186,
                purchaseAmount: 200,
                realAmount: 220,
                realUnitPrice: 5.00,
                realTotalPrice: 1100.00,
                factoryName: "一一鞋材",
                Status: "已入库",
                comment: ""
            }],
            originalBomTestData: [],
            factoryOptions: [
                { materialName: '黑色超软镜面PU', factoryName: '一一鞋材' },
                { materialName: '黑色超软镜面PU', factoryName: '深源皮革' },
                { materialName: '黑色超软镜面PU', factoryName: '嘉泰皮革' },
                // Add more options here
            ],
            purchaseTestData: [
                {
                    factoryName: '一一鞋材', data: [{ num: 1, materialName: '黑色超软镜面PU', unit: '米', amount: '200', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '白色超软镜面PU', unit: '米', amount: '250', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '蓝色超软镜面PU', unit: '米', amount: '140', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" }]
                },
                {
                    factoryName: '深源皮革', data: [{ num: 1, materialName: '黑色超软镜面PU', unit: '米', amount: '200', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '白色超软镜面PU', unit: '米', amount: '250', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '蓝色超软镜面PU', unit: '米', amount: '140', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" }]
                },
                {
                    factoryName: '嘉泰皮革', data: [{ num: 1, materialName: '黑色超软镜面PU', unit: '米', amount: '200', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '白色超软镜面PU', unit: '米', amount: '250', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '蓝色超软镜面PU', unit: '米', amount: '140', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" }]
                },
                {
                    factoryName: '一一皮革', data: [{ num: 1, materialName: '黑色超软镜面PU', unit: '米', amount: '200', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '白色超软镜面PU', unit: '米', amount: '250', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
                    { num: 1, materialName: '蓝色超软镜面PU', unit: '米', amount: '140', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" }]
                },
            ],
            isPreviewDialogVisible: false,
            selectedFile: null
        }
    },
    methods: {
        handleMaterialInputOpen() {
            this.isMaterialInput = true

        },
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
        closePreviewDialog() {
            this.isPreviewDialogVisible = false
        },
    }
}
</script>

<style scoped>
/* Add your styles here */
</style>