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
                            <span>半成品入库/出库</span>
                        </el-menu-item>
                        <el-menu-item index="4" @click="handleMenuClick(4)">
                            <span>成品入库/出库</span>
                        </el-menu-item>
                        <el-menu-item index="6" @click="handleMenuClick(5)">
                            <span>出/入库历史</span>
                        </el-menu-item>
                        <el-menu-item index="7">
                            <span>个人信息</span>
                        </el-menu-item>
                        <el-menu-item index="8">
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
import FirstWarehousing from '../components/FirstWarehousingListView.vue'
import SecondWarehousing from '../components/SecondPurchaseListView.vue'
import MaterialInbound from '../components/MaterialInbound.vue'
import InboundOutboundHistory from '../components/InboundOutboundHistory.vue'
import SemiInboundOutbound from '../components/SemiInboundOutbound.vue'
import FinishedInboundOutbound from '../components/FinishedInboundOutbound.vue'
import MaterialOutbound from '../components/MaterialOutbound.vue'
import { UserFilled } from '@element-plus/icons-vue'
import axios from 'axios'
export default {
    components: {
        AllHeader,
        Dashboard,
        FirstWarehousing,
        SecondWarehousing,
        MaterialInbound,
        MaterialOutbound,
        InboundOutboundHistory,
        SemiInboundOutbound,
        FinishedInboundOutbound,
    },
    data() {
        return {
            UserFilled,
            currentComponent:'MaterialInbound',
            userName: ''
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
                    this.currentComponent = 'MaterialInbound'
                    break
                case 2:
                    this.currentComponent = 'MaterialOutbound' 
                    break
                case 3:
                    this.currentComponent = 'SemiInboundOutbound'
                    break
                case 4:
                    this.currentComponent = 'FinishedInboundOutbound'
                    break
                case 5:
                    this.currentComponent = 'InboundOutboundHistory'
                    break
            }
        }
    }
}
</script>