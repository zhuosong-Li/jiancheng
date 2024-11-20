<template>
    <div class="content">
        <div>
            <el-date-picker
                v-model="timeValue"
                type="datetimerange"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                format="YYYY-MM-DD HH:mm:ss"
                date-format="YYYY/MM/DD ddd"
                time-format="A hh:mm:ss"
                style="height: 40px"
                :default-time="defaultTime"
            />
            <el-button type="primary" size="middle" style="margin-left: 50px" @click="filterData()"
                >筛选</el-button
            >
        </div>
        <div
            :id="'histroyTrend_' + materialName"
            class="historyTrend"
            style="
                width: 100%;
                height: 90%;
                display: flex;
                justify-content: center;
                align-items: center;
            "
        ></div>
    </div>
</template>

<script setup>
import { onMounted, watch, ref, nextTick } from 'vue'
import useHistoryMaterial from '../../hooks/useHistoryMaterial'
import axios from 'axios'
import * as echarts from 'echarts'

const { materialName } = defineProps(['materialName'])

const { materialData, getMaterialData } = useHistoryMaterial()

const defaultTime = ref([new Date(2024, 11, 1, 12, 0, 0), new Date(2024, 11, 15, 8, 0, 0)])
let timeValue = ref('')

let myChart;

onMounted(() => {
    getMaterialData(materialName)
    setTimeout(() => {
        materialData.value = {
            materialName: materialName,
            data: [
                {
                    date: '2024-11-01',
                    price: 10
                },
                {
                    date: '2024-11-02',
                    price: 20
                },
                {
                    date: '2024-11-03',
                    price: 30
                },
                {
                    date: '2024-11-04',
                    price: 17
                },
                {
                    date: '2024-11-05',
                    price: 31
                },
                {
                    date: '2024-11-06',
                    price: 21
                },
                {
                    date: '2024-11-07',
                    price: 8
                },
                {
                    date: '2024-11-08',
                    price: 14
                },
                {
                    date: '2024-11-09',
                    price: 18
                },
                {
                    date: '2024-11-10',
                    price: 20
                },
                {
                    date: '2024-11-11',
                    price: 15
                },
                {
                    date: '2024-11-12',
                    price: 30
                }
            ]
        }
    }, 2000)
    window.addEventListener('resize', ()=>{
        nextTick(()=>{
            myChart.resize();
        })
    });
})

watch(
    () => materialData,
    () => {
        // 基于准备好的dom，初始化echarts实例
        let chartDom = document.getElementById('histroyTrend_' + materialName)
        if (!echarts.getInstanceByDom(chartDom)) {
            myChart = echarts.init(chartDom)
        } else {
            myChart = echarts.getInstanceByDom(chartDom)
        }
        updateChart()
    },
    { deep: true }
)

function updateChart() {
    const data = materialData.value.data
    let xAxisData = []
    let yAxisData = []
    for (let i = 0; i < data.length; i++) {
        // 增加时间范围数据筛选
        // if (data[i].date >= defaultTime[0] && data[i].date <= defaultTime[1]) {
        xAxisData.push(data[i].date)
        yAxisData.push(data[i].price)
        // }
    }
    // 绘制图表
    myChart.setOption({
        xAxis: {
            type: 'category',
            data: xAxisData,
            name: '时间'
        },
        yAxis: {
            type: 'value',
            name: '单价'
        },
        series: [
            {
                data: yAxisData,
                type: 'line',
                name: materialData.value.materialName + '单价'
            }
        ],
        //简单的在图表配置中添加这个工具配置
        toolbox: {
            show: true,
            feature: {
                saveAsImage: {}
            }
        }
    })
}
</script>

<style scoped>
.content {
    display: flex;
    width: 100%;
    height: 90%;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
.historyTrend > div {
    width: 100% !important;
    height: 100% !important;
} 
</style>
