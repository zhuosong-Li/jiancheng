<template>
    <el-row :gutter="20">
        <el-col :span="24">
            <el-table :data="tableData" border>
                <el-table-column prop="orderRId" label="订单号"></el-table-column>
                <el-table-column prop="shoeRId" label="工厂型号"></el-table-column>
                <el-table-column prop="outboundRId" label="单号"></el-table-column>
                <el-table-column prop="timestamp" label="操作时间"></el-table-column>
                <el-table-column label="出库类型">
                    <template #default="scope">
                        {{ determineOutboundType(scope.row.outboundType) }}
                    </template>
                </el-table-column>
                <el-table-column label="出库至">
                    <template #default="scope">
                        {{ determineDestination(scope.row, scope.row.outboundType) }}
                    </template>
                </el-table-column>
                <el-table-column label="查看">
                    <template #default="scope">
                        <el-button type="primary" @click="handleView(scope.row)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="total" />
        </el-col>
    </el-row>

    <el-dialog title="出库单详情" v-model="dialogVisible" width="80%">
        <!-- <div :id="`outboundRecipt`" style="padding:10px;background-color:#fff;">
            <el-card>
                <h2 style="text-align: center; margin-bottom: 10px">{{ `健诚鞋业出库单${currentRow.outboundRId}` }}</h2>
                <el-descriptions :column="4" border>
                    <el-descriptions-item label="订单号">{{ currentRow.orderRId }}</el-descriptions-item>
                    <el-descriptions-item label="工厂型号">{{ currentRow.shoeRId }}</el-descriptions-item>
                    <el-descriptions-item label="出库时间">{{ currentRow.timestamp }}</el-descriptions-item>
                    <el-descriptions-item label="出库方式">{{
                        determineOutboundType(currentRow.outboundType) }}</el-descriptions-item>
                </el-descriptions>
                <el-table v-if="recordData['material'].length > 0" :data="recordData['material']" border>
                    <el-table-column prop="materialName" label="材料名称"></el-table-column>
                    <el-table-column prop="materialModel" label="材料型号"></el-table-column>
                    <el-table-column prop="materialSpecification" label="材料规格"></el-table-column>
                    <el-table-column prop="colorName" label="颜色"></el-table-column>
                    <el-table-column prop="materialUnit" label="单位"></el-table-column>
                    <el-table-column prop="outboundQuantity" label="出库数量">
                    </el-table-column>
                    <el-table-column prop="remark" label="备注">
                    </el-table-column>
                </el-table>
                <el-table v-if="recordData['sizeMaterial'].length > 0" :data="recordData['sizeMaterial']" border>
                    <el-table-column prop="materialName" label="材料名称"></el-table-column>
                    <el-table-column prop="materialModel" label="材料型号"></el-table-column>
                    <el-table-column prop="materialSpecification" label="材料规格"></el-table-column>
                    <el-table-column prop="colorName" label="颜色"></el-table-column>
                    <el-table-column prop="materialUnit" label="单位"></el-table-column>
                    <el-table-column v-for="column in recordData.shoeSizeColumns" :key="column.prop"
                        :prop="column.prop" :label="column.label" width="55">
                    </el-table-column>
                    <el-table-column prop="remark" label="备注">
                    </el-table-column>
                </el-table>
                <template #footer>
                    <el-descriptions v-if="currentRow.outboundType == 0" :column="4" border>
                        <el-descriptions-item label="出库至">{{ currentRow.outboundDepartment
                            }}</el-descriptions-item>
                        <el-descriptions-item label="领料人">{{ currentRow.picker }}</el-descriptions-item>
                    </el-descriptions>
                    <el-descriptions v-else-if="currentRow.outboundType == 2" :column="4" border>
                        <el-descriptions-item label="外包工厂">
                            {{ currentRow.outsourceFactoryName }}
                        </el-descriptions-item>
                        <el-descriptions-item label="出库地址">{{ currentRow.outboundAddress }}</el-descriptions-item>
                    </el-descriptions>
                    <el-descriptions v-else-if="currentRow.outboundType == 3" :column="4" border>
                        <el-descriptions-item label="复合工厂">{{
                            currentRow.compositeSupplierName }}</el-descriptions-item>
                        <el-descriptions-item label="出库地址">{{ currentRow.outboundAddress }}</el-descriptions-item>
                    </el-descriptions>
                </template>
            </el-card>
        </div> -->
        <div id="printView" style="padding-left: 20px; padding-right: 20px;color:black; font-family: SimSun;">
            <h2 style="text-align: center;">健诚鞋业出库单</h2>
            <div style="display: flex; justify-content: flex-end; padding: 5px;">
                <span style="font-weight: bolder;font-size: 16px;">
                    单据编号：{{ currentRow.outboundRId }}
                </span>
            </div>
            <table class="table" border="0pm" cellspacing="0" align="left" width="100%"
                style="font-size: 16px;margin-bottom: 10px; table-layout:fixed;word-wrap:break-word;word-break:break-all">
                <tr>
                    <td style="padding:5px;" align="left">订单号:{{ currentRow.orderRId }}</td>
                    <td style="padding:5px;" align="left">工厂型号:{{ currentRow.shoeRId }}</td>
                    <td style="padding:5px;" align="left">出库时间:{{ currentRow.timestamp }}</td>
                    <td style="padding:5px;" align="left">出库方式:{{ determineOutboundType(currentRow.outboundType) }}</td>
                </tr>
            </table>
            <table v-if="recordData['material'].length > 0" class="yk-table" border="1pm" cellspacing="0" align="center" width="100%"
                style="font-size: 16px; table-layout:fixed;word-wrap:break-word;word-break:break-all">
                <tr>
                    <th width="55">序号</th>
                    <th>材料名</th>
                    <th>型号</th>
                    <th>规格</th>
                    <th width="80">颜色</th>
                    <th width="55">单位</th>
                    <th width="100">数量</th>
                    <th>备注</th>
                </tr>
                <tr v-for="(item, index) in recordData['material']" :key="index" align="center">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.materialName }}</td>
                    <td>{{ item.materialModel }}</td>
                    <td>{{ item.materialSpecification }}</td>
                    <td>{{ item.colorName }}</td>
                    <td>{{ item.materialUnit }}</td>
                    <td>{{ item.outboundQuantity }}</td>
                    <td>{{ item.remark }}</td>
                </tr>
            </table>
            <table v-if="recordData['sizeMaterial'].length > 0" class="yk-table" border="1pm" cellspacing="0" align="center" width="100%"
                style="font-size: 16px; table-layout:fixed;word-wrap:break-word;word-break:break-all">
                <tr>
                    <th width="55">序号</th>
                    <th>材料名</th>
                    <th>型号</th>
                    <th>规格</th>
                    <th width="80">颜色</th>
                    <th width="55">单位</th>
                    <th width="55" v-for="column in recordData.shoeSizeColumns" :key="column.prop">{{ column.label }}</th>
                    <th>备注</th>
                </tr>
                <tr v-for="(item, index) in recordData['sizeMaterial']" :key="index" align="center">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.materialName }}</td>
                    <td>{{ item.materialModel }}</td>
                    <td>{{ item.materialSpecification }}</td>
                    <td>{{ item.colorName }}</td>
                    <td>{{ item.materialUnit }}</td>
                    <td v-for="column in recordData.shoeSizeColumns" :key="column.prop">{{ item[column.prop] }}</td>
                    <td>{{ item.remark }}</td>
                </tr>
            </table>
            <div style="margin-top: 20px; font-size: 16px; font-weight: bold;">
                <div v-if="currentRow.outboundType == 0" style="display: flex;">
                    <span style="padding-right: 10px;">合计数量: <span style="text-decoration: underline;">{{
                            calculateInboundTotal() }}</span>
                    </span>
                    <span style="padding-right: 10px;">出库至: <span style="text-decoration: underline;">{{
                            currentRow.outboundDepartment }}</span>
                    </span>
                    <span style="padding-right: 10px;">领料人: <span style="text-decoration: underline;">{{
                            currentRow.picker }}</span>
                    </span>
                </div>
                <div v-else-if="currentRow.outboundType == 2" style="display: flex;">
                    <span style="padding-right: 10px;">合计数量: <span style="text-decoration: underline;">{{
                            calculateInboundTotal() }}</span>
                    </span>
                    <span style="padding-right: 10px;">外包工厂: <span style="text-decoration: underline;">{{
                            currentRow.outsourceFactoryName }}</span>
                    </span>
                    <span style="padding-right: 10px;">出库地址: <span style="text-decoration: underline;">{{
                            currentRow.outboundAddress }}</span>
                    </span>
                </div>
                <div v-else-if="currentRow.outboundType == 3" style="display: flex;">
                    <span style="padding-right: 10px;">合计数量: <span style="text-decoration: underline;">{{
                            calculateInboundTotal() }}</span>
                    </span>
                    <span style="padding-right: 10px;">复合工厂: <span style="text-decoration: underline;">{{
                            currentRow.compositeSupplierName }}</span>
                    </span>
                    <span style="padding-right: 10px;">出库地址: <span style="text-decoration: underline;">{{
                            currentRow.outboundAddress }}</span>
                    </span>
                </div>
            </div>
        </div>
        <template #footer>
            <el-button type="primary" @click="dialogVisible = false">返回</el-button>
            <el-button type="primary" v-print="'#printView'">打印</el-button>
            <el-button type="primary"
                @click="downloadPDF(`健诚鞋业出库单${currentRow.outboundRId}`, `printView`)">下载PDF</el-button>
        </template>
    </el-dialog>
</template>
<script>
import axios from 'axios'
import { ElMessage } from 'element-plus';
import htmlToPdf from '@/Pages/utils/htmlToPdf';
export default {
    data() {
        return {
            currentPage: 1,
            pageSize: 10,
            tableData: [],
            total: 0,
            currentRow: {},
            recordData: {},
            dialogVisible: false,
        }
    },
    mounted() {
        this.getOutboundRecordsTable()
    },
    methods: {
        calculateInboundTotal() {
            // Calculate the total inbound quantity
            const number = this.recordData.material.reduce((total, item) => {
                return total + (Number(item.outboundQuantity) || 0);
            }, 0);
            return Number(number).toFixed(2);
        },
        determineDestination(row, type) {
            if (type == 0) {
                return row.outboundDepartment
            }
            else if (type == 1) {
                return "废料处理"
            }
            else if (type == 2) {
                return row.outboundAddress
            }
            else if (type == 3) {
                return row.compositeSupplierName
            }
            else {
                return "未知"
            }
        },
        determineOutboundType(type) {
            if (type == 0) {
                return "自产出库"
            }
            else if (type == 1) {
                return "废料处理"
            }
            else if (type == 2) {
                return "外包发货"
            }
            else if (type == 3) {
                return "外发复合"
            }
            else {
                return "未知"
            }
        },
        downloadPDF(title, domName) {
            htmlToPdf.getPdf(title, domName);
        },
        async getOutboundRecordsTable() {
            try {
                let params = {
                    page: this.currentPage,
                    pageSize: this.pageSize
                }
                let response = await axios.get(`${this.$apiBaseUrl}/warehouse/getmaterialoutboundrecords`, { params })
                this.tableData = response.data.result
                this.total = response.data.total
            }
            catch (error) {
                console.log(error)
            }
        },
        handleSizeChange(val) {
            this.pageSize = val
            this.getOutboundRecordsTable()
        },
        handlePageChange(val) {
            this.page = val
            this.getOutboundRecordsTable()
        },
        async handleView(row) {
            this.currentRow = row
            console.log(row)
            try {
                let params = { "outboundBatchId": row.outboundBatchId, "orderId": row.orderId }
                if (this.currentRow.outboundRId.startsWith("N")) {
                    params["materialCategory"] = 0
                }
                else {
                    params["materialCategory"] = 1
                }
                let response = await axios.get(`${this.$apiBaseUrl}/warehouse/getoutboundrecordbybatchid`, { params })
                this.recordData["material"] = response.data.material
                this.recordData["sizeMaterial"] = response.data.sizeMaterial
                this.recordData["shoeSizeColumns"] = response.data.shoeSizeColumns
                console.log(this.recordData)

                this.dialogVisible = true
            }
            catch (error) {
                console.log(error)
                ElMessage.error('获取出库单详情失败')
            }
        }
    }
}
</script>