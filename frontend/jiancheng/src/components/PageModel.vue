<template>
    <el-container>
        <el-header>
            <AllHeader></AllHeader>
        </el-header> <!--引用header-->
        <el-container>
            <el-aside><!--引用aside-->
                <el-row>
                    <div>
                        <el-avatar :icon="UserFilled" />
                    </div>
                </el-row>
                <el-row>
                    <div class="aside-menu">
                        <el-menu default-active="2" class="el-menu-vertical-demo" @open="handleOpen"
                            @close="handleClose">
                            <el-sub-menu index="1">
                                <template #title>
                                    <el-icon>
                                        <location />
                                    </el-icon>
                                    <span>Navigator One</span>
                                </template>
                                <el-menu-item-group title="Group One">
                                    <el-menu-item index="1-1">item one</el-menu-item>
                                    <el-menu-item index="1-2">item two</el-menu-item>
                                </el-menu-item-group>
                                <el-menu-item-group title="Group Two">
                                    <el-menu-item index="1-3">item three</el-menu-item>
                                </el-menu-item-group>
                                <el-sub-menu index="1-4">
                                    <template #title>item four</template>
                                    <el-menu-item index="1-4-1">item one</el-menu-item>
                                </el-sub-menu>
                            </el-sub-menu>
                            <el-menu-item index="2">
                                <el-icon><icon-menu /></el-icon>
                                <span>Navigator Two</span>
                            </el-menu-item>
                            <el-menu-item index="3" disabled>
                                <el-icon>
                                    <document />
                                </el-icon>
                                <span>Navigator Three</span>
                            </el-menu-item>
                            <el-menu-item index="4">
                                <el-icon>
                                    <setting />
                                </el-icon>
                                <span>Navigator Four</span>
                            </el-menu-item>
                        </el-menu>
                    </div>
                </el-row>
            </el-aside>
            <el-main> <!--引用main-->
                main
            </el-main>
        </el-container>
    </el-container>

</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
export default {
    components: {
        AllHeader,
    }
}
</script>