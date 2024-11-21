<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0">
            <MaterialStorage></MaterialStorage>
        </el-col>
    </el-row>
</template>
<script>
import MaterialStorage from './MaterialStorage.vue';
export default {
    components: {
        MaterialStorage,
    },
}
</script>
