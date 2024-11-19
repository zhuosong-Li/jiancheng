<template>
    <el-timeline style="max-width: 100%">
        <el-timeline-item
            v-for="(activity, index) in activities"
            :key="index"
            :icon="activity.icon"
            :type="activity.type"
            :color="activity.color"
            :size="activity.size"
            :hollow="activity.hollow"
            :timestamp="activity.timestamp"
        >
            <el-card>
                <h4>{{ activity.timestamp }}</h4>
                <p>{{ activity.content }}</p>
            </el-card>
        </el-timeline-item>
    </el-timeline>
</template>

<script lang="js" setup>
import { MoreFilled } from '@element-plus/icons-vue'
import { onMounted, ref } from 'vue'
import axios from 'axios'

const { orderId } = defineProps(['orderId'])
let activities = ref([])

onMounted(() => {
    // 组件创建时立马根据鞋型id去查询相关时间线数据
    queryOrderMsg(orderId)
})

async function queryOrderMsg(orderId) {
    // 后续需放开进行根据订单id查询时间线数据，显示对应状态
    // if (orderId) {
    //     const response = await axios.get(`${apiBaseUrl}/后续路由`, { 'orderId': orderId });
    //     activities.value = response.data.result;
    // }
    activities.value = [
        {
            content: orderId,
            timestamp: '2018-04-12 20:46',
            size: 'large',
            type: 'primary',
            icon: MoreFilled
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46',
            color: '#0bbd87'
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46',
            size: 'large'
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46',
            type: 'primary',
            hollow: true
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46'
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46',
            type: 'primary',
            hollow: true
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46'
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46',
            type: 'primary',
            hollow: true
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46'
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46',
            type: 'primary',
            hollow: true
        },
        {
            content: orderId,
            timestamp: '2018-04-03 20:46'
        }
    ]
}
</script>

<style scoped></style>
