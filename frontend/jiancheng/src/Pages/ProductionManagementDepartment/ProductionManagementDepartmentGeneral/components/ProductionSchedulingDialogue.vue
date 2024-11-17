<template>
  <el-row :gutter="20">
    <el-col :span="6" :offset="20"
      ><el-button-group>
        <el-button type="default" size="default" :icon="Memo" @click="changeToList">列表视图</el-button>
        <el-button type="default" size="default" :icon="Calendar" @click="changeToSchedule">日历视图</el-button>
      </el-button-group>
    </el-col>
  </el-row>
  <component :is="currentComponent" style="margin-top: 20px;"></component>
</template>

<script>
import { Calendar, Memo } from '@element-plus/icons-vue'
import ListView from './ProductionInfo/TableView.vue'
import ScheduleView from './ProductionInfo/ScheduleView.vue'

export default {
  components: {
    ListView,
    ScheduleView
  },
  data() {
    return {
      Calendar,
      Memo,
      currentComponent: "ListView"
    }
  },
  methods: {
    changeToSchedule() {
      this.currentComponent = "ScheduleView"
    },
    changeToList() {
      this.currentComponent = "ListView"
    }
  }
}
</script>

<style>
.vuecal__event.leisure {
  background-color: rgba(253, 156, 66, 0.9);
  border: 1px solid rgb(233, 136, 46);
  color: #fff;
}
.vuecal__event.sport {
  background-color: rgba(255, 102, 102, 0.9);
  border: 1px solid rgb(235, 82, 82);
  color: #fff;
}
</style>
