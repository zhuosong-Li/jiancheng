<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">固定资产/耗材采购订单生成</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="12" :offset="0"><el-button-group>
                <el-button type="primary" size="default" @click="openCreateDialog">新建耗材/固定资产采购订单</el-button>
                <el-button type="primary" size="default" @click="">以过去订单为模板新建</el-button>
            </el-button-group>
        </el-col>
        <el-col :span="4" :offset="8"><el-button type="warning" size="large" @click="openUnsubmitDialog">待提交订单 {{
                finishedNum }}</el-button>
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="6" :offset="0">
            <div style="display: flex; align-items: center; white-space: nowrap;">订单编号查询：<el-input v-model="orderSearch"
                    placeholder="" size="default" :suffix-icon="Search" clearable @input="tableWholeFilter"></el-input>
            </div>
        </el-col>
        <el-col :span="6" :offset="0">
            <div style="display: flex; align-items: center; white-space: nowrap;">耗材类型查询：<el-input
                    v-model="assetsTypeSearch" placeholder="" size="default" :suffix-icon="Search" clearable
                    @input="tableWholeFilter"></el-input></div>
        </el-col>
        <el-col :span="6" :offset="0">
            <div style="display: flex; align-items: center; white-space: nowrap;">采购类型查询： <el-select
                    v-model="isPurchaseOrderFilter" value-key="" placeholder="" clearable filterable
                    @change="tableWholeFilter">
                    <el-option v-for="item in isPurchaseOrderOptions" :key="item.value" :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </div>
        </el-col>

    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24" :offset="0">
            <el-table :data="materialPurchaseFilterData" border style="height: 600px;" ref="singleSelectTable"
                @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="purchaseId" label="采购订单编号"></el-table-column>
                <el-table-column prop="purchaseCreateDate" label="采购下发日期"></el-table-column>
                <el-table-column prop="purchaseType" label="采购物品类型"></el-table-column>
                <el-table-column prop="isPurchaseOrder" label="随订单采购/独立采购"></el-table-column>
                <el-table-column prop="purchaseOrderId" label="订单编号"></el-table-column>
                <el-table-column label="操作"> <template #default="scope">
                        <el-button type="primary" @click="openPreviewDialog(scope.row)">查看</el-button>
                    </template></el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <!--未提交订单对话框-->
    <el-dialog title="未提交订单一览" v-model="unsubmitVis" width="90%">
        <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="24" :offset="0">
                <el-table :data="materialPurchaseFilterData" border style="height: 600px;">
                    <el-table-column prop="purchaseId" label="采购订单编号"></el-table-column>
                    <el-table-column prop="purchaseCreateDate" label="采购下发日期"></el-table-column>
                    <el-table-column prop="purchaseType" label="采购物品类型"></el-table-column>
                    <el-table-column prop="isPurchaseOrder" label="随订单采购/独立采购"></el-table-column>
                    <el-table-column prop="purchaseOrderId" label="订单编号"></el-table-column>
                    <el-table-column label="操作"> <template #default="scope">
                            <el-button type="primary" @click="openPreviewDialog(scope.row)">查看</el-button>
                            <el-button type="primary" @click="openEditDialog(scope.row)">编辑</el-button>
                            <el-button type="primary" @click="">下发</el-button>
                        </template></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="">Cancel</el-button>
                <el-button type="primary" @click="">OK</el-button>
            </span>
        </template>
    </el-dialog>

    <!--创建新采购订单/过往订单创建-->
    <el-dialog title="耗材/固定资产采购订单 K2402121116202024061101F" v-model="createVis" width="90%"
        @close="handleGenerateClose">
        <el-table :data="newAssetPurchaseData" border>
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column prop="warehouseType" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column label="采购数量">
                <template #default="scope">
                    <el-input-number v-model="scope.row.purchaseAmount" :min="0" size="small" />
                </template>
            </el-table-column>
            <el-table-column prop="factoryName" label="工厂名称">
            </el-table-column>
            <el-table-column label="随订单采购/独立采购">
                <template #default="scope">
                    <el-select v-model="scope.row.isPurchaseOrder" placeholder="" filterable>
                        <el-option v-for="item in isPurchaseOrderOptions" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="订单编号">
                <template #default="scope">
                    <el-input v-model="scope.row.purchaseOrderId" placeholder="" size="default" clearable
                        :disabled="scope.row.isPurchaseOrder === '独立采购'"></el-input>
                </template>
            </el-table-column>
            <el-table-column label="备注">
                <template #default="scope">
                    <el-input v-model="scope.row.comment" placeholder="" size="default" clearable></el-input>
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" size="default" @click="openNewMaterialDialog">添加新材料</el-button>


        <template #footer>
            <span>
                <el-button @click="handleGenerateClose">取消</el-button>
                <el-button type="primary" @click="">保存</el-button>
            </span>
        </template>
    </el-dialog>
    <!--采购材料对话框-->
    <el-dialog title="添加新采购材料" v-model="newMaterialVis" width="60%">
        <el-row :gutter="20">
            <el-col :span="6" :offset="0">
                <div style="display: flex; align-items: center; white-space: nowrap;">材料查询：<el-input
                        v-model="materialSearch" placeholder="" size="default" :suffix-icon="Search" clearable
                        @input="materialTableWholeFilter"></el-input>
                </div>
            </el-col>
            <el-col :span="6" :offset="0">
                <div style="display: flex; align-items: center; white-space: nowrap;">工厂名查询：<el-input
                        v-model="factorySearch" placeholder="" size="default" :suffix-icon="Search" clearable
                        @input="materialTableWholeFilter"></el-input>
                </div>
            </el-col>
        </el-row>
        <el-table :data="assetFilterTable" border ref="materialSelectTable"
            @selection-change="handleMaterialSelectionChange" style="max-height: 400px;">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column prop="warehouseName" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column prop="factoryName" label="工厂名称" />
        </el-table>


        <template #footer>
            <span>
                <el-button @click="handleGenerateClose">取消</el-button>
                <el-button type="primary" @click="confirmNewMaterialAdd">保存</el-button>
            </span>
        </template>
    </el-dialog>
    <!--采购订单预览-->
    <el-dialog title="耗材/固定资产采购订单 K2402121116202024061101F 预览" v-model="purchaseOrderVis" width="90%">
        <div style="height: 500px; overflow-y: scroll; overflow-x: hidden">
            <el-row v-for="factory in purchaseTestData" :key="factory.factoryName" :gutter="20"
                style="margin-bottom: 20px;">
                <el-col :span="23">
                    <h3>{{ factory.factoryName }}</h3>
                    <el-table :data="factory.data" border style="width: 100%">
                        <el-table-column prop="num" label="编号" />
                        <el-table-column prop="materialName" label="材料名称" />
                        <el-table-column prop="warehouseName" label="所属仓库" />
                        <el-table-column prop="unit" label="单位" />
                        <el-table-column prop="amount" label="数量" />
                        <el-table-column prop="purchaseOrderId" label="订单编号" />
                        
                        <el-table-column prop="comment" label="备注" />
                    </el-table>
                </el-col>
            </el-row>
        </div>
        <template #footer>
            <span>
                <el-button @click="">Cancel</el-button>
                <el-button type="primary" @click="">OK</el-button>
            </span>
        </template>
    </el-dialog>


</template>
<script>
import { Search } from '@element-plus/icons-vue';
import { markRaw } from 'vue';
import { ElMessageBox } from 'element-plus'
export default {
    data() {
        return {
            finishedNum: 1,
            materialSearch: "",
            factorySearch: "",
            unsubmitVis: false,
            createVis: false,
            newMaterialVis: false,
            purchaseOrderVis: false,
            orderSearch: "",
            assetsTypeSearch: "",
            isPurchaseOrderFilter: "",
            addAssetName: '',
            isPurchaseOrderOptions: [{ value: "随订单采购", label: "随订单采购" }, { value: "独立采购", label: "独立采购" }],
            assetTable: [{ materialName: "胶水", warehouseName: "化工库", unit: "桶", factoryName: "询价" },
            { materialName: "染料", warehouseName: "化工库", unit: "桶", factoryName: "询价" },
            { materialName: "森达G8C307新", warehouseName: "楦头库", unit: "个", factoryName: "森达" },
            { materialName: "森达E69138", warehouseName: "楦头库", unit: "个", factoryName: "森达" },
            ],
            assetFilterTable: [],
            Search: markRaw(Search),
            materialPurchaseTestData: [{
                purchaseId: 'K2402121116202024061101A',
                purchaseCreateDate: '2024-06-12',
                purchaseType: '化工类, 工具类',
                isPurchaseOrder: '随订单采购',
                purchaseOrderId: 'W24-01-2111620'
            },
            {
                purchaseId: 'K2402121116202024061102A',
                purchaseCreateDate: '2024-06-12',
                purchaseType: '化工类, 工具类',
                isPurchaseOrder: '随订单采购',
                purchaseOrderId: 'W24-01-2111620'
            }],
            materialPurchaseFilterData: [],
            selectedRow: null,
            materialSelectRow: null,
            newAssetPurchaseData: [],
            factoryOptions: [
                { materialName: '黑色超软镜面PU', factoryName: '一一鞋材' },
                { materialName: '黑色超软镜面PU', factoryName: '深源皮革' },
                { materialName: '黑色超软镜面PU', factoryName: '嘉泰皮革' },
                // Add more options here
            ],
            purchaseTestData: [
                {
                    factoryName: '询价', data: [{ num: 1, materialName: '黑色超软镜面PU', unit: '米', amount: '200', customerId: 'K24', internalModel: '0E202620', customerModel: "VRA-1020", comment: "" },
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
        }
    },
    mounted() {
        this.materialPurchaseFilterData = this.materialPurchaseTestData
    },
    methods: {
        handleSelectionChange(selection) {
            if (selection.length > 1) {
                // Ensure only one row is selected
                this.$refs.singleSelectTable.clearSelection();
                this.$refs.singleSelectTable.toggleRowSelection(selection[selection.length - 1], true);
            } else {
                this.selectedRow = selection[0];
            }
            console.log(this.selectedRow)
        },
        handleMaterialSelectionChange(selection) {
            if (selection.length > 1) {
                // Ensure only one row is selected
                this.$refs.materialSelectTable.clearSelection();
                this.$refs.materialSelectTable.toggleRowSelection(selection[selection.length - 1], true);
            } else {
                this.materialSelectRow = selection[0];
            }
            console.log(this.materialSelectRow)
        },
        tableWholeFilter() {
            if (!this.orderSearch && !this.assetsTypeSearch && !this.isPurchaseOrderFilter) {
                this.materialPurchaseFilterData = this.materialPurchaseTestData;
                return;
            }

            this.materialPurchaseFilterData = this.materialPurchaseTestData.filter(task => {
                const orderMatch = task.purchaseOrderId.includes(this.orderSearch);
                const typeMatch = task.purchaseType.includes(this.assetsTypeSearch);
                const purchaseOrderMatch = this.isPurchaseOrderFilter === "" || task.isPurchaseOrder.includes(this.isPurchaseOrderFilter);

                return orderMatch && typeMatch && purchaseOrderMatch;
            });
        },
        openUnsubmitDialog() {
            this.unsubmitVis = true
        },
        openCreateDialog() {
            this.createVis = true
        },
        openNewMaterialDialog() {
            this.newMaterialVis = true
            this.assetFilterTable = this.assetTable
        },
        openPreviewDialog() {
            this.purchaseOrderVis = true
        },
        confirmNewMaterialAdd() {
            if (this.materialSelectRow === null) {
                ElMessageBox.alert('材料不能为空！', '警告', { confirmButtonText: '确认' })
                return
            }

            this.newAssetPurchaseData.push({
                materialName: this.materialSelectRow.materialName,
                warehouseType: this.materialSelectRow.warehouseName,
                unit: this.materialSelectRow.unit,
                purchaseAmount: 0,
                factoryName: this.materialSelectRow.factoryName,
                isPurchaseOrder: '独立采购',
                purchaseOrderId: '',
                comment: ''
            });
            this.addAssetName = '';
            this.newMaterialVis = false
        },
        getFilteredFactoryOptions(materialName) {
            const filteredOptions = this.factoryOptions.filter(option => option.materialName === materialName);
            return [{ factoryName: '询价' }, ...filteredOptions];
        },
        materialTableWholeFilter() {
            if (!this.materialSearch && !this.factorySearch) {
                this.assetFilterTable = this.assetTable;
                return;
            }

            this.assetFilterTable = this.assetTable.filter(task => {
                const materialMatch = task.materialName.includes(this.materialSearch);
                const factoryMatch = task.factoryName.includes(this.factorySearch);

                return materialMatch && factoryMatch;
            });
        }
    }
}
</script>