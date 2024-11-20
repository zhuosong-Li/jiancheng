<template>
    <el-container>
        <el-header>
            <AllHeader></AllHeader>
        </el-header>
        <el-container>
            <el-main>
                <el-table
                    :data="orderShoeData"
                    border
                    stripe
                    height="650"
                    :row-key="
                        (row) => {
                            return row.orderShoeTypeId
                        }
                    "
                >
                    <el-table-column type="expand">
                        <template #default="props">
                            <el-table
                                :data="props.row.orderShoeTypes"
                                border
                                :row-key="
                                    (row) => {
                                        return row.packagingInfoId
                                    }
                                "
                            >
                                <el-table-column type="expand">
                                    <template #default="scope">
                                        <el-table :data="scope.row.shoeTypeBatchInfoList">
                                            <el-table-column
                                                prop="packaginginfolocale"
                                                label="地区"
                                            />
                                            <el-table-column
                                                prop="packaginginfoname"
                                                label="名称"
                                            />
                                            <el-table-column prop="size34ratio" label="34" />
                                            <el-table-column prop="size35ratio" label="35" />
                                            <el-table-column prop="size36ratio" label="36" />
                                            <el-table-column prop="size37ratio" label="37" />
                                            <el-table-column prop="size38ratio" label="38" />
                                            <el-table-column prop="size39ratio" label="39" />
                                            <el-table-column prop="size40ratio" label="40" />
                                            <el-table-column prop="size41ratio" label="41" />
                                            <el-table-column prop="size42ratio" label="42" />
                                            <el-table-column prop="size43ratio" label="43" />
                                            <el-table-column prop="size44ratio" label="44" />
                                            <el-table-column prop="size45ratio" label="45" />
                                            <el-table-column prop="size46ratio" label="46" />
                                            <el-table-column
                                                prop="totalquantityratio"
                                                label="比例和"
                                            />
                                            <el-table-column
                                                prop="unitPerRatio"
                                                label="比例单位数量"
                                            />
                                        </el-table>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    prop="shoeTypeColorName"
                                    label="颜色名称"
                                    sortable
                                />
                                <el-table-column prop="shoeTypeBatchData.size34Amount" label="34" />
                                <el-table-column prop="shoeTypeBatchData.size35Amount" label="35" />
                                <el-table-column prop="shoeTypeBatchData.size36Amount" label="36" />
                                <el-table-column prop="shoeTypeBatchData.size37Amount" label="37" />
                                <el-table-column prop="shoeTypeBatchData.size38Amount" label="38" />
                                <el-table-column prop="shoeTypeBatchData.size39Amount" label="39" />
                                <el-table-column prop="shoeTypeBatchData.size40Amount" label="40" />
                                <el-table-column prop="shoeTypeBatchData.size41Amount" label="41" />
                                <el-table-column prop="shoeTypeBatchData.size42Amount" label="42" />
                                <el-table-column prop="shoeTypeBatchData.size43Amount" label="43" />
                                <el-table-column prop="shoeTypeBatchData.size44Amount" label="44" />
                                <el-table-column prop="shoeTypeBatchData.size45Amount" label="45" />
                                <el-table-column prop="shoeTypeBatchData.size46Amount" label="46" />
                                <el-table-column
                                    prop="shoeTypeBatchData.totalAmount"
                                    label="总数量"
                                />

                                <el-table-column label="金额">
                                    <template #default="scope">
                                        <el-input
                                            size="small"
                                            controls-position="right"
                                            @change="updateValue(scope.row)"
                                            v-model.lazy="scope.row.shoeTypeBatchData.unitPrice"
                                            :disabled="priceChangeNotAllowed"
                                        >
                                        </el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    prop="shoeTypeBatchData.totalPrice"
                                    label="总金额"
                                />
                            </el-table>
                        </template>
                    </el-table-column>
                    <el-table-column prop="shoeRid" label="鞋型编号" sortable />
                    <el-table-column prop="shoeCid" label="客户鞋型编号" sortable />
                    <el-table-column prop="currentStatus" label="订单状态" />
                    <el-table-column label="备注">
                        <template #default="scope">
                            <el-button
                                v-if="!scope.row.orderShoeRemarkExist"
                                type="primary"
                                size="default"
                                @click="openRemarkDialog(scope.row)"
                                style="margin-left: 20px; margin-top: -20px"
                                >添加备注
                            </el-button>

                            <el-text v-if="scope.row.orderShoeRemarkExist">{{
                                scope.row.orderShoeRemarkRep
                            }}</el-text>
                            <el-button
                                v-if="scope.row.orderShoeRemarkExist"
                                type="warning"
                                size="default"
                                @click="openEditRemarkDialog(scope.row)"
                                style="margin-left: 20px; margin-top: -20px"
                            >
                                编辑备注
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>

                <span>
                    <el-button type="primary" size="middle" @click="submitFormData"
                        >确认修改完成</el-button
                    >
                </span>
            </el-main>
        </el-container>
    </el-container>
    <el-dialog title="鞋型备注" v-model="remarkDialogVis" width="50%">
        <el-form>
            <el-form-item label="工艺备注">
                <el-input type="textarea" :rows="2" v-model="remarkForm.technicalRemark"></el-input>
            </el-form-item>

            <el-form-item label="材料备注">
                <el-input type="textarea" :rows="2" v-model="remarkForm.materialRemark"></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <span>
                <el-button @click="remarkDialogVis = false">取消</el-button>

                <el-button type="primary" @click="submitRemarkForm">提交备注</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
import { onMounted, reactive, ref } from 'vue'
import { getCurrentInstance } from 'vue'
import { ElMessage } from 'element-plus'

const $api_baseUrl = getCurrentInstance().appContext.config.globalProperties.$apiBaseUrl

const { orderId } = defineProps(['orderId'])
let orderData = reactive({})
let orderShoeData = ref([])
let priceChangeNotAllowed = ref(false)
let remarkDialogVis = ref(false)
let orderShoeTypeIdToUnitPrice = reactive({})
let remarkForm = reactive({
    orderShoeId: '',
    technicalRemark: '',
    materialRemark: ''
})

onMounted(() => {
    getOrderInfo()
})

async function getOrderInfo() {
    const response = await axios.get(
        `${$api_baseUrl}/order/getbusinessorderinfo?orderid=${orderId}`
    )
    orderData = response.data
    orderShoeData.value = response.data.orderShoeAllData
}
function updateValue(row) {
    row.shoeTypeBatchData.totalPrice =
        row.shoeTypeBatchData.unitPrice * row.shoeTypeBatchData.totalAmount
    orderShoeTypeIdToUnitPrice[row.orderShoeTypeId] = row.shoeTypeBatchData.unitPrice
}

async function submitFormData() {
    await axios.post(`${$api_baseUrl}/order/getbusinessorderinfo?orderid=${orderId}`)
}

function openRemarkDialog(row) {
    remarkForm.orderShoeId = row.orderShoeId
    remarkDialogVis.value = true
}
function openEditRemarkDialog(row) {
    remarkForm.orderShoeId = row.orderShoeId
    remarkForm.technicalRemark = row.orderShoeTechnicalRemark
    remarkForm.materialRemark = row.orderShoeMaterialRemark
    remarkDialogVis.value = true
}
async function submitRemarkForm() {
    const response = await axios.post(`${$api_baseUrl}/ordercreate/updateremark`, {
        orderShoeRemarkForm: remarkForm
    })
    if (response.status === 200) {
        ElMessage.success('信息变更成功')
        getOrderInfo()
        remarkDialogVis.value = false
    }
}
</script>

<style scoped>
.el-table .cell {
    white-space: pre-line !important;
}
</style>
