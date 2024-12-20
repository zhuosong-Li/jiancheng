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
                            <span>用户管理</span>
                        </el-menu-item>
                        <el-menu-item index="4" @click="handleMenuClick(4)">
                            <span>人员管理</span>
                        </el-menu-item>
                        <el-menu-item index="3" @click="handleMenuClick(3)">
                            <span>个人页面</span>
                        </el-menu-item>
                        <el-menu-item index="9" @click="handleMenuClick(9)">
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
import UserManagementView from '../components/UserManagementView.vue';
import StaffManagementView from '../components/StaffManagementView.vue';
import PersonalInfo from '@/components/PersonalInfo.vue';
import axios from 'axios'



export default {
    components: {
        AllHeader,
        UserManagementView,
        StaffManagementView,
        PersonalInfo
    },
    data() {
        return {
            UserFilled,
            currentComponent: 'UserManagementView',
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
                case 2:
                    this.currentComponent = 'UserManagementView'
                    break
                case 3:
                    this.currentComponent = 'PersonalInfo'
                    break
                case 4:
                    this.currentComponent = 'StaffManagementView'
                    break
                case 9:
                    this.Logout()
                    break
            }
        },
        async Logout() {
            await axios.post(`${this.$apiBaseUrl}/logout`)
                .then(response => {
                    this.$router.push({name: 'login'})
                    localStorage.removeItem('token')
                    localStorage.removeItem('role')
                })
        }
    }
}
</script>