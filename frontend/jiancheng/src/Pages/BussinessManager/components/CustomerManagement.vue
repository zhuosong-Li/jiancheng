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
                            >编辑</el-button
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
            addCustomerDialogVisible: false,
            editCustomerDialogVisible: false,
            customerTableData: []
        }
    },
    mounted() {
        this.$setAxiosToken()
        this.getCustomerList()
    },
    methods: {
        async getCustomerList() {
            const response = await axios.get('http://localhost:8000/customer/getcustomerdetails')
            this.customerTableData = response.data
        },
        openAddCustomerDialog() {
            this.addCustomerDialogVisible = true
        },
        openEditCustomerDialog(row) {
            this.editCustomerDialogVisible = true
            this.orderForm = row

        },
        submitAddCustomerForm() {
            console.log(this.orderForm)
            this.$confirm('确认添加客户信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post('http://localhost:8000/customer/addcustomer', this.orderForm)
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
        submitEditCustomerForm() {
            console.log(this.orderForm)
            this.$confirm('确认修改客户信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                const response = await axios.post('http://localhost:8000/customer/editcustomer', this.orderForm)
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