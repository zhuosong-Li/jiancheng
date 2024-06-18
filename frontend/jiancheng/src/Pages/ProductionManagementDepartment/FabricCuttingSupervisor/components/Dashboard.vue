<template>
    <el-row :gutter="20">
        <el-col :span="6" v-for="(content, index) in tasks" :key="index">
            <el-card style="max-width: 480px" shadow="hover">
                <template #header>
                <div class="card-header">
                    <span>{{ "订单号: " + content.orderNumber }}</span>
                </div>
                </template>
                <p>{{ content.name }}</p>
                <template #footer>{{ "创建日期：" + content.createdDate }}</template>
            </el-card>
        </el-col>
    </el-row>
</template>

<script setup>
import AllHeader from '@/components/AllHeader.vue'
import Sidebar from './Sidebar.vue';
import { useRouter } from 'vue-router'
import { ref } from 'vue';
const names = ["针车工价填报"]
const tasks = ref([
    {
        orderNumber: "1001",
        name: names[0],
        createdDate: "2024-06-01"
    },
    {
        orderNumber: "1002",
        name: names[0],
        createdDate: "2024-06-01"
    }
])
</script>
