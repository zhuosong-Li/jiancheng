<template>
    <el-tabs v-model="editableTabsValue" type="card" class="demo-tabs" @edit="handleTabsEdit">
        <el-tab-pane label="材料价格与成本趋势" name="1" :closable="false">
            <MaterialData  @edit="handleTabsEdit"/>
        </el-tab-pane>
        <el-tab-pane
            v-for="item in editableTabs"
            :key="item.name"
            :label="item.title"
            :name="item.name"
            :closable="item.closable"
        >
            <component
                :is="item.content"
                :materialName="item.needQuery ? item.name : undefined"
            ></component>
        </el-tab-pane>
    </el-tabs>
</template>
<script setup lang="js">
import MaterialData from './MaterialData.vue';
import HistoryTrend from './HistoryTrend.vue';
import { ref } from 'vue';

const editableTabsValue = ref('1');
const editableTabs = ref([]);

const handleTabsEdit = (targetName, action) => {
    if (action === 'add') {
        editableTabs.value.push({
            title: targetName + '历史价格数据曲线',
            name: targetName,
            content: HistoryTrend,
            closable: true,
            needQuery: true
        });
        editableTabsValue.value = targetName;
    } else if (action === 'remove') {
        const tabs = editableTabs.value;
        let activeName = editableTabsValue.value;
        if (activeName === targetName) {
            tabs.forEach((tab, index) => {
                if (tab.name === targetName) {
                    const nextTab = tabs[index + 1] || tabs[index - 1];
                    if (nextTab) {
                        activeName = nextTab.name;
                    } else {
                        activeName = '1';
                    }
                }
            })
        }
        editableTabsValue.value = activeName;
        editableTabs.value = tabs.filter((tab) => tab.name !== targetName);
    }
}
</script>

<style>
.demo-tabs > .el-tabs__content {
    color: #6b778c;
}
.demo-tabs {
    height: calc(100% - 40px);
    width: calc(100% - 40px);
}
.el-tab-pane {
    height: 100%;
    overflow: auto;
}
</style>
