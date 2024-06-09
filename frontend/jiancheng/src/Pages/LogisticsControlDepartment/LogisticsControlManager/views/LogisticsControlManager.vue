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
                    物控经理-姓名
                </div>
                <div class="aside-menu" style="width: 100%; margin-top: 50px;">
                    <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
                        <el-menu-item index="1">
                            <span>任务看板</span>
                        </el-menu-item>
                        <el-menu-item index="2">
                            <span>一次采购订单生成</span>
                        </el-menu-item>
                        <el-menu-item index="3">
                            <span>二次采购订单生成</span>
                        </el-menu-item>
                        <el-menu-item index="4">
                            <span>订单查询</span>
                        </el-menu-item>
                        <el-menu-item index="5">
                            <span>个人信息</span>
                        </el-menu-item>
                        <el-menu-item index="6">
                            <span>退出系统</span>
                        </el-menu-item>
                    </el-menu>
                </div>
            </el-aside>
            <el-main> <!--引用main-->
                <Dashboard></Dashboard>
            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import Dashboard from '../components/LogisticsManagerDashboard.vue'
export default {
    components: {
        AllHeader,
        Dashboard
    }
}
</script>