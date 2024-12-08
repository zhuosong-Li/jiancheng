<template>
    <el-container direction="vertical">
        <el-main style="height: 100vh;">
            <el-row :gutter="20" style="text-align: center;">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">
                    {{ `耗材/固定资产采购订单 ${purchaseOrderRId}` }}
                </el-col>
            </el-row>
            <el-form :model="assetForm" :rules="rules" ref="assetForm">
                <el-form-item prop="purchaseOrderType" label="采购类型">
                    <el-radio-group v-model="assetForm.purchaseOrderType">
                        <el-radio value="O" label="随订单采购"></el-radio>
                        <el-radio value="X" label="随鞋型采购"></el-radio>
                        <el-radio value="I" label="独立采购"></el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item v-if="assetForm.purchaseOrderType == 'O'" prop="orderId" label="选择订单">
                    <el-table :data="activeOrders" border stripe>
                        <el-table-column width="55">
                            <template #default="scope">
                                <el-radio :value="scope.row.orderId" v-model="assetForm.orderId">
                                </el-radio>
                            </template>
                        </el-table-column>
                        <el-table-column prop="orderRId" label="订单号"></el-table-column>
                    </el-table>
                </el-form-item>
                <el-form-item v-if="assetForm.purchaseOrderType == 'X'" prop="orderShoeId" label="选择鞋型">
                    <el-table :data="activeOrderShoes" border stripe>
                        <el-table-column width="55">
                            <template #default="scope">
                                <el-radio :value="scope.row.orderShoeId" v-model="assetForm.orderShoeId">
                                </el-radio>
                            </template>
                        </el-table-column>
                        <el-table-column prop="orderRId" label="订单号"></el-table-column>
                        <el-table-column prop="shoeRId" label="工厂型号"></el-table-column>
                    </el-table>
                </el-form-item>
            </el-form>
            <el-form-item prop="purchaseData">
                <PurchaseItemsTable :material-type-options="materialTypeOptions"
                    :purchaseData.sync="assetForm.purchaseData" @update-items="updateNewPurchaseData" />
            </el-form-item>

            <el-row :gutter="20">
                <span>
                    <el-button type="primary" @click="savePurchaseOrder">保存</el-button>
                    <!-- <el-button type="primary" @click="">提交</el-button> -->
                </span>
            </el-row>
        </el-main>
    </el-container>
</template>
<script>
import axios from 'axios'
import PurchaseItemsTable from '../components/VariousPurchaseTables/PurchaseItemsTable.vue';
import { ElMessage } from 'element-plus';
export default {
    components: {
        PurchaseItemsTable
    },
    props: ["purchaseorderid"],
    data() {
        return {
            assetForm: {
                purchaseOrderType: null,
                orderId: null,
                orderShoeId: null,
                purchaseData: []
            },
            activeOrders: [],
            activeOrderShoes: [],
            purchaseOrderRId: null,
            materialTypeOptions: [],
            rules: {
                purchaseOrderType: { required: true, message: '此项为必填项', trigger: 'change' },
                orderId: [
                    {
                        required: true,
                        validator: (rule, value, callback) => {
                            if (this.assetForm.purchaseOrderType == 'O' && !value) {
                                callback(new Error("尚未选择订单"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                ],
                orderShoeId: [
                    {
                        required: true,
                        validator: (rule, value, callback) => {
                            if (this.assetForm.purchaseOrderType == 'X' && !value) {
                                callback(new Error("尚未选择订单鞋型"));
                            } else {
                                callback();
                            }
                        },
                        trigger: "change",
                    },
                ],
            },
        }
    },
    mounted() {
        this.getAllMaterialTypes()
        this.loadPurchaseOrder()
        this.getActiveOrders()
        this.getActiveOrderShoes()
    },
    methods: {
        async loadPurchaseOrder() {
            if (this.$props.purchaseorderid === "null") {
                await this.getPurchaseOrderId()
            }
            else {
                let params = { purchaseOrderId: this.$props.purchaseorderid }
                const response = await axios.get(`${this.$apiBaseUrl}/logistics/getassetspurchaseorderitems`, { params })
                this.assetForm.purchaseData = response.data.data
                this.purchaseOrderRId = this.assetForm.purchaseData[0].purchaseOrderRId
                this.assetForm.purchaseOrderType = this.assetForm.purchaseData[0].purchaseOrderType
                this.assetForm.orderId = this.assetForm.purchaseData[0].orderId
                this.assetForm.orderShoeId = this.assetForm.purchaseData[0].orderShoeId
            }
        },
        async getAllMaterialTypes() {
            let response = await axios.get(`${this.$apiBaseUrl}/logistics/getallmaterialtypes`)
            this.materialTypeOptions = response.data
        },
        updateNewPurchaseData(updatedItems) {
            this.assetForm.purchaseData = [...updatedItems]
        },
        async getActiveOrders() {
            let response = await axios.get(`${this.$apiBaseUrl}/order/getactiveorders`)
            this.activeOrders = response.data
        },
        async getActiveOrderShoes() {
            let response = await axios.get(`${this.$apiBaseUrl}/order/getactiveordershoes`)
            this.activeOrderShoes = response.data
        },
        async getPurchaseOrderId() {
            let response = await axios.post(
                `${this.$apiBaseUrl}/logistics/getassetsnewpurchaseorderid`,
                {
                    department: '01'
                }
            )
            this.purchaseOrderRId = response.data.newId
        },
        async savePurchaseOrder() {
            // validate the data before insert
            this.$refs.assetForm.validate(async (valid) => {
                if (valid) {
                    for (let row of this.assetForm.purchaseData) {
                        let zeroAmount = row.purchaseAmount == 0
                        let noMaterialName = !row.materialName
                        if (zeroAmount) {
                            ElMessage.error("采购数量不能为零")
                            return
                        }
                        if (noMaterialName) {
                            ElMessage.error("材料名称不能为空")
                            return
                        }
                    }
                    try {
                        console.log(this.assetForm)
                        if (this.$props.purchaseorderid) {
                            await axios.post(
                                `${this.$apiBaseUrl}/logistics/editsavedpurchaseorderitems`,
                                {
                                    data: this.assetForm.purchaseData,
                                    purchaseOrderId: this.$props.purchaseorderid,
                                    orderId: this.assetForm.orderId,
                                    orderShoeId: this.assetForm.orderShoeId,
                                    purchaseDivideOrderType: 'N',
                                    purchaseOrderType: this.assetForm.purchaseOrderType
                                }
                            )
                        }
                        else {
                            await axios.post(
                                `${this.$apiBaseUrl}/logistics/newpurchaseordersave`,
                                {
                                    data: this.assetForm.purchaseData,
                                    purchaseOrderRId: this.purchaseOrderRId,
                                    orderId: this.assetForm.orderId,
                                    orderShoeId: this.assetForm.orderShoeId,
                                    purchaseDivideOrderType: 'N',
                                    purchaseOrderType: this.assetForm.purchaseOrderType
                                }
                            )
                        }
                        ElMessage.success('保存成功')
                    }
                    catch (error) {
                        console.log(error)
                        ElMessage.error("保存失败")
                    }
                }
                else {
                    console.log("validation error")
                }
            })
        },
    },
}
</script>