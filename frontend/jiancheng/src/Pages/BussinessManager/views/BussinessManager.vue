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
                    <el-menu default-active="2" class="el-menu-vertical-demo">
                        <el-menu-item index="2" @click="handleMenuClick(2)">
                            <span>订单管理</span>
                        </el-menu-item>
                        <el-menu-item index="3" @click="handleMenuClick(3)">
                            <span>客户管理</span>
                        </el-menu-item>
                        <el-menu-item index="4" @click="handleMenuClick(4)">
                            <span>鞋型管理</span>
                        </el-menu-item>
                        <el-menu-item index="5" @click="handleMenuClick(5)">
                            <span>配码种类管理</span>
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
import OrderManagement from '../components/OrderManagement.vue';
import CustomerManagement from '../components/CustomerManagement.vue';
import axios from 'axios'
import ShoeTypeManagement from '@/components/ShoeTypeManagement.vue';
import BatchInfoTypeManagement from '../components/BatchInfoTypeManagement.vue';
export default {
    components: {
        AllHeader,
        OrderManagement,
        CustomerManagement,
        ShoeTypeManagement,
        BatchInfoTypeManagement
    },
    data() {
        return {
            UserFilled,
            currentComponent: 'OrderManagement',
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
        handleMenuClick(index) {
            switch (index) {
                case 1:
                    this.currentComponent = 'Dashboard'
                    break
                case 2:
                    this.currentComponent = 'OrderManagement'
                    break
                case 3:
                    this.currentComponent = 'CustomerManagement'
                    break
                case 4:
                    this.currentComponent = 'ShoeTypeManagement'
                    break
                case 5:
                    this.currentComponent = "BatchInfoTypeManagement"
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