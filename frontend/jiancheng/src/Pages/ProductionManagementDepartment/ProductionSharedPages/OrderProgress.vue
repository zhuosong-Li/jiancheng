<template>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            <el-input v-model="orderRIdSearch" placeholder="请输入订单号" clearable @keypress.enter="getOrderDataTable"
                @clear="getOrderDataTable" />
        </el-col>
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            <el-input v-model="shoeRIdSearch" placeholder="请输入公司型号" clearable @keypress.enter="getOrderDataTable"
                @clear="getOrderDataTable" />
        </el-col>
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            <el-input v-model="customerProductNameSearch" placeholder="请输入客户型号" clearable
                @keypress.enter="getOrderDataTable" @clear="getOrderDataTable" />
        </el-col>
        <el-col :span="4" :offset="0" style="white-space: nowrap;">
            <el-select v-model="statusNodeSearch" placeholder="状态点查询" clearable
                @change="getOrderDataTable" @clear="getOrderDataTable">
                <el-option v-for="item in [
                        '未排期',
                        '已保存排期',
                        '等待生产开始',
                        '裁断中',
                        '针车预备中',
                        '针车中',
                        '成型中',
                        '生产结束',
                    ]" :key="item" :label="item" :value="item">
                    </el-option>
            </el-select>
        </el-col>
    </el-row>
    <el-button v-if="$props.editable && isMultipleSelection" @click="openMultipleShoesDialog">
        排产
    </el-button>
    <el-button v-if="$props.editable" @click="toggleSelectionMode">
        {{ isMultipleSelection ? "退出" : "选择鞋型" }}
    </el-button>
    <p v-if="isSelectedRowsEmpty">未选择鞋型</p>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24" :offset="0">
            <el-table :data="orderTableData" stripe border style="height: 600px"
                @selection-change="handleSelectionChange">
                <el-table-column v-if="isMultipleSelection" type="selection" width="55" />
                <el-table-column prop="orderRId" label="订单号" sortable></el-table-column>
                <el-table-column prop="shoeRId" label="公司型号" sortable></el-table-column>
                <el-table-column prop="customerProductName" label="客户型号" sortable></el-table-column>
                <el-table-column prop="colorName" label="颜色" sortable></el-table-column>
                <el-table-column prop="status" label="状态" sortable></el-table-column>
                <el-table-column prop="colorAmount" label="订单数量" sortable></el-table-column>

                <el-table-column label="裁断" header-align="center">
                    <el-table-column label="完成数/欠数" sortable>
                        <template #default="scope">
                            {{ scope.row.cuttingAmount + " / " + (scope.row.colorAmount - scope.row.cuttingAmount) }}
                        </template>
                    </el-table-column>
                    <el-table-column label="周期" width="200" header-align="center">
                        <template #default="scope">
                            <span v-if="scope.row.cuttingStartDate !== ''">
                                {{ scope.row.cuttingStartDate + " 至 " + scope.row.cuttingEndDate }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="cuttingLineGroup" label="线别" width="100" header-align="center" />
                </el-table-column>

                <el-table-column label="针车预备" header-align="center">
                    <el-table-column label="完成数/欠数" sortable>
                        <template #default="scope">
                            {{ scope.row.preSewingAmount + " / " + (scope.row.colorAmount - scope.row.preSewingAmount)
                            }}
                        </template>
                    </el-table-column>
                    <el-table-column label="周期" width="200" header-align="center">
                        <template #default="scope">
                            <span v-if="scope.row.preSewingStartDate !== ''">
                                {{ scope.row.preSewingStartDate + " 至 " + scope.row.preSewingEndDate }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="preSewingLineGroup" label="线别" width="100" header-align="center" />
                </el-table-column>

                <el-table-column label="针车" header-align="center">
                    <el-table-column prop="sewingAmount" label="完成数" sortable></el-table-column>
                    <el-table-column label="欠数" sortable>
                        <template #default="scope">
                            {{ scope.row.colorAmount - scope.row.sewingAmount }}
                        </template>
                    </el-table-column>
                    <el-table-column label="周期" width="200" header-align="center">
                        <template #default="scope">
                            <span v-if="scope.row.sewingStartDate !== ''">
                                {{ scope.row.sewingStartDate + " 至 " + scope.row.sewingEndDate }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sewingLineGroup" label="线别" width="100" header-align="center" />
                </el-table-column>

                <el-table-column label="成型" header-align="center">
                    <el-table-column prop="moldingAmount" label="完成数" sortable></el-table-column>
                    <el-table-column label="欠数" sortable>
                        <template #default="scope">
                            {{ scope.row.colorAmount - scope.row.moldingAmount }}
                        </template>
                    </el-table-column>
                    <el-table-column label="周期" width="200" header-align="center">
                        <template #default="scope">
                            <span v-if="scope.row.moldingStartDate !== ''">
                                {{ scope.row.moldingStartDate + " 至 " + scope.row.moldingEndDate }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="moldingLineGroup" label="线别" width="100" header-align="center" />
                </el-table-column>
                <el-table-column prop="orderEndDate" label="出货日期" sortable></el-table-column>
                <el-table-column label="物料">
                    <template #default="scope">
                        <el-button v-if="scope.row.isMaterialArrived == 0" type="warning" size="small"
                            @click="openLogisticsDialog(scope.row)">未到</el-button>
                        <el-button v-else-if="scope.row.isMaterialArrived == 1" type="success" size="small"
                            @click="openLogisticsDialog(scope.row)">已到</el-button>
                    </template>
                </el-table-column>
                <el-table-column label="工艺单">
                    <template #default="scope">
                        <el-button :disabled="scope.row.processSheetUploadStatus != 2"
                            v-if="scope.row.processSheetUploadStatus != 2" type="primary" size="small">
                            未下发
                        </el-button>
                        <el-button v-if="scope.row.processSheetUploadStatus == 2" type="primary" size="small"
                            @click="downloadProcessSheet(scope.row)">
                            下载
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="logisticsInfo" label="生产指令单">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click="downloadProductionOrderSheet(scope.row)">
                            下载
                        </el-button>
                    </template>
                </el-table-column>
                <!-- <el-table-column type="expand" label="工组信息" width="100">
                    <template #default="props">
                        <el-table :data="props.row.productionInfoArr" stripe border>
                            <el-table-column prop="team" label="工组"></el-table-column>
                            <el-table-column prop="producedAmount" label="完成数量"></el-table-column>
                            <el-table-column prop="lineGroup" label="工组线号"></el-table-column>
                            <el-table-column prop="startDate" label="开始日期"></el-table-column>
                            <el-table-column prop="endDate" label="结束日期"></el-table-column>
                        </el-table>
                    </template>
                </el-table-column> -->
                <el-table-column label="排产">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click="openScheduleDialog(scope.row)">
                            查看
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="12" :offset="14">
            <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper" :total="orderTotalRows" />
        </el-col>
    </el-row>
    <el-dialog title="鞋型所有材料物流信息" v-model="isMaterialLogisticVis" width="80%">
        <el-row :gutter="20">
            <el-col :span="24" :offset="0">
                <el-table :data="logisticsMaterialData" border stripe>
                    <el-table-column prop="materialType" label="材料类型"></el-table-column>
                    <el-table-column prop="materialName" label="材料名称"></el-table-column>
                    <el-table-column prop="colorName" label="颜色"></el-table-column>
                    <el-table-column prop="estimatedInboundAmount" label="核定用量"></el-table-column>
                    <el-table-column prop="actualInboundAmount" label="采购数量"></el-table-column>
                    <el-table-column prop="supplierName" label="供应商名称"></el-table-column>
                    <el-table-column prop="materialArrivalDate" label="材料预计到达日期"></el-table-column>
                    <el-table-column prop="status" label="材料状态"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="12" :offset="15">
                <el-pagination @size-change="handleSizeChange" @current-change="handlePageChange"
                    :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper" :total="logisticsRows" />
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button type="primary" @click="isMaterialLogisticVis = false">返回</el-button>
            </span>
        </template>
    </el-dialog>


    <el-dialog title="多鞋型排产页面" v-model="isMultipleShoesDialogVis" width="50%">
        <el-row :gutter="20">
            已选中鞋型：{{ displaySelectedOrderShoe() }}
        </el-row>
        <el-form :model="multipleShoesScheduleForm" :rules="rules" ref="multipleShoesScheduleForm" class="custom-form">
            <el-form-item label="裁断线号选择" prop="cuttingLineNumbers">
                <el-select v-model="multipleShoesScheduleForm.cuttingLineNumbers" placeholder="" multiple>
                    <el-option v-for="item in productionLines['cutting']" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="裁断生产周期" prop="cuttingDateRange">
                <el-date-picker v-model="multipleShoesScheduleForm.cuttingDateRange" type="daterange" size="default"
                    range-separator="至" value-format="YYYY-MM-DD">
                </el-date-picker>
            </el-form-item>
            <el-form-item label="针车预备线号选择" prop="preSewingLineNumbers">
                <el-select v-model="multipleShoesScheduleForm.preSewingLineNumbers" placeholder="" @change="" multiple>
                    <el-option v-for="item in productionLines['preSewing']" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="针车预备生产周期" prop="preSewingDateRange">
                <el-date-picker v-model="multipleShoesScheduleForm.preSewingDateRange" type="daterange" size="default"
                    range-separator="至" value-format="YYYY-MM-DD">
                </el-date-picker>
            </el-form-item>
            <el-form-item label="针车线号选择" prop="sewingLineNumbers">
                <el-select v-model="multipleShoesScheduleForm.sewingLineNumbers" placeholder="" @change="" multiple>
                    <el-option v-for="item in productionLines['sewing']" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="针车生产周期" prop="sewingDateRange">
                <el-date-picker v-model="multipleShoesScheduleForm.sewingDateRange" type="daterange" size="default"
                    range-separator="至" value-format="YYYY-MM-DD">
                </el-date-picker>
            </el-form-item>
            <el-form-item label="成型线号选择" prop="moldingLineNumbers">
                <el-select v-model="multipleShoesScheduleForm.moldingLineNumbers" placeholder="" @change="" multiple>
                    <el-option v-for="item in productionLines['molding']" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="成型生产周期" prop="moldingDateRange">
                <el-date-picker v-model="multipleShoesScheduleForm.moldingDateRange" type="daterange" size="default"
                    range-separator="至" value-format="YYYY-MM-DD">
                </el-date-picker>
            </el-form-item>
        </el-form>
        <template #footer>
            <span>
                <el-button type="primary" @click="isMultipleShoesDialogVis = false">返回</el-button>
                <el-button type="primary" @click="saveMultipleSchedules">保存</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog title="修改排产信息" v-model="isScheduleDialogOpen" width="95%">
        <el-tabs v-model="activeTab" type="card" tab-position="top" @tab-click="">
            <el-tab-pane v-for="tab in tabs" :key="tab.name" :label="tab.label" :name="tab.name">
                <el-row :gutter="20">
                    <el-col :span="10" :offset="0">
                        <span style="white-space: nowrap">
                            {{ tab.lineLabel }}：
                            <el-select v-model="tab.lineValue" placeholder="" @change="" multiple :disabled="!$props.editable">
                                <el-option v-for="item in productionLines[tab.name]" :key="item" :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </span>
                    </el-col>
                    <el-col :span="8" :offset="6">
                        <el-descriptions title="" border v-if="$props.editable">
                            <el-descriptions-item label="外包状态">
                                <div v-if="tab.isOutsourced == 0">
                                    未设置外包
                                </div>
                                <div v-else>
                                    已设置外包
                                </div>
                            </el-descriptions-item>
                            <el-descriptions-item label="操作">
                                <el-button v-if="tab.isOutsourced == 0" type="primary" size="default"
                                    @click="openOutsourceFlow()">启动外包流程</el-button>
                                <el-button-group v-else>
                                    <el-button type="primary" size="default"
                                        @click="openOutsourceFlow()">查看外包流程</el-button>
                                </el-button-group>
                            </el-descriptions-item>
                        </el-descriptions>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="10" :offset="0">
                        <span>
                            {{ tab.dateLabel }}：
                            <el-date-picker v-model="tab.dateValue" type="daterange" size="default" range-separator="-"
                                value-format="YYYY-MM-DD" :readonly="!$props.editable">
                            </el-date-picker>
                        </span>
                    </el-col>
                    <el-col :span="5" :offset="0">
                        <el-button type="primary" size="default" @click="checkDateProductionStatus(tab)">{{
                            tab.isDateStatusTableVis ? '关闭表格' : '查看工期内排产情况' }}</el-button>
                    </el-col>
                    <!-- <el-col :span="5" :offset="0">预计每天生产数量：{{ calculateDailyProduction(currentRow.totalShoes,
                        tab.dateValue)
                        }}</el-col> -->
                </el-row>
                <el-row :gutter="20">
                    <el-table v-if="tab.isDateStatusTableVis" :data="tab.dateStatusTable" border stripe read>
                        <el-table-column type="expand">
                            <template #default="props">
                                <el-table :data="props.row.detail" border stripe>
                                    <el-table-column type="index" />
                                    <el-table-column label="订单号" prop="orderRId" />
                                    <el-table-column label="工厂型号" prop="shoeRId" />
                                    <el-table-column label="鞋型总数量" prop="totalAmount" />
                                    <el-table-column label="工段生产开始" prop="productionStartDate" />
                                    <el-table-column label="工段生产结束" prop="productionEndDate" />
                                    <el-table-column label="平均每天数量" prop="averageAmount" />
                                </el-table>
                            </template>
                        </el-table-column>

                        <el-table-column prop="date" label="日期"> </el-table-column>
                        <el-table-column prop="orderShoeCount" label="已排产鞋型数"> </el-table-column>
                        <el-table-column prop="predictAmount" label="预计当日现有生产量"> </el-table-column>
                    </el-table>
                </el-row>
                <el-row>
                    计划自产数量
                </el-row>
                <el-row :gutter="20">
                    <el-col>
                        <el-table :data="tab.productionAmountTable" border stripe :max-height="500">
                            <el-table-column prop="colorName" label="颜色"></el-table-column>
                            <el-table-column v-for="column in filteredColumns" :key="column.prop" :prop="column.prop"
                                :label="column.label">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row[column.prop]" :readonly="!$props.editable"/>
                                </template>
                            </el-table-column>
                            <el-table-column prop="pairAmount" label="双数"></el-table-column>
                            <el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
            </el-tab-pane>
        </el-tabs>
        <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24" :offset="0">
                鞋型配码信息
                <el-table :data="shoeBatchInfo" :span-method="spanMethod" border stripe :max-height="500">
                    <el-table-column prop="colorName" label="颜色"></el-table-column>
                    <el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
                    <el-table-column prop="batchName" label="配码编号"></el-table-column>
                    <el-table-column v-for="column in filteredColumns" :key="column.prop" :prop="column.prop"
                        :label="column.label"></el-table-column>
                    <el-table-column prop="pairAmount" label="双数"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="isScheduleDialogOpen = false">取消</el-button>
                <el-button type="primary" @click="modifyProductionSchedule">保存</el-button>
                <el-button v-if="currentRow.status === '未排产'" type="success" @click="startProduction">开始生产</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import AllHeader from '@/components/AllHeader.vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus';
import { shoeBatchInfoTableSpanMethod, productionLines, getShoeSizesName } from '../utils';
export default {
    props: ["editable"],
    components: {
        AllHeader
    },
    data() {
        return {
            getShoeSizesName,
            orderRIdSearch: '',
            shoeRIdSearch: '',
            customerProductNameSearch: '',
            statusNodeSearch: '',
            currentPage: 1,
            pageSize: 10,
            orderTotalRows: 0,
            orderTableData: [],
            currentRow: {},
            shoeBatchInfo: [],
            spanMethod: null,
            logisticsMaterialData: [],
            logisticsRows: 0,
            isMaterialLogisticVis: false,
            logisticsCurrentPage: 1,
            logisticsPageSize: 10,
            instruction: false,
            specification: false,
            isMultipleSelection: false,
            selectedRows: [],
            isMultipleShoesDialogVis: false,
            multipleShoesScheduleForm: {},
            multiShoeFormTemplate: {
                cuttingLineNumbers: null,
                cuttingDateRange: null,
                preSewingLineNumbers: null,
                preSewingDateRange: null,
                sewingLineNumbers: null,
                sewingDateRange: null,
                moldingLineNumbers: null,
                moldingDateRange: null,
            },
            productionLines,
            shoeSizes: [],
            isScheduleDialogOpen: false,
            shoeSizeColumns: [],
            activeTab: "cutting",
            // index 0: 裁断，1：预备，2：针车，3：成型
            tabs: [
                {
                    name: 'cutting',
                    label: '裁断排产',
                    lineLabel: '裁断线号',
                    dateLabel: '裁断工期',
                    lineValue: [],
                    dateValue: [],
                    dateStatusTable: [],
                    isOutsourced: 0,
                    isDateStatusTableVis: false,
                    productionAmountTable: [],
                    productionSpanMethod: null,
                    team: 0
                },
                {
                    name: 'preSewing',
                    label: '针车预备排产',
                    lineLabel: '针车预备线号',
                    dateLabel: '针车预备工期',
                    lineValue: [],
                    dateValue: [],
                    dateStatusTable: [],
                    isOutsourced: 0,
                    isDateStatusTableVis: false,
                    productionAmountTable: [],
                    productionSpanMethod: null,
                    team: 1
                },
                {
                    name: 'sewing',
                    label: '针车排产',
                    lineLabel: '针车线号',
                    dateLabel: '针车工期',
                    lineValue: [],
                    dateValue: [],
                    dateStatusTable: [],
                    isOutsourced: 0,
                    isDateStatusTableVis: false,
                    productionAmountTable: [],
                    productionSpanMethod: null,
                    team: 1
                },
                {
                    name: 'molding',
                    label: '成型排产',
                    lineLabel: '成型线号',
                    dateLabel: '成型工期',
                    lineValue: [],
                    dateValue: [],
                    dateStatusTable: [],
                    isOutsourced: 0,
                    isDateStatusTableVis: false,
                    productionAmountTable: [],
                    productionSpanMethod: null,
                    team: 2
                }
            ],
            rules: {
                cuttingLineNumbers: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                cuttingDateRange: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                preSewingLineNumbers: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                preSewingDateRange: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                sewingDateRange: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                sewingDateRange: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                moldingLineNumbers: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
                moldingDateRange: [
                    { required: true, message: '此项为必填项', trigger: 'change' },
                ],
            },
            isSelectedRowsEmpty: false
        }
    },
    async mounted() {
        await this.getOrderDataTable()
    },
    computed: {
        filteredColumns() {
            return this.shoeSizeColumns.filter(column =>
                this.shoeBatchInfo.some(row => row[column.prop] !== undefined && row[column.prop] !== null && row[column.prop] !== 0)
            );
        }
    },
    methods: {
        handleFocus(event) {
            console.log(event)
            if (!this.$props.editable) event.preventDefault(); // Prevent opening dropdown
        },
        async openScheduleDialog(row) {
            this.currentRow = row
            this.isScheduleDialogOpen = true
            this.shoeSizeColumns = await this.getShoeSizesName(row.orderShoeId)
            this.tabs.forEach(row => {
                row.lineValue = []
                row.dateValue = []
                row.isOutsourced = 0
                row.productionAmountTable = []
            })
            await this.getOrderShoeScheduleInfo()
            await this.getOrderShoeBatchInfo()
            await this.getOrderShoeProductionAmount()
        },
        async getOrderShoeScheduleInfo() {
            let params = { "orderShoeId": this.currentRow.orderShoeId }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoescheduleinfo`, { params })
            response.data.forEach((row, index) => {
                this.tabs[index].lineValue = row.lineGroup
                this.tabs[index].dateValue = [row.startDate, row.endDate]
                this.tabs[index].isOutsourced = row.isOutsourced
            })
        },
        async getOrderShoeBatchInfo() {
            this.shoeBatchInfo = []
            const params = { "orderShoeId": this.currentRow.orderShoeId }
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoebatchinfo`, { params })
            this.shoeBatchInfo = response.data
            console.log(this.shoeBatchInfo)
            this.spanMethod = shoeBatchInfoTableSpanMethod(this.shoeBatchInfo);
        },
        async getOrderShoeProductionAmount() {
            const params = { "orderShoeId": this.currentRow.orderShoeId }
            const response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getordershoeproductionamount`, { params })
            this.tabs.forEach(row => {
                if (response.data[row.team] === undefined) {
                    row.productionAmountTable = []
                    let color_totals = {}
                    this.shoeBatchInfo.forEach(batchInfo => {
                        if (!(batchInfo.colorName in color_totals)) {
                            color_totals[batchInfo.colorName] = { ...batchInfo }
                        }
                        else {
                            for (let i = 34; i < 47; i++) {
                                color_totals[batchInfo.colorName][`size${i}Amount`] += batchInfo[`size${i}Amount`]
                            }
                            color_totals[batchInfo.colorName][`pairAmount`] += batchInfo[`pairAmount`]
                        }
                    })
                    for (let color_key in color_totals) {
                        row.productionAmountTable.push(color_totals[color_key])
                    }
                }
                else {
                    row.productionAmountTable = response.data[row.team]
                }
                // row.productionSpanMethod = shoeBatchInfoTableSpanMethod(row.productionAmountTable)
            })
            this.tabs[1].productionAmountTable = this.tabs[2].productionAmountTable
        },
        displaySelectedOrderShoe() {
            let uniqueData = this.selectedRows.filter((item, index, self) =>
                index === self.findIndex((t) => (
                    t.orderShoeId === item.orderShoeId
                ))
            )
            uniqueData = uniqueData.map(item => `(订单号: ${item.orderRId}, 鞋型号: ${item.shoeRId})`).join(', ');
            return uniqueData.toString()
        },
        async saveMultipleSchedules() {
            this.$refs.multipleShoesScheduleForm.validate(async (valid) => {
                if (valid) {
                    try {
                        let data = {
                            "orderShoeIdArr": this.selectedRows.map(row => row.orderShoeId),
                            "scheduleForm": this.multipleShoesScheduleForm
                        }
                        await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/savemultipleschedules`, data)
                        ElMessage.success("保存成功")
                    }
                    catch (error) {
                        ElMessage.error(error)
                    }
                    await this.getOrderDataTable()
                }
                else {
                    console.log("testing2")
                }
            })
        },
        async modifyProductionSchedule() {
            try {
                let data = {
                    "orderShoeId": this.currentRow.orderShoeId,
                }
                let infoList = []
                this.tabs.forEach(row => {
                    let obj = {
                        "lineValue": row.lineValue.join(","),
                        "isOutsourced": row.isOutsourced,
                        "startDate": row.dateValue[0],
                        "endDate": row.dateValue[1]
                    }
                    infoList.push(obj)
                })
                data["productionInfoList"] = infoList
                await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/editproductionschedule`, data)
                let temp_data = [this.tabs[0].productionAmountTable, this.tabs[2].productionAmountTable, this.tabs[3].productionAmountTable]
                data = []
                temp_data.forEach((table, index) => {
                    table.forEach(row => {
                        let obj = {
                            "productionAmountId": row.productionAmountId,
                            "orderShoeTypeId": row.orderShoeTypeId,
                            "productionTeam": index,
                        }
                        for (let i = 34; i < 47; i++) {
                            obj[`size${i}Amount`] = row[`size${i}Amount`]
                        }
                        data.push(obj)
                    })
                })
                await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/saveproductionamount`, data)
                ElMessage.success("修改成功")
            }
            catch (error) {
                ElMessage.error("修改失败")
            }
            this.isScheduleDialogOpen = false
        },
		async startProduction() {
			ElMessageBox.alert('点击确认后，你仍可修改排期，但推进流程操作不可撤回', '警告', {
				confirmButtonText: '确认',
				showCancelButton: true,
				cancelButtonText: '取消'
			}).then(async () => {
				try {
					await this.modifyProductionSchedule()
					const data = { "orderId": this.currentRow.orderId, "orderShoeId": this.currentRow.orderShoeId }
					await axios.patch(`${this.$apiBaseUrl}/production/productionmanager/startproduction`, data)
					ElMessage.success("生产开始")
				}
				catch (error) {
					console.log(error)
					ElMessage.error("排期异常")
				}
                this.getOrderDataTable()
                this.isScheduleDialogOpen = false
			})
		},
        openMultipleShoesDialog() {
            if (this.selectedRows.length == 0) {
                this.isSelectedRowsEmpty = true
                return
            }
            this.multipleShoesScheduleForm = { ...this.multiShoeFormTemplate }
            this.isMultipleShoesDialogVis = true
            this.isSelectedRowsEmpty = false
        },
        toggleSelectionMode() {
            this.isMultipleSelection = !this.isMultipleSelection;
            this.isSelectedRowsEmpty = false
        },
        handleSelectionChange(selection) {
            this.selectedRows = selection
        },
        async handlePageChange(val) {
            this.currentPage = val
            await this.getOrderDataTable()
        },
        async handleSizeChange(val) {
            this.pageSize = val
            await this.getOrderDataTable()
        },
        downloadProductionOrderSheet(row) {
            window.open(
                `${this.$apiBaseUrl}/production/productionmanager/downloadprocutionordersheet?${row.orderShoeId}`
            )
        },
        async getOrderDataTable() {
            let params = {
                "page": this.currentPage,
                "pageSize": this.pageSize,
                "orderRId": this.orderRIdSearch,
                "shoeRId": this.shoeRIdSearch,
                "customerProductName": this.customerProductNameSearch,
                "statusNode": this.statusNodeSearch,
            }
            let response = await axios.get(`${this.$apiBaseUrl}/production/productionmanager/getallorderproductionprogress`, { params })
            this.orderTableData = response.data.result
            this.orderTotalRows = response.data.totalLength
        },
        downloadInstructionForm(row) {

        },
        async openLogisticsDialog(rowData) {
            this.logisticsCurrentPage = 1
            await this.viewLogisticDetail(rowData)
            this.isMaterialLogisticVis = true
        },
        async viewLogisticDetail(row) {
            const params = {
                "page": this.logisticsCurrentPage,
                "pageSize": this.logisticsPageSize,
                "orderRId": row.orderRId,
                "shoeRId": row.shoeRId
            }
            const response = await axios.get(`${this.$apiBaseUrl}/warehouse/warehousemanager/getallmaterialinfo`, { params })
            this.logisticsMaterialData = response.data.result
            this.logisticsRows = response.data.total
        },
        async handleLogisticsPageChange(val) {
            this.logisticsCurrentPage = val
            await this.viewLogisticDetail()
        },
        async handleLogisticsPageChange(val) {
            this.logisticsPageSize = val
            await this.viewLogisticDetail()
        },
    }
}
</script>
<style scoped>
.error-text {
    color: red;
    font-size: 12px;
}

.custom-form {
    width: 400px;
}

.is-readonly .el-input__inner {
  cursor: not-allowed;
  background-color: #f5f5f5;
}
.is-readonly .el-input__suffix {
  display: none;
}
</style>
