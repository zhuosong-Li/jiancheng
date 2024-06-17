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
                    技术部BOM文员-姓名
                </div>
                <div class="aside-menu" style="width: 100%; margin-top: 50px;">
                    <el-menu default-active="1" class="el-menu-vertical-demo">
                        <el-menu-item index="1" @click="handleMenuClick(1)">
                            <span>任务看板</span>
                        </el-menu-item>
                        <el-menu-item index="2" @click="handleMenuClick(2)">
                            <span>一次BOM表填写</span>
                        </el-menu-item>
                        <el-menu-item index="3" @click="handleMenuClick(3)">
                            <span>二次BOM表填写</span>
                        </el-menu-item>
                        <el-menu-item index="9">
                            <span>退出系统</span>
                        </el-menu-item>
                        <el-menu-item index="10" @click="handleMenuClick(10)">
                            <span>测试页面</span>
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
import { UserFilled } from '@element-plus/icons-vue'
import Dashboard from '../components/TechnicalClerkDashboard.vue';
import FirstBOMCreate from '../components/FirstBOMListView.vue';
import SecondBOMCreate from '../components/SecondBOMListView.vue'
export default {
    components: {
        AllHeader,
        Dashboard,
        FirstBOMCreate,
        SecondBOMCreate
    },
    data() {
        return {
            UserFilled,
            currentComponent: 'Dashboard'
        }
    },
    methods: {
        handleMenuClick(index) {
            console.log(index)
            switch (index) {
                case 1:
                    this.currentComponent = 'Dashboard'
                    break
                case 2:
                    this.currentComponent = 'FirstBOMCreate'
                    break
                case 3:
                    this.currentComponent = 'SecondBOMCreate'
                    break
                case 4:
                    this.currentComponent = 'FixedAssets'
                    break
                case 5:
                    this.currentComponent = 'MaterialManagement'
                    break
                case 6:
                    this.currentComponent = 'WarehouseManagement'
                    break
                case 7:
                    this.currentComponent = 'SupplierManagement'
                    break
                case 10:
                    this.currentComponent = 'TestPage'
            }
        }
    }
}
</script>