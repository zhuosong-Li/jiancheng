<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">仓库管理</el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24" :offset="0">
            <el-table :data="materialPurchaseFilterData" border style="height: 500px;">
                <el-table-column prop="warehouseName" label="仓库名称"></el-table-column>
                <el-table-column prop="addDate" label="添加日期"></el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="4" :offset="20"><el-button type="primary" size="default" @click="openCreateDialog">创建新仓库</el-button>
        </el-col>
    </el-row>

    <el-dialog title="创建新仓库" v-model="createVis" width="30%">
        <el-row :gutter="20">
            <el-col :span="3" :offset="0" style="white-space: nowrap;">仓库名：</el-col>
            <el-col :span="12" :offset="0"><el-input v-model="warehouseName" placeholder="" size="default" clearable @change=""></el-input>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="">取消</el-button>
                <el-button type="primary" @click="">确认</el-button>
            </span>
        </template>
    </el-dialog>

</template>
<script>

export default {
    data() {
        return {
            createVis: false,
            warehouseName: ''
        }
    },
    methods: {
        openCreateDialog() {
            this.createVis = true
        }
    }
}
</script>