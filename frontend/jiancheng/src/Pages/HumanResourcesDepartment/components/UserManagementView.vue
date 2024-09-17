<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
            >用户管理</el-col
        >
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            用户名搜索：
            <el-input v-model="searchValue" placeholder="请输入用户名" clearable suffix-icon=""></el-input>
        </el-col>
        <el-col :span="4" :offset="4" style="white-space: nowrap;">
            职员姓名搜索：
            <el-input v-model="searchValue" placeholder="请输入职员姓名" clearable suffix-icon=""></el-input>
        </el-col>
        <el-col :span="4" :offset="8">
            <el-button type="primary" size="default" @click="openAddUserDialog">添加新用户</el-button>
            
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24" :offset="0">
            <el-table :data="userData" border style="height: 500px" v-loading="datafinished" >
                <el-table-column prop="userName" label="用户名"></el-table-column>
                <el-table-column prop="staffName" label="姓名"></el-table-column>
                <el-table-column prop="characterName" label="角色"></el-table-column>
                <el-table-column prop="departmentName" label="部门" :filters="departmentFilter" :filter-method="filterDepartment" filter-placement="bottom-end"></el-table-column>
                <!-- <el-table-column prop="email" label="邮箱"></el-table-column>
                <el-table-column prop="phone" label="电话"></el-table-column> -->
                <el-table-column prop="operation" label="操作">
                    <template #default="scope">
                        <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-dialog
        title="添加用户"
        v-model="addUserDialogVisible"
        width="30%">
        <el-form>
            <el-form-item label="用户名: ">
                <el-input v-model="addUserData.userName"></el-input>
            </el-form-item>
            <el-form-item label="姓名: ">
                <el-input v-model="addUserData.staffName"></el-input>
            </el-form-item>
            <el-form-item label="角色: ">
                <el-select v-model="addUserData.characterId" placeholder="请选择角色">
                    <el-option v-for="item in characterData" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                    </el-select>
            </el-form-item>
            <el-form-item label="部门: ">
                <el-select v-model="addUserData.departmentId" placeholder="请选择部门">
                    <el-option v-for="item in departmentData" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                    </el-select>
            </el-form-item>
            </el-form>
        <template #footer>
        <span>
            <el-button @click="addUserDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="createUser">确认</el-button>
        </span>
        </template>
    </el-dialog>
    
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            addUserDialogVisible: false,
            datafinished: true,
            userData: [],
            addUserData: {
                userName: '',
                staffName: '',
                characterId: '',
                departmentId: ''
            },
            characterData:[],
            departmentData: [],
            staffData: [],
            searchValue: '',
            departmentFilter: [
                {
                    text: '人事部',
                    value: '人事部'
                },
                {
                    text: '物控部',
                    value: '物流部'
                },
                {
                    text: '财务部',
                    value: '财务部'
                },
                {
                    text: '总仓',
                    value: '总仓'
                },
                {
                    text: '总经理',
                    value: '总经理'
                },
                {
                    text: '生产部',
                    value: '生产部'
                },
                {
                    text: '业务部',
                    value: '业务部'
                },
                {
                    text: '开发部',
                    value: '开发部'
                },

            ]
        }
    },
    methods: {
        handleEdit(row) {
            console.log('Edit user:', row)
        },
        handleDelete(row) {
            console.log('Delete user:', row)
        },
        filterDepartment(value, row) {
            return row.departmentName === value
        },
        openAddUserDialog() {
            this.addUserDialogVisible = true
        },
        async getUserData() {
            const response = await axios.get('http://localhost:8000/usermanage/getallusers')
            console.log(response)
            this.userData = response.data
            this.datafinished = false
        },
        async getCharacterData() {
            const response = await axios.get('http://localhost:8000/general/getallcharacters')
            console.log(response)
            this.characterData = response.data
        },
        async getDepartmentData() {
            const response = await axios.get('http://localhost:8000/general/getalldepartments')
            console.log(response)
            this.departmentData = response.data
        },
        async getStaffData() {
            const response = await axios.get('http://localhost:8000/general/getallstaffs')
            console.log(response)
            this.staffData = response.data
        },
        async createUser() {
            this.$confirm('确认添加用户吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                this.datafinished = true
                await axios.post('http://localhost:8000/usermanage/createuser', this.addUserData)
                    .then(response => {
                        console.log(response)
                        this.addUserDialogVisible = false
                        this.getUserData()
                    })
                    .catch(error => {
                        console.log('Create user failed!')
                    })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消添加用户'
                });
            });
        },
    },
    mounted() {
        this.getUserData()
        this.getCharacterData()
        this.getDepartmentData()
    },
}
</script>

