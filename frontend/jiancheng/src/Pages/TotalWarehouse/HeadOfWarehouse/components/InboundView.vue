<template>
<el-tabs v-model="activeTab" tab-position="top" style="width: 100%;">
    <el-tab-pane label="原材料" name="原材料">
        <MaterialInbound></MaterialInbound>
    </el-tab-pane>
    <el-tab-pane label="复合材料" name="复合材料">
        <CompositeMaterialInbound></CompositeMaterialInbound>
    </el-tab-pane>
</el-tabs>
</template>
<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import MaterialInbound from './MaterialInbound.vue';
import CompositeMaterialInbound from './CompositeMaterialInbound.vue';
export default {
    components: {
        MaterialInbound,
        CompositeMaterialInbound
    },
    data() {
        return {
            activeTab: '原材料',
            tabs: [
                { label: "原材料", name: "原材料" },
                { label: "复合材料", name: "复合材料" }
            ],
        }
    }
}
</script>