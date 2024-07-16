<template>
  <el-container>
    <el-header>
      <AllHeader></AllHeader>
    </el-header>
    <!--引用header-->
    <el-container>
      <!-- <el-menu default-active="1" 
                    class="el-menu-vertical-demo"
                    :collapse="isCollapse" 
                    @open="handleOpen" 
                    @close="handleClose">
                    <SideMenu></SideMenu>
            </el-menu> -->
      <el-aside>

        <div>
          <el-avatar :icon="UserFilled" :size="100" />
        </div>
        <div style="font-size: x-large">生产经理-姓名</div>

        <div class="aside-menu" style="width: 100%; margin-top: 50px;">
          <el-menu
            default-active="1"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
          >
            <el-menu-item index="1" @click="handleMenuClick(1)">
              <span>任务看板</span>
            </el-menu-item>
            <el-menu-item index="2" @click="handleMenuClick(2)">
              <span>生产排期表</span>
            </el-menu-item>
            <el-menu-item index="3" @click="handleMenuClick(3)">
              <span>物料信息</span>
            </el-menu-item>
            <el-menu-item index="5">
              <span>订单查询</span>
            </el-menu-item>
            <el-menu-item index="7">
              <span>数量审批</span>
            </el-menu-item>
            <el-menu-item index="8">
              <span>数据总览</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      <el-main>
        <component :is="currentComponent"></component>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import SideMenu from '../components/sideMenu.vue'
import todotaskDashboard from '../components/TodoTasksView.vue'
import LogisticInfo from '../components/LogisticInfo.vue'
import ProductionInfo from '../components/ProductionInfo.vue'
import ProductionSchedulingDialogue from '../components/ProductionSchedulingDialogue.vue'
import { UserFilled } from '@element-plus/icons-vue'
import { ref } from 'vue'

const isCollapse = ref(false)

export default {
  components: {
    AllHeader,
    todotaskDashboard,
    ProductionInfo,
    SideMenu,
    LogisticInfo,
    ProductionSchedulingDialogue
  },
  data() {
    return {
      UserFilled,
      currentComponent: 'todotaskDashboard'
    }
  },
  methods: {
    handleMenuClick(index) {
      console.log(index)
      switch (index) {
        case 1:
          this.currentComponent = 'todotaskDashboard'
          break
        case 2:
          this.currentComponent = 'ProductionSchedulingDialogue'
          break
        case 3:
          this.currentComponent = 'LogisticInfo'
          break
        case 4:
          this.currentComponent = 'ProductionInfo'
      }
    },
  }
}
</script>

