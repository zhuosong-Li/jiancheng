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
                    技术部经理-姓名
                </div>
                <div class="aside-menu" style="width: 100%; margin-top: 50px;">
                    <el-menu default-active="1" class="el-menu-vertical-demo">
                        <el-menu-item index="1" @click="handleMenuClick(1)">
                            <span>任务看板</span>
                        </el-menu-item>
                        <el-menu-item index="2" @click="handleMenuClick(2)">
                            <span>调版分配与下发</span>
                        </el-menu-item>
                        <el-menu-item index="9" @click="logout">
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
import { UserFilled } from '@element-plus/icons-vue'
import Dashboard from '../components/TechnicalManagerDashboard.vue';
export default {
    components: {
        AllHeader,
        Dashboard,
    },
    data() {
        return {
            UserFilled,
            currentComponent: 'Dashboard'
        }
    },
    mounted() {
        this.$setAxiosToken()
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
            }
        },
        async logout() {
            await this.$axios.post(`${this.$apiBaseUrl}/logout`)
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
}
</script>