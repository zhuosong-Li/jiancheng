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
                            size="small"
                            @click="openEditCustomerDialog(scope.row)"
                            >编辑客户</el-button
                        >
                        <el-button
                            type="primary"
                            size="small"
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
            <el-button type="primary" @click="openAddCustomerDialog">添加新客户</el-button>
        </el-col>
    </el-row>
    <el-dialog
        title="添加客户"
        v-model="addCustomerDialogVisible"
        width="30%">
        <el-form :model="customerForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="客户名称">
                <el-input v-model="customerForm.customerName"></el-input>
            </el-form-item>
            <el-form-item label="客户商标">
                <el-input v-model="customerForm.customerBrand"></el-input>
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
                <el-table-column prop="totalQuantityInRatio" label="对/件" sortable/>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" size="default" @click="editBatchInfo(scope.row)"
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
                <el-input v-model="batchForm.packagingInfoName"></el-input>
            </el-form-item>
            <el-form-item label="配码地区">
                <el-input v-model="batchForm.packagingInfoLocale"></el-input>
            </el-form-item>
            <el-form-item label="34">
                <el-input v-model="batchForm.size34Ratio"></el-input>
            </el-form-item>
            <el-form-item label="35">
                <el-input v-model="batchForm.size35Ratio"></el-input>
            </el-form-item>
            <el-form-item label="36">
                <el-input v-model="batchForm.size36Ratio"></el-input>
            </el-form-item>
            <el-form-item label="37">
                <el-input v-model="batchForm.size37Ratio"></el-input>
            </el-form-item>
            <el-form-item label="38">
                <el-input v-model="batchForm.size38Ratio"></el-input>
            </el-form-item>
            <el-form-item label="39">
                <el-input v-model="batchForm.size39Ratio"></el-input>
            </el-form-item>
            <el-form-item label="40">
                <el-input v-model="batchForm.size40Ratio"></el-input>
            </el-form-item>
            <el-form-item label="41">
                <el-input v-model="batchForm.size41Ratio"></el-input>
            </el-form-item>
            <el-form-item label="42">
                <el-input v-model="batchForm.size42Ratio"></el-input>
            </el-form-item>
            <el-form-item label="43">
                <el-input v-model="batchForm.size43Ratio"></el-input>
            </el-form-item>
            <el-form-item label="44">
                <el-input v-model="batchForm.size44Ratio"></el-input>
            </el-form-item>
            <el-form-item label="45">
                <el-input v-model="batchForm.size45Ratio"></el-input>
            </el-form-item>
            <el-form-item label="46">
                <el-input v-model="batchForm.size46Ratio"></el-input>
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
        title="编辑配码"
        v-model="editBatchDialogVisible"
        width="30%">
        <el-form :model="batchForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="配码名称">
                <el-input v-model="batchForm.packagingInfoName"></el-input>
            </el-form-item>
            <el-form-item label="配码地区">
                <el-input v-model="batchForm.packagingInfoLocale"></el-input>
            </el-form-item>
            <el-form-item label="34">
                <el-input v-model="batchForm.size34Ratio"></el-input>
            </el-form-item>
            <el-form-item label="35">
                <el-input v-model="batchForm.size35Ratio"></el-input>
            </el-form-item>
            <el-form-item label="36">
                <el-input v-model="batchForm.size36Ratio"></el-input>
            </el-form-item>
            <el-form-item label="37">
                <el-input v-model="batchForm.size37Ratio"></el-input>
            </el-form-item>
            <el-form-item label="38">
                <el-input v-model="batchForm.size38Ratio"></el-input>
            </el-form-item>
            <el-form-item label="39">
                <el-input v-model="batchForm.size39Ratio"></el-input>
            </el-form-item>
            <el-form-item label="40">
                <el-input v-model="batchForm.size40Ratio"></el-input>
            </el-form-item>
            <el-form-item label="41">
                <el-input v-model="batchForm.size41Ratio"></el-input>
            </el-form-item>
            <el-form-item label="42">
                <el-input v-model="batchForm.size42Ratio"></el-input>
            </el-form-item>
            <el-form-item label="43">
                <el-input v-model="batchForm.size43Ratio"></el-input>
            </el-form-item>
            <el-form-item label="44">
                <el-input v-model="batchForm.size44Ratio"></el-input>
            </el-form-item>
            <el-form-item label="45">
                <el-input v-model="batchForm.size45Ratio"></el-input>
            </el-form-item>
            <el-form-item label="46">
                <el-input v-model="batchForm.size46Ratio"></el-input>
            </el-form-item>

        </el-form>
        
        <template #footer>
        <span>
            <el-button @click="editBatchDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEditCustomerBatchForm">确认提交</el-button>
        </span>
        </template>
    </el-dialog>

    <el-dialog
        title="编辑客户"
        v-model="editCustomerDialogVisible"
        width="30%">
        <el-form :model="customerForm" label-width="120px" :inline="false" size="normal">
            <el-form-item label="客户名称">
                <el-input v-model="customerForm.customerName"></el-input>
            </el-form-item>
            <el-form-item label="客户商标">
                <el-input v-model="customerForm.customerBrand"></el-input>
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
            customerForm: {
                customerId: '',
                customerName: '',
                customerBrand: ''
            },
            batchForm: {
                customerId:'',
                packagingInfoName: '',
                packagingInfoLocale: '',
                size34Ratio: 0,
                size35Ratio: 0,
                size36Ratio: 0,
                size37Ratio: 0,
                size38Ratio: 0,
                size39Ratio: 0,
                size40Ratio: 0,
                size41Ratio: 0,
                size42Ratio: 0,
                size43Ratio: 0,
                size44Ratio: 0,
                size45Ratio: 0,
                size46Ratio: 0,
                totalQuantityInRatio:0
                },
            addCustomerDialogVisible: false,
            editCustomerDialogVisible: false,
            addCustomerBatchDialogVisible: false,
            editCustomerBatchDialogVisible: false,
            editBatchDialogVisible:false,
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
        editBatchInfo(row){
            this.editBatchDialogVisible = true
            this.batchForm = row
            console.log(row)

        },
        openAddCustomerDialog() {
            this.addCustomerDialogVisible = true
        },
        openEditCustomerDialog(row) {
            this.editCustomerDialogVisible = true
            this.customerForm = row

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
            console.log(this.customerForm)
            this.$confirm('确认添加客户信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post(`${this.$apiBaseUrl}/customer/addcustomer`, this.customerForm)
                if (response.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '添加成功'
                    })
                    this.addCustomerDialogVisible = false
                    this.customerForm = {
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
                
        }).catch(() => {})


        },
        submitEditCustomerBatchForm(){
            console.log(this.batchForm)
             this.$confirm('确认修改客户配码信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post(`${this.$apiBaseUrl}/customer/editbatchinfo`, this.batchForm)
                if (response.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })
                    this.editBatchDialogVisible = false
                    this.batchForm = {
                        customerId:'',
                        packagingInfoName: '',
                        packagingInfoLocale: '',
                        size34Ratio: 0,
                        size35Ratio: 0,
                        size36Ratio: 0,
                        size37Ratio: 0,
                        size38Ratio: 0,
                        size39Ratio: 0,
                        size40Ratio: 0,
                        size41Ratio: 0,
                        size42Ratio: 0,
                        size43Ratio: 0,
                        size44Ratio: 0,
                        size45Ratio: 0,
                        size46Ratio: 0,
                        totalQuantityInRatio:0
                        }
                    this.getCustomerBatchInfo(this.batchDialogCurCustomerId)
                // this.getCustomerList()
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

        },
        submitEditCustomerForm() {
            console.log(this.customerForm)
            this.$confirm('确认修改客户信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post(`${this.$apiBaseUrl}/customer/editcustomer`, this.customerForm)
                if (response.status === 200) {
                    this.$message({
                        type: 'success',
                        message: '修改成功'
                    })
                    this.editCustomerDialogVisible = false
                    this.customerForm = {
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