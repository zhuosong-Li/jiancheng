<template>
    <el-container>
        <el-header>
            <AllHeader></AllHeader>
        </el-header> <!--引用header-->
        <el-container>
            <el-aside><!--引用aside-->
                <div>
                    <el-avatar :icon="UserFilled" :size="100" />
                </div>
                <div style="font-size: x-large;">
                    {{ userName }}
                </div>
                <div class="aside-menu" style="width: 100%; margin-top: 50px;">
                    <el-menu default-active="1" class="el-menu-vertical-demo">
                        <el-menu-item index="1" @click="handleMenuClick(1)">
                            <span>材料入库</span>
                        </el-menu-item>
                        <el-menu-item index="2" @click="handleMenuClick(2)">
                            <span>材料出库</span>
                        </el-menu-item>
                        <el-menu-item index="3" @click="handleMenuClick(3)">
                            <span>生产动态明细</span>
                        </el-menu-item>
                        <el-menu-item index="4" @click="handleMenuClick(4)">
                            <span>文件下载</span>
                        </el-menu-item>
                        <el-menu-item index="5" @click="handleMenuClick(5)">
                            <span>出/入库历史</span>
                        </el-menu-item>
                        <el-menu-item index="6" @click="handleMenuClick(6)">
                            <span>独立采购</span>
                        </el-menu-item>
                        <el-menu-item index="6" @click="handleMenuClick(7)">
                            <span>码段管理</span>
                        </el-menu-item>
                        <el-menu-item index="8" @click="logout">
                            <span>退出系统</span>
                        </el-menu-item>
                    </el-menu>
                </div>
            </el-aside>
            <el-main> <!--引用main-->
                <component :is="currentComponent"></component>
            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import Dashboard from '../components/HeadOfWarehouseDashboard.vue'
import MaterialInbound from '../components/MaterialInbound.vue'
import InboundOutboundHistory from '../components/InboundOutboundHistory.vue'
import MaterialOutbound from '../components/MaterialOutbound.vue'
import FileDownload from '../components/FileDownload.vue'
import OrderProgress from '@/Pages/ProductionManagementDepartment/ProductionSharedPages/OrderProgress.vue'
import { UserFilled } from '@element-plus/icons-vue'
import axios from 'axios'
import { logout } from '@/Pages/utils/logOut'
import InboundView from '../components/InboundView.vue'
import OutboundView from '../components/OutboundView.vue'
import FixedAssetsConsumablesView from '@/Pages/LogisticsControlDepartment/LogisticsControlManager/components/FixedAssetsConsumablesView.vue'
import LogisticsBatchTypeManagement from '@/components/LogisticsBatchInfoTypeManagement.vue'

export default {
    components: {
        AllHeader,
        Dashboard,
        MaterialInbound,
        MaterialOutbound,
        InboundOutboundHistory,
        FileDownload,
        OrderProgress,
        InboundView,
        OutboundView,
        FixedAssetsConsumablesView,
        LogisticsBatchTypeManagement
    },
    data() {
        return {
            UserFilled,
            currentComponent:'InboundView',
            userName: '',
            logout
        }
    },
    mounted() {
        this.$setAxiosToken()
        this.getUserAndCharacter()
    },
    methods: {
        async getUserAndCharacter() {
            const response = await axios.get(`${this.$apiBaseUrl}/general/getcurrentstaffandcharacter`)
            this.userName = response.data.staffName + '-' + response.data.characterName
        },
        handleMenuClick(index){
            switch(index) {
                case 1:
                    this.currentComponent = 'InboundView'
                    break
                case 2:
                    this.currentComponent = 'OutboundView'
                    break
                case 3:
                    this.currentComponent = 'OrderProgress'
                    break
                case 4:
                    this.currentComponent = 'FileDownload' 
                    break
                case 5:
                    this.currentComponent = 'InboundOutboundHistory'
                    break
                case 6:
                    this.currentComponent = 'FixedAssetsConsumablesView'
                case 7:
                    this.currentComponent = 'LogisticsBatchTypeManagement'
                    break
            }
        }
    }
}
</script>