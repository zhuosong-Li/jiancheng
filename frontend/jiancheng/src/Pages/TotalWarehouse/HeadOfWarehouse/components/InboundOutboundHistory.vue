<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center">入库/出库历史记录</el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <el-tabs v-model="currentTab" type="border-card" tab-position="top" @tab-click="">
                <el-tab-pane v-for="item in panes" :key="item.key" :label="item.label" :name="item.key">
                    <el-row :gutter="20">
                        <el-col :span="24" :offset="0">
                            <div v-if="item.key === 1">
                                <MaterialStorage></MaterialStorage>
                            </div>
                            <div v-else-if="item.key === 2">
                                <SemifinishedStorage></SemifinishedStorage>
                            </div>
                            <div v-else>
                                <FinishedStorage></FinishedStorage>
                            </div>
                        </el-col>
                    </el-row>
                </el-tab-pane>
            </el-tabs>
        </el-col>
    </el-row>
</template>
<script>
import MaterialStorage from './InOutboundHistory/MaterialStorage.vue';
import SemifinishedStorage from './InOutboundHistory/SemifinishedStorage.vue';
import FinishedStorage from './InOutboundHistory/FinishedStorage.vue';
export default {
    components: {
        MaterialStorage,
        SemifinishedStorage,
        FinishedStorage
    },
    data() {
        return {
            currentTab: 1,
            panes: [
                {
                    label: '材料仓',
                    key: 1
                },
                {
                    label: '半成品仓',
                    key: 2
                },
                {
                    label: '成品仓',
                    key: 3
                }
            ],
        }
    },
}
</script>
