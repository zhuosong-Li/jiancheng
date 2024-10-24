<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
            >客户管理</el-col
        >
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-table
                :data="customerTableData"
                style="width: 100%"
                stripe
                border
                height="500"
            >
                <el-table-column
                    prop="customerId"
                    label="客户编号"
                ></el-table-column>
                <el-table-column
                    prop="customerName"
                    label="客户名称"
                ></el-table-column>
                <el-table-column
                    prop="customerBrand"
                    label="客户商标"
                ></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button
                            type="primary"
                            size="mini"
                            @click="openEditCustomerDialog(scope.row)"
                            >编辑客户</el-button
                        >
                        <el-button
                            type="primary"
                            size="mini"
                            @click="openEditCustomerBatchDialog(scope.row)"
                            >配码管理</el-button
                        >
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-button type="primary" @click="openEditCustomerDialog">添加新客户</el-button>
        </el-col>
    </el-row>
    <el-dialog
        title="添加客户"
        v-model="addCustomerDialogVisible"
        width="30%">
        <el-form :model="orderForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="客户名称">
                <el-input v-model="orderForm.customerName"></el-input>
            </el-form-item>
            <el-form-item label="客户商标">
                <el-input v-model="orderForm.customerBrand"></el-input>
            </el-form-item>
        </el-form>
        
        <template #footer>
        <span>
            <el-button @click="addCustomerDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitAddCustomerForm">确认提交</el-button>
        </span>
        </template>
    </el-dialog>

    <el-dialog
        title = "配码管理"
        v-model="editCustomerBatchDialogVisible"
        width = "90%">
        <el-col :span="4" :offset="15"
            ><el-input
                v-model="batchNameFilter"
                placeholder="请输入配码名称"
                size="normal"
                :suffix-icon="Search"
                clearable
                @input="filterBatchData"
            ></el-input>
        </el-col>
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-descriptions title="" :column="2" border>
                    <el-descriptions-item label="客户名称" align="center">{{
                        batchDialogCurCustomerName
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户商标" align="center">{{
                        batchDialogCurCustomerBrand
                    }}</el-descriptions-item>
                </el-descriptions>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-table :data="customerDisplayBatchData" border stripe height="500">

                <el-table-column prop="packagingInfoName" label="配码名称" sortable/>
                <el-table-column prop="packagingInfoLocale" label="配码地区" sortable/>
                <el-table-column prop="size34Ratio" label="34" />
                <el-table-column prop="size35Ratio" label="35" />
                <el-table-column prop="size36Ratio" label="36" />
                <el-table-column prop="size37Ratio" label="37" />
                <el-table-column prop="size38Ratio" label="38" />
                <el-table-column prop="size39Ratio" label="39" />
                <el-table-column prop="size40Ratio" label="40" />
                <el-table-column prop="size41Ratio" label="41" />
                <el-table-column prop="size42Ratio" label="42" />
                <el-table-column prop="size43Ratio" label="43" />
                <el-table-column prop="size44Ratio" label="44" />
                <el-table-column prop="size45Ratio" label="45" />
                <el-table-column prop="size46Ratio" label="46" />

                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default" @click="openPreviewDialog(scope.row)"
                            >查看详情</el-button
                        >
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
        <span>
            <el-button @click="editCustomerBatchDialogVisible = false">取消</el-button>
            <el-button @click="openAddCustomerBatchDialog()"> 添加配码</el-button>
        </span>
    </el-dialog>

    <el-dialog
        title="添加配码"
        v-model="addCustomerBatchDialogVisible"
        width="30%">
        <el-form :model="batchForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="配码名称">
                <el-input v-model="batchForm.batchName"></el-input>
            </el-form-item>
            <el-form-item label="配码地区">
                <el-input v-model="batchForm.batchLocale"></el-input>
            </el-form-item>
            <el-form-item label="34">
                <el-input v-model="batchForm.batchQuantity34"></el-input>
            </el-form-item>
            <el-form-item label="35">
                <el-input v-model="batchForm.batchQuantity35"></el-input>
            </el-form-item>
            <el-form-item label="36">
                <el-input v-model="batchForm.batchQuantity36"></el-input>
            </el-form-item>
            <el-form-item label="37">
                <el-input v-model="batchForm.batchQuantity37"></el-input>
            </el-form-item>
            <el-form-item label="38">
                <el-input v-model="batchForm.batchQuantity38"></el-input>
            </el-form-item>
            <el-form-item label="39">
                <el-input v-model="batchForm.batchQuantity39"></el-input>
            </el-form-item>
            <el-form-item label="40">
                <el-input v-model="batchForm.batchQuantity40"></el-input>
            </el-form-item>
            <el-form-item label="41">
                <el-input v-model="batchForm.batchQuantity41"></el-input>
            </el-form-item>
            <el-form-item label="42">
                <el-input v-model="batchForm.batchQuantity42"></el-input>
            </el-form-item>
            <el-form-item label="43">
                <el-input v-model="batchForm.batchQuantity43"></el-input>
            </el-form-item>
            <el-form-item label="44">
                <el-input v-model="batchForm.batchQuantity44"></el-input>
            </el-form-item>
            <el-form-item label="45">
                <el-input v-model="batchForm.batchQuantity45"></el-input>
            </el-form-item>
            <el-form-item label="46">
                <el-input v-model="batchForm.batchQuantity46"></el-input>
            </el-form-item>
        </el-form>
        
        <template #footer>
        <span>
            <el-button @click="addCustomerDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitAddCustomerBatchForm">确认提交</el-button>
        </span>
        </template>
    </el-dialog>



    <el-dialog
        title="编辑客户"
        v-model="editCustomerDialogVisible"
        width="30%">
        <el-form :model="orderForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="客户名称">
                <el-input v-model="orderForm.customerName"></el-input>
            </el-form-item>
            <el-form-item label="客户商标">
                <el-input v-model="orderForm.customerBrand"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
        <span>
            <el-button @click="editCustomerDialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="submitEditCustomerForm">OK</el-button>
        </span>
        </template>
    </el-dialog>
    
    
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            orderForm: {
                customerId: '',
                customerName: '',
                customerBrand: ''
            },
            batchForm: {
                customerId:'',
                batchName: '',
                batchLocale: '',
                batchQuantity34: 0,
                batchQuantity35: 0,
                batchQuantity36: 0,
                batchQuantity37: 0,
                batchQuantity38: 0,
                batchQuantity39: 0,
                batchQuantity40: 0,
                batchQuantity41: 0,
                batchQuantity42: 0,
                batchQuantity43: 0,
                batchQuantity44: 0,
                batchQuantity45: 0,
                batchQuantity46: 0

            },
            addCustomerDialogVisible: false,
            editCustomerDialogVisible: false,
            addCustomerBatchDialogVisible: false,
            editCustomerBatchDialogVisible: false,
            batchNameFilter: '',
            customerTableData: [],
            customerBatchData: [],
            customerDisplayBatchData: [],
            customerFilteredBatchData: [],
            batchDialogCurCustomerName:'',
            batchDialogCurCustomerBrand:'',
            batchDialogCurCustomerId:''
        }
    },
    mounted() {
        this.$setAxiosToken()
        this.getCustomerList()
    },
    methods: {
        async getCustomerList() {
            const response = await axios.get(`${this.$apiBaseUrl}/customer/getcustomerdetails`)
            this.customerTableData = response.data
        },
        async getCustomerBatchInfo(customerId) {
            const response = await axios.get(`${this.$apiBaseUrl}/customer/getcustomerbatchinfo`,{
                params: {
                    customerid: customerId
                }
            })
            console.log(response.data)
            this.customerBatchData = response.data
            this.customerDisplayBatchData = response.data
        },
        filterBatchData(){
            if (!this.batchNameFilter){
                this.customerDisplayBatchData = this.customerBatchData
            }
            else{
                this.customerFilteredBatchData = this.customerBatchData.filter((task) => {
                    const filteredData = task.packagingInfoName.includes(this.batchNameFilter)
                    return filteredData
                })
                this.customerDisplayBatchData = this.customerFilteredBatchData
            }
        },
        openAddCustomerDialog() {
            this.addCustomerDialogVisible = true
        },
        openEditCustomerDialog(row) {
            this.editCustomerDialogVisible = true
            this.orderForm = row

        },
        openAddCustomerBatchDialog(row) {
            this.batchForm.customerId = this.batchDialogCurCustomerId
            this.addCustomerBatchDialogVisible = true
        },
        openEditCustomerBatchDialog(row) {
            this.batchDialogCurCustomerName = row.customerName
            this.batchDialogCurCustomerBrand = row.customerBrand
            this.batchDialogCurCustomerId = row.customerId
            this.getCustomerBatchInfo(row.customerId)
            this.editCustomerBatchDialogVisible = true
        },
        submitAddCustomerForm() {
            console.log(this.orderForm)
            this.$confirm('确认添加客户信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post(`${this.$apiBaseUrl}/customer/addcustomer`, this.orderForm)
                if (response.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '添加成功'
                    })
                    this.addCustomerDialogVisible = false
                    this.orderForm = {
                        customerId: '',
                        customerName: '',
                        customerBrand: ''
                    }
                    this.getCustomerList()
                } else {
                    this.$message({
                        type: 'error',
                        message: '添加失败'
                    })
                }

            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消添加'
                })
            })
        },
        submitAddCustomerBatchForm() {
            console.log(this.batchForm)
            this.$confirm('确认添加客户配码信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post(`${this.$apiBaseUrl}/customer/addcustomerbatchinfo`, this.batchForm)
                
        }).catch(() => {})},
        submitEditCustomerForm() {
            console.log(this.orderForm)
            this.$confirm('确认修改客户信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post(`${this.$apiBaseUrl}/customer/editcustomer`, this.orderForm)
                if (response.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })
                    this.editCustomerDialogVisible = false
                    this.orderForm = {
                        customerId: '',
                        customerName: '',
                        customerBrand: ''
                    }
                    this.getCustomerList()
                } else {
                    this.$message({
                        type: 'error',
                        message: '修改失败'
                    })
                }

            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消修改'
                })
            })
        }

    },
}
</script>