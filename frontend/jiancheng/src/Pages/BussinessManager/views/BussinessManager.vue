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
                    业务部经理-姓名
                </div>
                <div class="aside-menu" style="width: 100%; margin-top: 50px;">
                    <el-menu default-active="2" class="el-menu-vertical-demo">
                        <el-menu-item index="2" @click="handleMenuClick(2)">
                            <span>订单管理</span>
                        </el-menu-item>
                        <el-menu-item index="3" @click="handleMenuClick(3)">
                            <span>客户管理</span>
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
import OrderImport from '../components/OrderImport.vue';
import CustomerManagement from '../components/CustomerManagement.vue';


export default {
    components: {
        AllHeader,
        OrderImport,
        CustomerManagement
    },
    data() {
        return {
            UserFilled,
            currentComponent: 'OrderImport'
        }
    },
    mounted() {
        this.$setAxiosToken()
    },
    methods: {
        handleMenuClick(index) {
            switch (index) {
                case 1:
                    this.currentComponent = 'Dashboard'
                    break
                case 2:
                    this.currentComponent = 'OrderImport'
                    break
                case 3:
                    this.currentComponent = 'CustomerManagement'
                    break
                case 9:
                    this.$router.push('/')
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