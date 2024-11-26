<template>
    <el-timeline style="max-width: 100%">
        <el-timeline-item
            v-for="(activity, index) in activities"
            :key="index"
            :timestamp="activity.handleTime"
        >
            <el-card>
                <p>操作名称：{{ activity.operationName }}</p>
                <p>源状态：{{ activity.operationModifiedStatus }}</p>
            </el-card>
        </el-timeline-item>
    </el-timeline>
</template>

<script lang="js" setup>
import { MoreFilled } from '@element-plus/icons-vue'
import { onMounted, ref, getCurrentInstance } from 'vue'
import axios from 'axios'

const { orderId } = defineProps(['orderId'])
let activities = ref([])
const $api_baseUrl = getCurrentInstance().appContext.config.globalProperties.$apiBaseUrl
const routeMsg = `${$api_baseUrl}/headmanager/getordershoetimeline`

onMounted(() => {
    // 组件创建时立马根据鞋型id去查询相关时间线数据
    queryOrderMsg(orderId)
})

async function queryOrderMsg(orderId) {
    // 后续需放开进行根据订单id查询时间线数据，显示对应状态
    if (orderId) {
        const params = { 'orderId': orderId }
        try {
            const response = await axios.get(routeMsg, {params});
            activities.value = response.data;
            activities.value.reverse();
        }
        catch(error) {
            console.log(error)
        }

    }
}
</script>

<style scoped></style>
