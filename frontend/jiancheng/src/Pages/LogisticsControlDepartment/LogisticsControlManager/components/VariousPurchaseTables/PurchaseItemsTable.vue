<template>
    <el-table :data="localTableData" border height="450">
        <el-table-column prop="materialType" label="材料类型">
            <template #default="scope">
                <el-popover trigger="hover" placement="top">
                    <p>{{ scope.row.materialType ? scope.row.materialType.materialTypeName : '' }}</p>
                    <template #reference>
                        <el-select v-model="scope.row.materialType" @change="changeWarehouseName(scope.row)"
                            value-key="materialTypeId">
                            <el-option v-for="item in materialTypeOptions" :key="item.materialTypeId" :value="item"
                                :label="item.materialTypeName">
                            </el-option>
                        </el-select>
                    </template>
                </el-popover>
            </template>
        </el-table-column>
        <el-table-column prop="warehouseName" label="所属仓库" />
        <el-table-column prop="supplierName" label="厂家名称">
            <template #default="scope">
                <el-autocomplete v-model="scope.row.supplierName" :fetch-suggestions="querySupplierNames"
                    placeholder="搜索厂家" @select="handleSupplierNameSelect(scope.row, $event)">
                </el-autocomplete>
            </template>
        </el-table-column>
        <el-table-column prop="materialName" label="材料名称">
            <template #default="scope">
                <el-input v-model="scope.row.materialName">

                </el-input>
            </template>
        </el-table-column>
        <el-table-column prop="materialModel" label="材料型号">
            <template #default="scope">
                <el-input v-model="scope.row.materialModel" clearable>

                </el-input>
            </template>
        </el-table-column>
        <el-table-column label="材料规格">
            <template #default="scope">
                <el-input v-model="scope.row.materialSpecification" placeholder="" clearable></el-input>
            </template>
        </el-table-column>
        <el-table-column label="颜色">
            <template #default="scope">
                <el-input v-model="scope.row.color" placeholder="" clearable>
                </el-input>
            </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位">
            <template #default="scope">
                <el-input v-model="scope.row.unit" placeholder="">
                </el-input>
            </template>
        </el-table-column>
        <el-table-column label="采购数量" width="150">
            <template #default="scope">
                <el-input-number v-model="scope.row.purchaseAmount" :min="0" size="small" :step="0.001" />
            </template>
        </el-table-column>
        <el-table-column label="备注">
            <template #default="scope">
                <el-input v-model="scope.row.comment" placeholder="" size="default" clearable></el-input>
            </template>
        </el-table-column>
        <el-table-column label="操作">
            <template #default="scope">
                <el-button size="small" type="danger" @click="deleteCurrentRow(scope.$index)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-button type="primary" @click="openNewMaterialDialog">添加新材料</el-button>
    <el-button type="primary" @click="manualAddMaterial">手动添加材料</el-button>


    <el-dialog title="添加新采购材料" v-model="newMaterialVis" width="60%" :close-on-click-modal="false">
        <el-row :gutter="20">
            <el-col :span="6" :offset="0">
                <el-input v-model="addMaterialDialogField.materialTypeSearch" placeholder="输入材料类型" size="default"
                    :suffix-icon="Search" clearable @change="getMaterialFilterData(currentCreateViewId)"></el-input>
            </el-col>
            <el-col :span="6" :offset="0">
                <el-input v-model="addMaterialDialogField.materialSearch" placeholder="输入材料名称" size="default"
                    :suffix-icon="Search" clearable @change="getMaterialFilterData(currentCreateViewId)"></el-input>
            </el-col>
            <el-col :span="6" :offset="0">
                <el-input v-model="addMaterialDialogField.factorySearch" placeholder="输入厂家名称" size="default"
                    :suffix-icon="Search" clearable @change="getMaterialFilterData(currentCreateViewId)"></el-input>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-table :data="assetFilterTable" border ref="materialSelectTable"
                @selection-change="handleMaterialSelectionChange" style="height: 400px">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="materialType" label="材料类型" />
                <el-table-column prop="materialName" label="材料名称" />
                <el-table-column prop="warehouseName" label="所属仓库" />
                <el-table-column prop="unit" label="单位" />
                <el-table-column prop="supplierName" label="工厂名称" />
            </el-table>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="newMaterialVis = false">取消</el-button>
                <el-button type="primary" @click="confirmNewMaterialAdd">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios'
import { markRaw } from 'vue';
import { Search } from '@element-plus/icons-vue'
export default {
    props: ["materialTypeOptions", "purchaseData"],
    data() {
        return {
            Search: markRaw(Search),
            isChooseOrderDialogOpen: false,
            isChooseOrderShoeDialogOpen: false,
            currentMaterialRow: {},
            selectedOrderId: null,
            localTableData: [],
            newItemTemplate: {
                materialName: null,
                materialType: null,
                supplierName: null,
                materialSpecification: null,
                materialModel: null,
                color: '',
                unit: '',
                purchaseAmount: 0,
                comment: '',
            },
            // search material dialog variables
            addMaterialDialogField: {},
            addMaterialTemplate: {
                materialTypeSearch: '',
                materialSearch: '',
                factorySearch: '',
            },
            assetTable: [],
            assetFilterTable: [],
            newMaterialVis: false,
            materialSelectRow: {}
        }
    },
    watch: {
        purchaseData(newItems) {
            this.localTableData = [...newItems];
        },
    },
    emits: ['update-items'],
    methods: {
        emitUpdate() {
            this.$emit('update-items', [...this.localTableData]);
        },
        async querySupplierNames(queryString, callback) {
            if (queryString.trim()) {
                await axios
                    .get(
                        `${this.$apiBaseUrl}/devproductionorder/getautofinishedsuppliername?supplierName=${queryString}`
                    )
                    .then((response) => {
                        const suggestions = response.data.map((item) => ({
                            value: item.name
                        }))
                        callback(suggestions)
                    })
                    .catch((error) => {
                        console.error('Failed to fetch material names:', error)
                    })
            } else {
                callback([])
            }
        },
        async getMaterialList() {
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getmaterialtypeandname`,
                {
                    params: {
                        materialcategory: 0
                    }
                }
            )
            this.assetTable = response.data
            this.assetFilterTable = this.assetTable
        },
        async openNewMaterialDialog() {
            this.newMaterialVis = true
            await this.getMaterialList()
            this.addMaterialDialogField = JSON.parse(JSON.stringify(this.addMaterialTemplate))
        },
        manualAddMaterial() {
            let newItem = JSON.parse(JSON.stringify(this.newItemTemplate))
            this.localTableData = [...this.localTableData, newItem]
            this.emitUpdate();
        },
        deleteCurrentRow(index) {
            this.localTableData.splice(index, 1)
            this.emitUpdate();
        },
        handleSupplierNameSelect(row, selectedItem) {
            row.supplierName = selectedItem.value
        },
        changeWarehouseName(row) {
            row.warehouseName = row.materialType.warehouseName
        },
        handleMaterialSelectionChange(selection) {
            if (selection.length > 1) {
                this.$refs.materialSelectTable.clearSelection()
                this.$refs.materialSelectTable.toggleRowSelection(
                    selection[selection.length - 1],
                    true
                )
            } else {
                this.materialSelectRow = selection[0]
            }
        },
        confirmNewMaterialAdd() {
            if (this.materialSelectRow === null) {
                ElMessageBox.alert('材料不能为空！', '警告', { confirmButtonText: '确认' })
                return
            }

            const isDuplicate = this.localTableData.some(
                (item) => item.materialName === this.materialSelectRow.materialName
            )

            if (isDuplicate) {
                ElMessageBox.alert('材料名称必须唯一！', '警告', { confirmButtonText: '确认' })
                return
            }
            let newItem = JSON.parse(JSON.stringify(this.newItemTemplate))
            newItem.materialName = this.materialSelectRow.materialName
            newItem.materialType = this.materialSelectRow.materialType
            newItem.warehouseName = this.materialSelectRow.warehouseName
            newItem.supplierName = this.materialSelectRow.supplierName
            newItem.unit = this.materialSelectRow.unit
            this.localTableData = [...this.localTableData, newItem]
            this.newMaterialVis = false
            this.addMaterialDialogField = JSON.parse(JSON.stringify(this.addMaterialTemplate))
            this.emitUpdate();
        },
    }
}
</script>