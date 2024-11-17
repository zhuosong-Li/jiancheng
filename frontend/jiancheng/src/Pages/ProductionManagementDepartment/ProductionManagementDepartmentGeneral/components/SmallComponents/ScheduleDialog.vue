<template>
    <el-dialog title="修改排产信息" v-model="isScheduleModify" width="95%">
        <el-tabs v-model="activeTab" type="card" tab-position="top" @tab-click="">
            <el-tab-pane v-for="tab in tabs" :key="tab.name" :label="tab.label" :name="tab.name">
                <el-row :gutter="20">
                    <el-col :span="10" :offset="0">
                        <span style="white-space: nowrap">
                            {{ tab.lineLabel }}：
                            <el-select v-model="tab.lineValue" placeholder="" @change="" multiple>
                                <el-option v-for="item in productionLines[tab.name]" :key="item" :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </span>
                    </el-col>
                    <el-col :span="8" :offset="6">
                        <el-descriptions title="" border>
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
                                :disabled-date="disableDate" value-format="YYYY-MM-DD">
                            </el-date-picker>
                        </span>
                    </el-col>
                    <el-col :span="5" :offset="0">
                        <el-button type="primary" size="default" @click="checkDateProductionStatus(tab)">{{
                            tab.isDateStatusTableVis ? '关闭表格' : '查看工期内排产情况' }}</el-button>
                    </el-col>
                    <el-col :span="5" :offset="0">预计每天生产数量：{{ calculateDailyProduction(currentRow.totalShoes,
                        tab.dateValue)
                        }}</el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-table v-if="tab.isDateStatusTableVis" :data="tab.dateStatusTable" border stripe>
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
                            <el-table-column prop="size34" label="34">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size34" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size35" label="35">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size35" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size36" label="36">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size36" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size37" label="37">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size37" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size38" label="38">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size38" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size39" label="39">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size39" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size40" label="40">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size40" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size41" label="41">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size41" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size42" label="42">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size42" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size43" label="43">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size43" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size44" label="44">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size44" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size45" label="45">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size45" />
                                </template>
                            </el-table-column>
                            <el-table-column prop="size46" label="46">
                                <template v-slot="scope">
                                    <el-input v-model="scope.row.size46" />
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
                    <el-table-column prop="batchName" label="配码编号"></el-table-column>
                    <el-table-column prop="size34" label="34"></el-table-column>
                    <el-table-column prop="size35" label="35"></el-table-column>
                    <el-table-column prop="size36" label="36"></el-table-column>
                    <el-table-column prop="size37" label="37"></el-table-column>
                    <el-table-column prop="size38" label="38"></el-table-column>
                    <el-table-column prop="size39" label="39"></el-table-column>
                    <el-table-column prop="size40" label="40"></el-table-column>
                    <el-table-column prop="size41" label="41"></el-table-column>
                    <el-table-column prop="size42" label="42"></el-table-column>
                    <el-table-column prop="size43" label="43"></el-table-column>
                    <el-table-column prop="size44" label="44"></el-table-column>
                    <el-table-column prop="size45" label="45"></el-table-column>
                    <el-table-column prop="size46" label="46"></el-table-column>
                    <el-table-column prop="pairAmount" label="双数"></el-table-column>
                    <el-table-column prop="totalAmount" label="颜色总数"></el-table-column>
                </el-table>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button @click="isScheduleModify = false">取消</el-button>
                <el-button type="primary" @click="modifyProductionSchedule">保存</el-button>
                <el-button v-if="currentRow.status === '未排产'" type="success" @click="startProduction">开始生产</el-button>
            </span>
        </template>
    </el-dialog>
</template>