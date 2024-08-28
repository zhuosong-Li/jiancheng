<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">一次BOM填写</el-col>
    </el-row>
    <component :is="components[currentDash]" :pendingTaskData="pendingData" :inProgressTaskData="inProgressData" @backToList="changeToList"
    @changeToPend="changeToPend" @changeToProgress="changeToProgress">
    </component>
</template>



<script setup>
import { onMounted, ref} from 'vue';
import axios from 'axios';

import { Grid, Memo } from '@element-plus/icons-vue'
import FirstBOMList from './FirstBOMCreate/FirstBOMList.vue'
import FirstOrderPend from './FirstBOMCreate/FirstBOMListPend.vue'
import FirstOrderProgress from './FirstBOMCreate/FirstBOMListProgress.vue'

const components = {
    FirstBOMList,
    FirstOrderPend,
    FirstOrderProgress
}

const pendingData = ref([])
const inProgressData = ref([])
onMounted(()=> {
    const params = {
        orderstatus: 9,
        ordershoestatus: 4
    };
    axios.get("http://localhost:8000/order/getorderbystatus", { params }).then(response => {
        const fetchPending = response.data.pendingOrders
        const fetchInProgress = response.data.inProgressOrders
        console.log("fetchPending is ")
        console.log(response.data.pendingData)
        fetchPending.forEach(element => {
            element['taskName'] = "一次BOM填写"
            pendingData.value.push(element)
        });
        console.log(pendingData.value)
        console.log(5)
        fetchInProgress.forEach(element => {
            element['taskName'] = "一次BOM填写"
            inProgressData.value.push(element)
        });
    })

})

const currentDash = ref('FirstBOMList')

const changeToList = () => {
    currentDash.value = 'FirstBOMList'
}
const changeToPend = () => {
    currentDash.value = 'FirstOrderPend'
}
const changeToProgress = ()=> {
    currentDash.value = 'FirstOrderProgress'
}

</script>
