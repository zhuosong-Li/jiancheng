<template>
    <el-container :direction="vertical">
        <el-header height="">
            <AllHeader></AllHeader>
        </el-header>
        <el-main height="">
            <el-row :gutter="20" style="text-align: center">
                <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
                    >一次采购订单生成</el-col
                >
            </el-row>
            <el-row :gutter="20">
                <el-col :span="24" :offset="0">
                    <span style="font-weight: bold; font-size: larger">订单信息：</span>
                    <Arrow :status="orderData.status" :key="updateArrowKey"></Arrow>
                    <el-descriptions title="" :column="2" border>
                        <el-descriptions-item label="订单编号" align="center">{{
                            orderData.orderId
                        }}</el-descriptions-item>
                        <el-descriptions-item label="订单创建时间" align="center">{{
                            orderData.createTime
                        }}</el-descriptions-item>
                        <el-descriptions-item label="客户名称" align="center">{{
                            orderData.customerName
                        }}</el-descriptions-item>
                        <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                        <el-descriptions-item label="订单预计截止日期" align="center">{{
                            orderData.deadlineTime
                        }}</el-descriptions-item>
                    </el-descriptions></el-col
                >
            </el-row>
            <el-row :gutter="20" style="margin-top: 10px">
                <el-col :span="4" :offset="0">
                    <div style="display: flex; align-items: center; white-space: nowrap">
                        工厂型号搜索：<el-input
                            v-model="inheritIdSearch"
                            placeholder=""
                            size="default"
                            :suffix-icon="Search"
                            clearable
                            @input="tableWholeFilter"
                        ></el-input>
                    </div>
                </el-col>
            </el-row>

            <el-row :gutter="20" style="margin-top: 20px">
                <el-col :span="24" :offset="0">
                    <el-table :data="testTableFilterData" border style="height: 400px">
                        <el-table-column
                            prop="inheritId"
                            label="工厂型号"
                            align="center"
                            width="100"
                        ></el-table-column>
                        <el-table-column
                            prop="customerId"
                            label="客户型号"
                            align="center"
                        ></el-table-column>
                        <el-table-column label="鞋图" align="center">
                            <template #default="scope">
                                <el-image
                                    style="width: 150px; height: 100px"
                                    :src="scope.row.image"
                                    :fit="contain"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column
                            prop="designer"
                            label="设计员"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="editter"
                            label="调版员"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="bomId"
                            label="BOM编号"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="status"
                            label="状态"
                            align="center"
                        ></el-table-column>
                        <el-table-column label="操作" align="center">
                            <template #default="scope">
                                <el-button
                                    v-if="scope.row.status === '一次采购订单未填写'"
                                    type="primary"
                                    @click="handleGenerate(scope.row)"
                                    >填写</el-button
                                >
                                <el-button
                                    v-else-if="scope.row.status === '一次采购订单已提交'"
                                    type="primary"
                                    @click="openPreviewDialog(scope.row)"
                                    >查看</el-button
                                >
                                <div v-else-if="scope.row.status === '一次采购订单已保存'">
                                    <el-button type="primary" @click="openEditDialog(scope.row)"
                                        >编辑</el-button
                                    >
                                    <el-button type="success" @click="openPreviewDialog(scope.row)"
                                        >预览</el-button
                                    >
                                    <el-button type="warning" @click="submitBOMUsage(scope.row)"
                                        >提交</el-button
                                    >
                                </div>
                            </template></el-table-column
                        >
                    </el-table></el-col
                >
            </el-row>
            <el-dialog
                :title="`一次BOM填写 ${newPurchaseOrderId}`"
                v-model="createVis"
                width="100%"
                @close="handleGenerateClose"
            >
                <el-descriptions title="订单信息" :column="2">
                    <el-descriptions-item label="订单编号" align="center">{{
                        orderData.orderId
                    }}</el-descriptions-item>
                    <el-descriptions-item label="订单创建时间" align="center">{{
                        orderData.createTime
                    }}</el-descriptions-item>
                    <el-descriptions-item label="客户名称" align="center">{{
                        orderData.customerName
                    }}</el-descriptions-item>
                    <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                                <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item> -->
                    <el-descriptions-item label="订单预计截止日期" align="center">{{
                        orderData.deadlineTime
                    }}</el-descriptions-item>
                    <el-descriptions-item label="工艺单"
                        ><el-button
                            type="primary"
                            size="default"
                            @click="downloadProductionOrderList"
                            >查看投产指令单</el-button
                        >
                    </el-descriptions-item>
                    <el-descriptions-item label="生产订单"
                        ><el-button type="primary" size="default" @click="downloadProductionOrder"
                            >查看生产订单</el-button
                        >
                    </el-descriptions-item>
                </el-descriptions>

                <div style="height: 600px; overflow-y: scroll; overflow-x: hidden">
                    <el-row>
                        <el-table
                            :data="orderProduceInfo"
                            border
                            style="width: 100%"
                            :span-method="arraySpanMethod"
                            height="300"
                        >
                            <el-table-column prop="color" label="颜色" />
                            <el-table-column prop="size" label="配码" />
                            <el-table-column prop="35" label="35" />
                            <el-table-column prop="36" label="36" />
                            <el-table-column prop="37" label="37" />
                            <el-table-column prop="38" label="38" />
                            <el-table-column prop="39" label="39" />
                            <el-table-column prop="40" label="40" />
                            <el-table-column prop="41" label="41" />
                            <el-table-column prop="42" label="42" />
                            <el-table-column prop="43" label="43" />
                            <el-table-column prop="44" label="44" />
                            <el-table-column prop="45" label="45" />
                            <el-table-column prop="pairAmount" label="双数" />
                            <el-table-column prop="total" label="合计" />
                        </el-table>
                    </el-row>
                    <el-row style="margin-top: 10px">
                        <el-table :data="bomTestData" border>
                            <el-table-column prop="materialType" label="材料类型">
                            </el-table-column>
                            <el-table-column prop="materialName" label="材料名称">
                            </el-table-column>
                            <el-table-column prop="materialSpecification" label="材料规格">
                            </el-table-column>
                            <el-table-column prop="color" label="颜色">
                                <template #default="scope">
                                    <el-select v-model="scope.row.color" size="default" disabled>
                                        <el-option
                                            v-for="item in colorOptions"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                        ></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column prop="unit" label="单位"> </el-table-column>
                            <el-table-column prop="supplierName" label="厂家名称"></el-table-column>
                            <el-table-column prop="unitUsage" label="单位用量">
                            </el-table-column>
                            <el-table-column prop="approvalUsage" label="核定用量">
                            </el-table-column>
                            <el-table-column prop="amount" label="采购数量">
                                <template #default="scope">
                                    <el-input-number
                                        v-if="scope.row.materialCategory == 0"
                                        v-model="scope.row.amount"
                                        :min="0"
                                        size="small"
                                    />
                                    <el-button
                                        v-if="scope.row.materialCategory == 1"
                                        type="primary"
                                        size="default"
                                        @click="openSizeDialog(scope.row, scope.$index)"
                                        >尺码用量填写</el-button
                                    >
                                </template>
                            </el-table-column>
                            <el-table-column prop="useDepart" label="使用工段">
                                <template #default="scope">
                                    <el-select
                                        v-model="scope.row.useDepart"
                                        size="default"
                                        disabled
                                    >
                                        <el-option
                                            v-for="item in departmentOptions"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                        ></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column label="备注">
                                <template #default="scope">
                                    <el-input v-model="scope.row.comment" size="default" />
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-row>
                </div>

                <template #footer>
                    <span>
                        <el-button @click="handleGenerateClose">取消</el-button>
                        <el-button type="primary" @click="confirmBOMSave">保存</el-button>
                    </span>
                </template>
            </el-dialog>

            <el-dialog
                title="预览采购订单 K2402121116202024061101F"
                v-model="isPreviewDialogVisible"
                width="90%"
            >
                <el-descriptions title="订单信息" :column="2">
                    <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
                </el-descriptions>
                <div style="height: 500px; overflow-y: scroll; overflow-x: hidden">
                    <el-row
                        v-for="factory in purchaseTestData"
                        :key="factory.factoryName"
                        :gutter="20"
                        style="margin-bottom: 20px"
                    >
                        <el-col :span="23">
                            <h3>{{ factory.factoryName }}</h3>
                            <div v-if="factoryFieldJudge(factory.factoryField)">
                                <el-table :data="factory.data" border style="width: 100%">
                                    <el-table-column type="index" label="编号" />
                                    <el-table-column
                                        prop="materialType"
                                        label="材料类型"
                                    ></el-table-column>
                                    <el-table-column prop="materialName" label="材料名称" />
                                    <el-table-column
                                        prop="materialSpecification"
                                        label="材料规格"
                                    ></el-table-column>
                                    <el-table-column prop="unit" label="单位" />

                                    <el-table-column prop="amount" label="采购数量" />
                                    <el-table-column label="分码数量（中国/美标内码/美标外显）">
                                        <el-table-column label="35" width="50">
                                            <el-table-column label="7" width="50">
                                                <el-table-column
                                                    prop="size35"
                                                    label="7"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="36" width="50">
                                            <el-table-column label="7" width="50">
                                                <el-table-column
                                                    prop="size36"
                                                    label="7.5"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="37" width="50">
                                            <el-table-column label="8" width="50">
                                                <el-table-column
                                                    prop="size37"
                                                    label="8"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="38" width="50">
                                            <el-table-column label="8" width="50">
                                                <el-table-column
                                                    prop="size38"
                                                    label="8.5"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="39" width="50">
                                            <el-table-column label="9" width="50">
                                                <el-table-column
                                                    prop="size39"
                                                    label="9"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="40" width="50">
                                            <el-table-column label="9" width="50">
                                                <el-table-column
                                                    prop="size40"
                                                    label="9.5"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="41" width="50">
                                            <el-table-column label="10" width="50">
                                                <el-table-column
                                                    prop="size41"
                                                    label="10"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="42" width="50">
                                            <el-table-column label="10" width="50">
                                                <el-table-column
                                                    prop="size42"
                                                    label="10.5"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="43" width="50">
                                            <el-table-column label="11" width="50">
                                                <el-table-column
                                                    prop="size43"
                                                    label="11"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="44" width="50">
                                            <el-table-column label="12" width="50">
                                                <el-table-column
                                                    prop="size44"
                                                    label="12"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column label="45" width="50">
                                            <el-table-column label="13" width="50">
                                                <el-table-column
                                                    prop="size45"
                                                    label="13"
                                                    width="50"
                                                ></el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                    </el-table-column>
                                    <el-table-column prop="comment" label="备注" />
                                </el-table>
                            </div>
                            <div v-else>
                                <el-table :data="factory.data" border style="width: 100%">
                                    <el-table-column type="index" label="编号" />
                                    <el-table-column
                                        prop="materialType"
                                        label="材料类型"
                                    ></el-table-column>
                                    <el-table-column prop="materialName" label="材料名称" />
                                    <el-table-column
                                        prop="materialSpecification"
                                        label="材料规格"
                                    ></el-table-column>
                                    <el-table-column prop="unit" label="单位" />
                                    <el-table-column prop="unitUsage" label="单位用量" />
                                    <el-table-column prop="approvedUsage" label="核定用量" />
                                    <el-table-column prop="amount" label="采购数量" />
                                    <el-table-column prop="comment" label="备注" />
                                </el-table>
                            </div>
                        </el-col>
                    </el-row>
                </div>
                <template #footer>
                    <span>
                        <el-button type="primary" @click="closePreviewDialog">确认</el-button>
                    </span>
                </template>
            </el-dialog>
            <el-dialog title="采购订单创建页面" v-model="isPurchaseOrderVis" width="80%">
                <el-tabs v-model="activeTab" type="card" tab-position="top" @tab-click="">
                    <el-tab-pane
                        v-for="item in tabPlaneData"
                        :key="item.purchaseOrderId"
                        :label="item.purchaseOrderId + '    ' + item.factoryName"
                        :name="item.purchaseOrderId"
                        style="min-height: 500px"
                    >
                        <el-row :gutter="20">
                            <el-col :span="12" :offset="0"
                                ><span
                                    >订单备注：
                                    <el-input
                                        v-model="item.unifiedRemark"
                                        placeholder=""
                                        type="textarea"
                                        resize="none"
                                        size="normal"
                                        clearable
                                        @change=""
                                    ></el-input> </span
                            ></el-col>
                            <el-col :span="12" :offset="0">
                                <span
                                    >环境要求：
                                    <el-input
                                        v-model="item.environmentalRequirements"
                                        placeholder=""
                                        type="textarea"
                                        resize="none"
                                        size="normal"
                                        clearable
                                        @change=""
                                    ></el-input>
                                </span>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="12" :offset="0">
                                <span
                                    >发货地址：
                                    <el-input
                                        v-model="item.shippingAddress"
                                        placeholder=""
                                        type="textarea"
                                        resize="none"
                                        size="normal"
                                        clearable
                                        @change=""
                                    ></el-input>
                                </span>
                            </el-col>
                            <el-col :span="12" :offset="0">
                                <span
                                    >交货周期：
                                    <el-input
                                        v-model="item.leadTime"
                                        placeholder=""
                                        type="textarea"
                                        resize="none"
                                        size="normal"
                                        clearable
                                        @change=""
                                    ></el-input>
                                </span>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20" style="margin-top: 20px">
                            <el-col :span="24" :offset="0">
                                <div v-if="factoryFieldJudge(item.factoryField)">
                                    <el-table
                                        :data="item.materialTableData"
                                        border
                                        style="width: 100%"
                                        height="500"
                                    >
                                        <el-table-column type="index" label="编号" />
                                        <el-table-column
                                            prop="materialType"
                                            label="材料类型"
                                        ></el-table-column>
                                        <el-table-column prop="materialName" label="材料名称" />
                                        <el-table-column
                                            prop="materialSpecification"
                                            label="材料规格"
                                        ></el-table-column>
                                        <el-table-column prop="unit" label="单位" />

                                        <el-table-column prop="amount" label="采购数量" />
                                        <el-table-column label="分码数量（中国/美标内码/美标外显）">
                                            <el-table-column label="35" width="50">
                                                <el-table-column label="7" width="50">
                                                    <el-table-column
                                                        prop="size35"
                                                        label="7"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="36" width="50">
                                                <el-table-column label="7" width="50">
                                                    <el-table-column
                                                        prop="size36"
                                                        label="7.5"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="37" width="50">
                                                <el-table-column label="8" width="50">
                                                    <el-table-column
                                                        prop="size37"
                                                        label="8"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="38" width="50">
                                                <el-table-column label="8" width="50">
                                                    <el-table-column
                                                        prop="size38"
                                                        label="8.5"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="39" width="50">
                                                <el-table-column label="9" width="50">
                                                    <el-table-column
                                                        prop="size39"
                                                        label="9"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="40" width="50">
                                                <el-table-column label="9" width="50">
                                                    <el-table-column
                                                        prop="size40"
                                                        label="9.5"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="41" width="50">
                                                <el-table-column label="10" width="50">
                                                    <el-table-column
                                                        prop="size41"
                                                        label="10"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="42" width="50">
                                                <el-table-column label="10" width="50">
                                                    <el-table-column
                                                        prop="size42"
                                                        label="10.5"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="43" width="50">
                                                <el-table-column label="11" width="50">
                                                    <el-table-column
                                                        prop="size43"
                                                        label="11"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="44" width="50">
                                                <el-table-column label="12" width="50">
                                                    <el-table-column
                                                        prop="size44"
                                                        label="12"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                            <el-table-column label="45" width="50">
                                                <el-table-column label="13" width="50">
                                                    <el-table-column
                                                        prop="size45"
                                                        label="13"
                                                        width="50"
                                                    ></el-table-column>
                                                </el-table-column>
                                            </el-table-column>
                                        </el-table-column>
                                        <el-table-column prop="comment" label="备注" />
                                    </el-table>
                                </div>
                                <div v-else>
                                    <el-table
                                        :data="item.materialTableData"
                                        border
                                        stripe
                                        height="500"
                                    >
                                        <el-table-column type="index"></el-table-column>
                                        <el-table-column
                                            prop="materialType"
                                            label="材料类型"
                                        ></el-table-column>
                                        <el-table-column prop="materialName" label="材料名称" />
                                        <el-table-column
                                            prop="materialSpecification"
                                            label="材料规格"
                                        ></el-table-column>
                                        <el-table-column prop="unit" label="单位" />
                                        <el-table-column prop="amount" label="数量" />
                                        <el-table-column prop="comment" label="备注" />
                                    </el-table>
                                </div>
                            </el-col>
                        </el-row>
                    </el-tab-pane>
                </el-tabs>

                <template #footer>
                    <span>
                        <el-button @click="">取消</el-button>
                        <el-button type="primary" @click="">保存</el-button>
                        <el-button type="success" @click="">提交</el-button>
                    </span>
                </template>
            </el-dialog>

            <!-- Main content -->
        </el-main>
    </el-container>
    <el-dialog title="尺码数量填写" v-model="isSizeDialogVisible" width="60%">
        <el-table :data="sizeData" border stripe>
            <el-table-column prop="size" label="尺码"></el-table-column>
            <el-table-column prop="USinnersize" label="内码美标尺码"></el-table-column>
            <el-table-column prop="USoutersize" label="外显美标尺码"></el-table-column>
            <el-table-column prop="usageAmount" label="BOM用量"></el-table-column>
            <el-table-column label="采购数量">
                <template #default="scope">
                    <el-input-number v-model="scope.row.purchaseAmount" :min="0" size="small" />
                </template>
            </el-table-column>
        </el-table>

        <template #footer>
            <span>
                <el-button @click="">Cancel</el-button>
                <el-button type="primary" @click="">OK</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import AllHeader from '@/components/AllHeader.vue'
import Arrow from '@/components/OrderArrowView.vue'
import axios from 'axios'
export default {
    props: ['orderId'],
    components: {
        AllHeader,
        Arrow
    },
    data() {
        return {
            newPurchaseOrderId: '',
            activeTab: '',
            isPurchaseOrderVis: false,
            createVis: false,
            isSizeDialogVisible: false,
            sizeData: [],
            tabPlaneData: [],
            orderData: {},
            testTableData: [],
            testTableFilterData: [],
            orderProduceInfo: [],
            bomTestData: [],
            originalBomTestData: [],
            factoryOptions: [
                { materialName: '黑色超软镜面PU', factoryName: '一一鞋材' },
                { materialName: '黑色超软镜面PU', factoryName: '深源皮革' },
                { materialName: '黑色超软镜面PU', factoryName: '嘉泰皮革' }
                // Add more options here
            ],
            departmentOptions: [],
            colorOptions: [],
            purchaseTestData: [],
            isPreviewDialogVisible: false,
            selectedFile: null
        }
    },
    mounted() {
        this.getAllColorOptions()
        this.getAllDepartmentOptions()
        this.$setAxiosToken()
        this.getOrderInfo()
        this.getAllShoeBomInfo()
    },
    methods: {
        async getAllDepartmentOptions() {
            const response = await this.$axios.get('http://localhost:8000/general/getalldepartments')
            this.departmentOptions = response.data
        },
        async getAllColorOptions() {
            const response = await this.$axios.get('http://localhost:8000/general/allcolors')
            this.colorOptions = response.data
        },
        async getNewPurchaseOrderId() {
            const response = await axios.get('http://localhost:8000/firstpurchase/getnewpurchaseorderid')
            this.newPurchaseOrderId = response.data.purchaseOrderId
        },
        async getOrderInfo() {
            const response = await axios.get(
                `http://localhost:8000/order/getorderInfo?orderid=${this.orderId}`
            )
            this.orderData = response.data
            console.log(this.orderData)
            this.updateArrowKey += 1
        },
        async getAllShoeBomInfo() {
            const response = await this.$axios.get(
                `http://localhost:8000/firstpurchase/getallboms?orderid=${this.orderId}`
            )
            this.testTableData = response.data
            this.tableWholeFilter()
        },
        async getOrderShoeBatchInfo(orderId, orderShoeId) {
            const response = await this.$axios.get(`http://localhost:8000/order/getordershoesizesinfo`, {
                params: {
                    orderid: orderId,
                    ordershoeid: orderShoeId
                }
            })
            this.orderProduceInfo = response.data
        },
        async getBOMDetails(row) {
            const response = await this.$axios.get(
                `http://localhost:8000/usagecalculation/getshoebomitems`,
                {
                    params: {
                        bomrid: row.bomId
                    }
                }
            )
            this.bomPreviewData = response.data
            this.bomTestData = response.data
        },
        tableWholeFilter() {
            if (!this.inheritIdSearch) {
                this.testTableFilterData = this.testTableData
                return
            }

            this.testTableFilterData = this.testTableData.filter((task) => {
                const inheritMatch = task.inheritId.includes(this.inheritIdSearch)
                return inheritMatch
            })
        },
        factoryFieldJudge(field) {
            if (field.includes('中底') || field.includes('大底') || field.includes('鞋楦')) {
                return true
            }
            return false
        },
        openSizeDialog(row) {
            this.sizeData = row.sizeInfo
            this.isSizeDialogVisible = true
        },
        sizeDisabled(row, column) {
            if (column === 1) {
                return (
                    row.materialType !== '大底' &&
                    row.materialType !== '中底' &&
                    row.materialType !== '楦头'
                )
            }
            return (
                row.materialType === '大底' ||
                row.materialType === '中底' ||
                row.materialType === '楦头'
            )
        },
        async handleGenerate(row) {
            await this.getNewPurchaseOrderId()
            this.createVis = true
            this.getOrderShoeBatchInfo(this.orderData.orderId, row.inheritId)
            this.getBOMDetails(row)
            this.currentPurchaseShoeId = row.inheritId
        },
        handleGenerateClose() {
            this.createVis = false
        },
        getFilteredFactoryOptions(materialName) {
            const filteredOptions = this.factoryOptions.filter(
                (option) => option.materialName === materialName
            )
            return [{ factoryName: '询价' }, ...filteredOptions]
        },
        openPreviewDialog() {
            // Replace this with the actual logic to get the file
            this.isPreviewDialogVisible = true
        },
        closePreviewDialog() {
            this.isPreviewDialogVisible = false
        }
    }
}
</script>

<style scoped>
/* Add your styles here */
</style>
