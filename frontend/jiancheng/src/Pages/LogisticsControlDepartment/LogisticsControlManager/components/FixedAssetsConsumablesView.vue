<template>
    <el-row :gutter="20">
        <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center"
            >固定资产/耗材采购订单生成</el-col
        >
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="12" :offset="0"
            ><el-button-group>
                <el-button type="primary" size="default" @click="openCreateDialog"
                    >新建耗材/固定资产采购订单</el-button
                >
                <el-button type="primary" size="default" @click="openCreateSizeDialog"
                    >创建尺码型号采购订单</el-button
                >
            </el-button-group>
        </el-col>
        <el-col :span="4" :offset="8"
            ><el-button type="warning" size="large" @click="openUnsubmitDialog"
                >待提交订单</el-button
            >
        </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="6" :offset="0">
            <div style="display: flex; align-items: center; white-space: nowrap">
                订单编号查询：<el-input
                    v-model="orderSearch"
                    placeholder=""
                    size="default"
                    :suffix-icon="Search"
                    clearable
                    @input="tableWholeFilter"
                ></el-input>
            </div>
        </el-col>
        <el-col :span="6" :offset="0">
            <div style="display: flex; align-items: center; white-space: nowrap">
                耗材类型查询：<el-input
                    v-model="assetsTypeSearch"
                    placeholder=""
                    size="default"
                    :suffix-icon="Search"
                    clearable
                    @input="tableWholeFilter"
                ></el-input>
            </div>
        </el-col>
        <el-col :span="6" :offset="0">
            <div style="display: flex; align-items: center; white-space: nowrap">
                采购类型查询：
                <el-select
                    v-model="isPurchaseOrderFilter"
                    value-key=""
                    placeholder=""
                    clearable
                    filterable
                    @change="tableWholeFilter"
                >
                    <el-option
                        v-for="item in isPurchaseOrderOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
        </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24" :offset="0">
            <el-table
                v-loading="datafinished"
                :data="materialPurchaseFilterData"
                border
                style="height: 450px"
                ref="singleSelectTable"
                @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column
                    prop="materialPurchaseOrderId"
                    label="采购订单编号"
                ></el-table-column>
                <el-table-column prop="createDate" label="采购下发日期"></el-table-column>
                <el-table-column prop="orderType" label="随订单采购/独立采购"></el-table-column>
                <el-table-column prop="orderId" label="订单编号"></el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" @click="openPreviewDialog(scope.row)"
                            >查看</el-button
                        >
                    </template></el-table-column
                >
            </el-table>
        </el-col>
    </el-row>
    <el-row :gutter="20">
        <el-col :span="6" :offset="16">
            <el-pagination
                background
                :total="materialPurchaseFilterData.length"
                :page-size="10"
                @current-change="handleCurrentChange"
            ></el-pagination>
        </el-col>
    </el-row>
    <!--未提交订单对话框-->
    <el-dialog
        title="未提交订单一览"
        v-model="unsubmitVis"
        width="90%"
        :close-on-click-modal="false"
    >
        <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24" :offset="0">
                <el-table :data="unsubmitPurchaseOrder" border style="height: 600px">
                    <el-table-column
                        prop="materialPurchaseOrderId"
                        label="采购订单编号"
                    ></el-table-column>
                    <el-table-column prop="orderType" label="随订单采购/独立采购"></el-table-column>
                    <el-table-column prop="orderId" label="订单编号"></el-table-column>
                    <el-table-column label="操作">
                        <template #default="scope">
                            <el-button type="primary" @click="openPreviewDialog(scope.row)"
                                >查看</el-button
                            >
                            <el-button type="primary" @click="openEditDialog(scope.row)"
                                >编辑</el-button
                            >
                            <el-button type="success" @click="openSubmitDialog(scope.row)"
                                >下发</el-button
                            >
                            <el-button
                                type="danger"
                                @click="deleteUnsubmitPurchaseOrder(scope.row)"
                                >删除</el-button
                            >
                        </template></el-table-column
                    >
                </el-table>
            </el-col>
        </el-row>
        <template #footer>
            <span>
                <el-button type="primary" @click="unsubmitVis = false">确认</el-button>
            </span>
        </template>
    </el-dialog>

    <!--创建新采购订单/过往订单创建-->
    <el-dialog
        :title="`耗材/固定资产采购订单 ${newPurchaseOrderId}`"
        v-model="createVis"
        width="95%"
        @close="handleGenerateClose"
        :close-on-click-modal="false"
    >
        <el-table :data="newAssetPurchaseData" border height="450">
            <el-table-column prop="materialType" label="材料类型" />
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column label="材料规格">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.materialSpecification"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="颜色">
                <template #default="scope">
                    <el-select v-model="scope.row.color" placeholder="" filterable>
                        <el-option
                            v-for="item in colorOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="warehouseName" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column label="采购数量">
                <template #default="scope">
                    <el-input-number
                        v-model="scope.row.purchaseAmount"
                        :min="0"
                        size="small"
                        step="0.001"
                    />
                </template>
            </el-table-column>
            <el-table-column prop="supplierName" label="工厂名称"> </el-table-column>
            <el-table-column label="随订单采购/独立采购">
                <template #default="scope">
                    <el-select v-model="scope.row.isPurchaseOrder" placeholder="" filterable>
                        <el-option
                            v-for="item in isPurchaseOrderOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="订单编号">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.orderId"
                        placeholder=""
                        size="default"
                        clearable
                        :disabled="scope.row.isPurchaseOrder === 'G'"
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="备注">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.comment"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button
                        type="danger"
                        @click="deleteCurrentRow(scope.$index, newAssetPurchaseData)"
                        >删除</el-button
                    >
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" size="default" @click="openNewMaterialDialog(0)"
            >添加新材料</el-button
        >

        <template #footer>
            <span>
                <el-button @click="createVis = false">取消</el-button>
                <el-button type="primary" @click="newPurchaseOrderSave">保存</el-button>
            </span>
        </template>
    </el-dialog>
    <!--采购材料对话框-->
    <el-dialog
        title="添加新采购材料"
        v-model="newMaterialVis"
        width="60%"
        :close-on-click-modal="false"
    >
        <el-row :gutter="20">
            <el-col :span="6" :offset="0">
                <div style="display: flex; align-items: center; white-space: nowrap">
                    材料类型查询：<el-input
                        v-model="materialTypeSearch"
                        placeholder=""
                        size="default"
                        :suffix-icon="Search"
                        clearable
                        @change="getMaterialFilterData(currentCreateViewId)"
                    ></el-input>
                </div>
            </el-col>
            <el-col :span="6" :offset="0">
                <div style="display: flex; align-items: center; white-space: nowrap">
                    材料名称查询：<el-input
                        v-model="materialSearch"
                        placeholder=""
                        size="default"
                        :suffix-icon="Search"
                        clearable
                        @change="getMaterialFilterData(currentCreateViewId)"
                    ></el-input>
                </div>
            </el-col>
            <el-col :span="6" :offset="0">
                <div style="display: flex; align-items: center; white-space: nowrap">
                    工厂名查询：<el-input
                        v-model="factorySearch"
                        placeholder=""
                        size="default"
                        :suffix-icon="Search"
                        clearable
                        @change="getMaterialFilterData(currentCreateViewId)"
                    ></el-input>
                </div>
            </el-col>
        </el-row>
        <el-table
            :data="assetFilterTable"
            border
            ref="materialSelectTable"
            @selection-change="handleMaterialSelectionChange"
            style="height: 400px"
            v-loading="materialAddfinished"
        >
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="materialType" label="材料类型" />
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column prop="warehouseName" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column prop="supplierName" label="工厂名称" />
        </el-table>

        <template #footer>
            <span>
                <el-button @click="handleGenerateClose">取消</el-button>
                <el-button
                    v-if="currentCreateViewId == 0"
                    type="primary"
                    @click="confirmNewMaterialAdd"
                    >保存</el-button
                >
                <el-button v-else-if="currentCreateViewId == 1" type="primary" @click="confirmNewSizeMaterialAdd">保存</el-button>
                <el-button v-else-if="currentCreateViewId == 2" type="primary" @click="confirmEditNewMaterialAdd">保存</el-button>
                <el-button v-else-if="currentCreateViewId == 3" type="primary" @click="confirmEditSizeNewMaterialAdd">保存</el-button>
            </span>
        </template>
    </el-dialog>
    <!--采购订单预览-->
    <el-dialog
        :title="`耗材/固定资产采购订单 ${currentViewPurchaseOrderId} 预览`"
        v-model="purchaseOrderVis"
        width="90%"
        :close-on-click-modal="false"
        :key="currentViewPurchaseOrderId"
    >
        <div style="height: 500px; overflow-y: scroll; overflow-x: hidden">
            <el-row
                v-for="purchaseDivideOrder in purchaseTestData"
                :key="purchaseDivideOrder"
                :gutter="20"
                style="margin-bottom: 20px"
            >
                <el-col :span="23">
                    <h3>分采购订单编号 {{ purchaseDivideOrder.purchaseDivideOrderId }}</h3>
                    <h3>工厂名称: {{ purchaseDivideOrder.supplierName }}</h3>
                    <el-row :gutter="20">
                        <el-col :span="12" :offset="0"
                            ><span
                                >订单备注：
                                {{ purchaseDivideOrder.remark }}
                            </span></el-col
                        >
                        <el-col :span="12" :offset="0">
                            <span
                                >环境要求：
                                {{ purchaseDivideOrder.evironmentalRequest }}
                            </span>
                        </el-col>
                    </el-row>
                    <el-row :gutter="20">
                        <el-col :span="12" :offset="0"
                            ><span
                                >发货地址: {{ purchaseDivideOrder.shipmentAddress }}
                            </span></el-col
                        >
                        <el-col :span="12" :offset="0">
                            <span>交货周期: {{ purchaseDivideOrder.shipmentDeadline }} </span>
                        </el-col>
                    </el-row>
                    <div v-if="factoryFieldJudge(purchaseDivideOrder.purchaseDivideOrderType)">
                        <el-table
                            :data="purchaseDivideOrder.assetsItems"
                            border
                            style="width: 100%"
                        >
                            <el-table-column type="index" label="编号" />
                            <el-table-column prop="materialType" label="材料类型"></el-table-column>
                            <el-table-column prop="materialName" label="材料名称" />
                            <el-table-column
                                prop="materialSpecification"
                                label="材料规格"
                            ></el-table-column>
                            <el-table-column prop="unit" label="单位" />

                            <el-table-column prop="purchaseAmount" label="采购数量" />
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
                            :data="purchaseDivideOrder.assetsItems"
                            border
                            style="width: 100%"
                        >
                            <el-table-column type="index" label="编号" />
                            <el-table-column prop="materialType" label="材料类型"></el-table-column>
                            <el-table-column prop="materialName" label="材料名称" />
                            <el-table-column
                                prop="materialSpecification"
                                label="材料规格"
                            ></el-table-column>
                            <el-table-column prop="color" label="颜色" />
                            <el-table-column prop="unit" label="单位" />
                            <el-table-column prop="purchaseAmount" label="采购数量" />
                            <el-table-column prop="remark" label="备注" />
                        </el-table>
                    </div>
                </el-col>
            </el-row>
        </div>
        <template #footer>
            <span>
                <el-button type="primary" @click="purchaseOrderVis = false">确认</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        :title="`创建尺码型号采购订单 ${newSizePurchaseOrderId}`"
        v-model="isLastPurchaseOrderDialogVisible"
        :close-on-click-modal="false"
        width="80%"
    >
        <el-table :data="lastData" border stripe>
            <el-table-column prop="materialType" label="材料类型" />
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column prop="materialSpecification" label="材料规格">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.materialSpecification"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="颜色">
                <template #default="scope">
                    <el-select v-model="scope.row.color" placeholder="" filterable>
                        <el-option
                            v-for="item in colorOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="warehouseName" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column prop="supplierName" label="工厂名称"> </el-table-column>
            <el-table-column label="型号填写">
                <template #default="scope">
                    {{ scope.row.sizeStatus }}
                    <el-button type="primary" size="default" @click="openSizeDialog(scope.row, scope.$index, 0)"
                        >尺码信息</el-button
                    >
                </template>
            </el-table-column>
            <el-table-column label="备注">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.comment"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button
                        type="danger"
                        @click="deleteCurrentRow(scope.$index, lastData)"
                        >删除</el-button
                    >
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" size="default" @click="openNewMaterialDialog(1)"
            >添加新材料</el-button
        >
        <template #footer>
            <span>
                <el-button @click="isLastPurchaseOrderDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="newSizePurchaseOrderSave">保存</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        title="尺码数量填写"
        v-model="isSizeDialogVisible"
        width="60%"
        :close-on-click-modal="false"
    >
        <el-table :data="sizeData" border stripe>
            <el-table-column prop="size" label="尺码"></el-table-column>
            <el-table-column prop="innerSize" label="内码"></el-table-column>
            <el-table-column prop="outterSize" label="外显"></el-table-column>
            <el-table-column label="采购数量">
                <template #default="scope">
                    <el-input-number v-model="scope.row.purchaseAmount" :min="0" size="small" />
                </template>
            </el-table-column>
        </el-table>

        <template #footer>
            <span>
                <el-button type="primary" @click="confirmSizeAmount(currentSizeData)">确认</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        title="采购订单创建页面"
        v-model="isPurchaseOrderVis"
        width="80%"
        :close-on-click-modal="false"
    >
        <el-tabs v-model="activeTab" type="card" tab-position="top">
            <el-tab-pane
                v-for="item in tabPlaneData"
                :key="item.purchaseDivideOrderId"
                :label="item.purchaseDivideOrderId + '    ' + item.supplierName"
                :name="item.purchaseDivideOrderId"
                style="min-height: 500px"
            >
                <el-row :gutter="20">
                    <el-col :span="12" :offset="0"
                        ><span
                            >订单备注：
                            <el-input
                                v-model="item.remark"
                                placeholder=""
                                type="textarea"
                                resize="none"
                                size="normal"
                                clearable
                            ></el-input> </span
                    ></el-col>
                    <el-col :span="12" :offset="0">
                        <span
                            >环境要求：
                            <el-input
                                v-model="item.evironmentalRequest"
                                placeholder=""
                                type="textarea"
                                resize="none"
                                size="normal"
                                clearable
                            ></el-input>
                        </span>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12" :offset="0">
                        <span
                            >发货地址：
                            <el-input
                                v-model="item.shipmentAddress"
                                placeholder=""
                                type="textarea"
                                resize="none"
                                size="normal"
                                clearable
                            ></el-input>
                        </span>
                    </el-col>
                    <el-col :span="12" :offset="0">
                        <span
                            >交货周期：
                            <el-input
                                v-model="item.shipmentDeadline"
                                placeholder=""
                                type="textarea"
                                resize="none"
                                size="normal"
                                clearable
                            ></el-input>
                        </span>
                    </el-col>
                </el-row>
                <el-row :gutter="20" style="margin-top: 20px">
                    <el-col :span="24" :offset="0">
                        <div v-if="factoryFieldJudge(item.purchaseDivideOrderType)">
                            <el-table
                                :data="item.assetsItems"
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
                            <el-table :data="item.assetsItems" border stripe height="500">
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
                                <el-table-column prop="color" label="颜色" />
                                <el-table-column prop="unit" label="单位" />
                                <el-table-column prop="purchaseAmount" label="数量" />
                                <el-table-column prop="remark" label="备注" />
                            </el-table>
                        </div>
                    </el-col>
                </el-row>
            </el-tab-pane>
        </el-tabs>

        <template #footer>
            <span>
                <el-button @click="isPurchaseOrderVis = false">取消</el-button>
                <el-button type="primary" @click="saveUnsubmitPurchaseOrder">保存</el-button>
                <el-button type="success" @click="confirmSubmitPurchaseOrder">提交</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        :title="`耗材/固定资产采购订单 ${editPurchaseOrderId} 修改`"
        v-model="editVis"
        width="95%"
        @close="handleGenerateClose"
        :close-on-click-modal="false"
    >
        <el-table :data="editAssetPurchaseData" border height="450">
            <el-table-column prop="materialType" label="材料类型" />
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column label="材料规格">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.materialSpecification"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="颜色">
                <template #default="scope">
                    <el-select v-model="scope.row.color" placeholder="" filterable>
                        <el-option
                            v-for="item in colorOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="warehouseName" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column label="采购数量">
                <template #default="scope">
                    <el-input-number
                        v-model="scope.row.purchaseAmount"
                        :min="0"
                        size="small"
                        step="0.001"
                    />
                </template>
            </el-table-column>
            <el-table-column prop="supplierName" label="工厂名称"> </el-table-column>
            <el-table-column label="随订单采购/独立采购">
                <template #default="scope">
                    <el-select v-model="scope.row.isPurchaseOrder" placeholder="" filterable>
                        <el-option
                            v-for="item in isPurchaseOrderOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column label="订单编号">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.orderId"
                        placeholder=""
                        size="default"
                        clearable
                        :disabled="scope.row.isPurchaseOrder === 'G'"
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="备注">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.comment"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button
                        type="danger"
                        @click="deleteCurrentRow(scope.$index, editAssetPurchaseData)"
                        >删除</el-button
                    >
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" size="default" @click="openNewMaterialDialog(2)"
            >添加新材料</el-button
        >

        <template #footer>
            <span>
                <el-button @click="editVis = false">取消</el-button>
                <el-button type="primary" @click="editPurchaseOrderSave">保存</el-button>
            </span>
        </template>
    </el-dialog>
    <el-dialog
        :title="`编辑尺码型号采购订单 ${editPurchaseOrderId}`"
        v-model="editLastPurchaseOrderDialogVisible"
        :close-on-click-modal="false"
        width="80%"
    >
        <el-table :data="editLastData" border stripe>
            <el-table-column prop="materialType" label="材料类型" />
            <el-table-column prop="materialName" label="材料名称" />
            <el-table-column prop="materialSpecification" label="材料规格">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.materialSpecification"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="颜色">
                <template #default="scope">
                    <el-select v-model="scope.row.color" placeholder="" filterable>
                        <el-option
                            v-for="item in colorOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="warehouseName" label="所属仓库" />
            <el-table-column prop="unit" label="单位" />
            <el-table-column prop="supplierName" label="工厂名称"> </el-table-column>
            <el-table-column label="型号填写">
                <template #default="scope">
                    {{ scope.row.sizeStatus }}
                    <el-button type="primary" size="default" @click="openSizeDialog(scope.row, scope.$index, 1)"
                        >尺码信息</el-button
                    >
                </template>
            </el-table-column>
            <el-table-column label="备注">
                <template #default="scope">
                    <el-input
                        v-model="scope.row.comment"
                        placeholder=""
                        size="default"
                        clearable
                    ></el-input>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button
                        type="danger"
                        @click="deleteCurrentRow(scope.$index, editLastData)"
                        >删除</el-button
                    >
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" size="default" @click="openNewMaterialDialog(3)"
            >添加新材料</el-button
        >
        <template #footer>
            <span>
                <el-button @click="editLastPurchaseOrderDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="editSizePurchaseOrderSave">保存</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import { Search } from '@element-plus/icons-vue'
import { markRaw } from 'vue'
import { ElMessageBox } from 'element-plus'
import axios from 'axios'
export default {
    data() {
        return {
            currentSizeData: 0,
            editVis: false,
            editPurchaseOrderId: '',
            editAssetPurchaseData: [],
            editLastPurchaseOrderDialogVisible: false,
            editLastData: [],
            currentSizeIndex: 0,
            currentViewPurchaseOrderId: '',
            currentSubmitPurchaseOrderId: '',
            currentCreateViewId: 0,
            unsubmitfinished: true,
            materialAddfinished: true,
            newPurchaseOrderId: '',
            newSizePurchaseOrderId: '',
            datafinished: true,
            activeTab: '',
            isPurchaseOrderVis: false,
            isSizeDialogVisible: false,
            isLastPurchaseOrderDialogVisible: false,
            sizeData: [],
            lastData: [],
            colorOptions: [],
            finishedNum: 1,
            materialSearch: '',
            materialTypeSearch: '',
            factorySearch: '',
            unsubmitVis: false,
            createVis: false,
            newMaterialVis: false,
            purchaseOrderVis: false,
            orderSearch: '',
            assetsTypeSearch: '',
            isPurchaseOrderFilter: '',
            addAssetName: '',
            isPurchaseOrderOptions: [
                { value: 'O', label: '随订单采购' },
                { value: 'G', label: '独立采购' }
            ],
            assetTable: [],
            assetFilterTable: [],
            unsubmitPurchaseOrder: [],
            Search: markRaw(Search),
            materialPurchaseTestData: [],
            materialPurchaseFilterData: [],
            selectedRow: null,
            materialSelectRow: null,
            newAssetPurchaseData: [],
            factoryOptions: [],
            tabPlaneData: []
        }
    },
    mounted() {
        this.getMaterialPurchaseData()
        this.getColors()
    },
    methods: {
        async getPurchaseOrderId() {
            const response = await axios.post(
                `${this.$apiBaseUrl}/logistics/getassetsnewpurchaseorderid`,
                {
                    department: '01'
                }
            )
            this.newPurchaseOrderId = response.data.newId
        },
        async getSizePurchaseOrderId() {
            const response = await axios.post(
                `${this.$apiBaseUrl}/logistics/getassetsnewpurchaseorderid`,
                {
                    department: '01'
                }
            )
            this.newSizePurchaseOrderId = response.data.newId
        },
        async getMaterialPurchaseData() {
            this.datafinished = true
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/assetsmaterialpurchaseorder`,
                {
                    params: {
                        purchaseorderstatus: '1'
                    }
                }
            )
            this.materialPurchaseTestData = response.data
            this.materialPurchaseFilterData = this.materialPurchaseTestData
            this.datafinished = false
        },
        async getUnsubmitPurchaseOrder() {
            this.unsubmitfinished = true
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/assetsmaterialpurchaseorder`,
                {
                    params: {
                        purchaseorderstatus: '0'
                    }
                }
            )
            this.unsubmitPurchaseOrder = response.data
            this.unsubmitfinished = false
        },
        async getSizeMaterialList() {
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getmaterialtypeandname`,
                {
                    params: {
                        materialcategory: 1
                    }
                }
            )
            this.assetTable = response.data
            this.assetFilterTable = this.assetTable
        },
        async getMaterialList() {
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getmaterialtypeandname`,
                {
                    params: {
                        materialcategory: 0
                    }
                }
            )
            this.assetTable = response.data
            this.assetFilterTable = this.assetTable
        },
        async getSizeMaterialFilterData() {
            this.materialAddfinished = true
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getmaterialtypeandname`,
                {
                    params: {
                        materialtype: this.materialTypeSearch,
                        materialname: this.materialSearch,
                        suppliername: this.factorySearch,
                        materialcategory: 1
                    }
                }
            )
            this.assetFilterTable = response.data
            this.materialAddfinished = false
        },
        async getMaterialFilterData() {
            this.materialAddfinished = true
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getmaterialtypeandname`,
                {
                    params: {
                        materialtype: this.materialTypeSearch,
                        materialname: this.materialSearch,
                        suppliername: this.factorySearch,
                        materialcategory: this.currentCreateViewId
                    }
                }
            )
            this.assetFilterTable = response.data
            this.materialAddfinished = false
        },
        async getColors() {
            const response = await axios.get(`${this.$apiBaseUrl}/general/allcolors`)
            this.colorOptions = response.data
        },
        factoryFieldJudge(type) {
            console.log(type)
            return type !== 'N'
        },
        openUnsubmitDialog() {
            this.unsubmitVis = true
            this.getUnsubmitPurchaseOrder()
        },
        openCreateSizeDialog() {
            this.currentCreateViewId = 1
            if (this.newSizePurchaseOrderId === '') {
                this.getSizePurchaseOrderId()
                this.isLastPurchaseOrderDialogVisible = true
            } else {
                this.$confirm('是否要创建新的采购订单？该操作会清空之前订单', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(async () => {
                        await this.getSizePurchaseOrderId()
                        this.lastData = []
                        this.isLastPurchaseOrderDialogVisible = true
                    })
                    .catch(() => {
                        this.$message({
                            type: 'info',
                            message: '已加载之前创建订单'
                        })
                        this.isLastPurchaseOrderDialogVisible = true
                    })
            }
        },
        openSizeDialog(row, index, type) {
            this.sizeData = row.sizeInfo
            this.isSizeDialogVisible = true
            this.currentSizeIndex = index
            this.currentSizeData = type
        },
        confirmSizeAmount(type) {
            if (type === 0) {
                this.lastData[this.currentSizeIndex].sizeInfo = this.sizeData
            }
            if (type === 1) {
                this.editLastData[this.currentSizeIndex].sizeInfo = this.sizeData
            }

            this.isSizeDialogVisible = false
        },
        handleSelectionChange(selection) {
            if (selection.length > 1) {
                // Ensure only one row is selected
                this.$refs.singleSelectTable.clearSelection()
                this.$refs.singleSelectTable.toggleRowSelection(
                    selection[selection.length - 1],
                    true
                )
            } else {
                this.selectedRow = selection[0]
            }
            console.log(this.selectedRow)
        },
        handleMaterialSelectionChange(selection) {
            if (selection.length > 1) {
                // Ensure only one row is selected
                this.$refs.materialSelectTable.clearSelection()
                this.$refs.materialSelectTable.toggleRowSelection(
                    selection[selection.length - 1],
                    true
                )
            } else {
                this.materialSelectRow = selection[0]
            }
            console.log(this.materialSelectRow)
        },
        async openCreateDialog() {
            this.currentCreateViewId = 0
            if (this.newPurchaseOrderId === '') {
                await this.getPurchaseOrderId()
                this.createVis = true
            } else {
                this.$confirm('是否要创建新的采购订单？该操作会清空之前订单', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                    .then(async () => {
                        await this.getPurchaseOrderId()
                        this.newAssetPurchaseData = []
                        this.createVis = true
                    })
                    .catch(() => {
                        this.$message({
                            type: 'info',
                            message: '已加载之前创建订单'
                        })
                        this.createVis = true
                    })
            }
        },
        async openNewMaterialDialog(type) {
            this.newMaterialVis = true
            this.materialAddfinished = true
            if (type == 1 || type == 3) {
                await this.getSizeMaterialList()
            } else if (type == 0 || type == 2) {
                await this.getMaterialList()
            }
            this.materialAddfinished = false
        },
        async openPreviewDialog(row) {
            this.currentViewPurchaseOrderId = row.materialPurchaseOrderId
            try {
                const response = await axios.get(
                    `${this.$apiBaseUrl}/logistics/getassetspurchasedivideorders`,
                    {
                        params: {
                            purchaseOrderId: row.materialPurchaseOrderId
                        }
                    }
                )
                this.purchaseTestData = response.data
                console.log(this.purchaseTestData)
            } catch (error) {
                console.log(error)
            }
            this.purchaseOrderVis = true
        },
        async openSubmitDialog(row) {
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getassetspurchasedivideorders`,
                {
                    params: {
                        purchaseOrderId: row.materialPurchaseOrderId
                    }
                }
            )
            this.currentSubmitPurchaseOrderId = row.materialPurchaseOrderId
            this.tabPlaneData = response.data
            this.activeTab = this.tabPlaneData[0].purchaseDivideOrderId
            this.isPurchaseOrderVis = true
        },
        async openEditDialog(row) {
            this.editPurchaseOrderId = row.materialPurchaseOrderId
            const response = await axios.get(
                `${this.$apiBaseUrl}/logistics/getassetspurchaseorderitems`,
                {
                    params: {
                        purchaseOrderId: row.materialPurchaseOrderId
                    }
                }
            )
            if (response.data.purchaseDivideOrderType === "N") {
                console.log(response.data)
                this.editAssetPurchaseData = response.data.data
                this.editVis = true
                this.currentCreateViewId = 2
            } else {
                this.editLastData = response.data.data
                this.editLastPurchaseOrderDialogVisible = true
                this.currentCreateViewId = 3
            }

        },
        confirmNewSizeMaterialAdd() {
            if (this.materialSelectRow === null) {
                ElMessageBox.alert('材料不能为空！', '警告', { confirmButtonText: '确认' })
                return
            }

            const isDuplicate = this.lastData.some(
                (item) => item.materialName === this.materialSelectRow.materialName
            )

            if (isDuplicate) {
                ElMessageBox.alert('材料名称必须唯一！', '警告', { confirmButtonText: '确认' })
                return
            }

            this.lastData.push({
                materialName: this.materialSelectRow.materialName,
                materialType: this.materialSelectRow.materialType,
                warehouseName: this.materialSelectRow.warehouseName,
                supplierName: this.materialSelectRow.supplierName,
                materialSpecification: this.materialSelectRow.materialSpecification,
                color: '',
                unit: this.materialSelectRow.unit,
                isPurchaseOrder: 'G',
                orderId: '',
                comment: '',
                sizeInfo: [
                    {
                        size: '35',
                        innerSize: '7',
                        outterSize: '7',
                        purchaseAmount: 0
                    },
                    {
                        size: '36',
                        innerSize: '7',
                        outterSize: '7.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '37',
                        innerSize: '8',
                        outterSize: '8',
                        purchaseAmount: 0
                    },
                    {
                        size: '38',
                        innerSize: '8',
                        outterSize: '8.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '39',
                        innerSize: '9',
                        outterSize: '9',
                        purchaseAmount: 0
                    },
                    {
                        size: '40',
                        innerSize: '9',
                        outterSize: '9.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '41',
                        innerSize: '10',
                        outterSize: '10',
                        purchaseAmount: 0
                    },
                    {
                        size: '42',
                        innerSize: '10',
                        outterSize: '10.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '43',
                        innerSize: '11',
                        outterSize: '11',
                        purchaseAmount: 0
                    },
                    {
                        size: '44',
                        innerSize: '12',
                        outterSize: '12',
                        purchaseAmount: 0
                    },
                    {
                        size: '45',
                        innerSize: '13',
                        outterSize: '13',
                        purchaseAmount: 0
                    }
                ]
            })
            this.addAssetName = ''
            this.newMaterialVis = false
            this.materialTypeSearch = ''
            this.materialSearch = ''
            this.factorySearch = ''
        },
        async saveUnsubmitPurchaseOrder() {
            this.$confirm('确定提交吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(async () => {
                    const response = await axios.post(
                        `${this.$apiBaseUrl}/logistics/unsubmitpurchaseordersave`,
                        {
                            data: this.tabPlaneData
                        }
                    )
                    if (response.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '提交成功'
                        })
                        this.isPurchaseOrderVis = false
                    } else {
                        this.$message({
                            type: 'error',
                            message: '提交失败'
                        })
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消提交'
                    })
                })
        },
        async confirmSubmitPurchaseOrder() {
            this.$confirm('确定提交吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(async () => {
                    const response = await axios.post(
                        `${this.$apiBaseUrl}/logistics/submitpurchaseorder`,
                        {
                            purchaseOrderId: this.currentSubmitPurchaseOrderId,
                        }
                    )
                    if (response.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '提交成功'
                        })
                        this.isPurchaseOrderVis = false
                        this.getUnsubmitPurchaseOrder()
                        this.getMaterialPurchaseData()
                    } else {
                        this.$message({
                            type: 'error',
                            message: '提交失败'
                        })
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消提交'
                    })
                })
        },
        confirmEditNewMaterialAdd() {
            if (this.materialSelectRow === null) {
                ElMessageBox.alert('材料不能为空！', '警告', { confirmButtonText: '确认' })
                return
            }

            const isDuplicate = this.editAssetPurchaseData.some(
                (item) => item.materialName === this.materialSelectRow.materialName
            )

            if (isDuplicate) {
                ElMessageBox.alert('材料名称必须唯一！', '警告', { confirmButtonText: '确认' })
                return
            }

            this.editAssetPurchaseData.push({
                materialName: this.materialSelectRow.materialName,
                materialType: this.materialSelectRow.materialType,
                warehouseName: this.materialSelectRow.warehouseName,
                supplierName: this.materialSelectRow.supplierName,
                materialSpecification: this.materialSelectRow.materialSpecification,
                color: '',
                unit: this.materialSelectRow.unit,
                purchaseAmount: 0,
                isPurchaseOrder: 'G',
                orderId: '',
                comment: ''
            })
            this.addAssetName = ''
            this.newMaterialVis = false
            this.materialTypeSearch = ''
            this.materialSearch = ''
            this.factorySearch = ''
        },
        confirmEditSizeNewMaterialAdd() {
            if (this.materialSelectRow === null) {
                ElMessageBox.alert('材料不能为空！', '警告', { confirmButtonText: '确认' })
                return
            }

            const isDuplicate = this.editLastData.some(
                (item) => item.materialName === this.materialSelectRow.materialName
            )

            if (isDuplicate) {
                ElMessageBox.alert('材料名称必须唯一！', '警告', { confirmButtonText: '确认' })
                return
            }

            this.editLastData.push({
                materialName: this.materialSelectRow.materialName,
                materialType: this.materialSelectRow.materialType,
                warehouseName: this.materialSelectRow.warehouseName,
                supplierName: this.materialSelectRow.supplierName,
                materialSpecification: this.materialSelectRow.materialSpecification,
                color: '',
                unit: this.materialSelectRow.unit,
                isPurchaseOrder: 'G',
                orderId: '',
                comment: '',
                sizeInfo: [
                    {
                        size: '35',
                        innerSize: '7',
                        outterSize: '7',
                        purchaseAmount: 0
                    },
                    {
                        size: '36',
                        innerSize: '7',
                        outterSize: '7.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '37',
                        innerSize: '8',
                        outterSize: '8',
                        purchaseAmount: 0
                    },
                    {
                        size: '38',
                        innerSize: '8',
                        outterSize: '8.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '39',
                        innerSize: '9',
                        outterSize: '9',
                        purchaseAmount: 0
                    },
                    {
                        size: '40',
                        innerSize: '9',
                        outterSize: '9.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '41',
                        innerSize: '10',
                        outterSize: '10',
                        purchaseAmount: 0
                    },
                    {
                        size: '42',
                        innerSize: '10',
                        outterSize: '10.5',
                        purchaseAmount: 0
                    },
                    {
                        size: '43',
                        innerSize: '11',
                        outterSize: '11',
                        purchaseAmount: 0
                    },
                    {
                        size: '44',
                        innerSize: '12',
                        outterSize: '12',
                        purchaseAmount: 0
                    },
                    {
                        size: '45',
                        innerSize: '13',
                        outterSize: '13',
                        purchaseAmount: 0
                    }
                ]
            })
            this.addAssetName = ''
            this.newMaterialVis = false
            this.materialTypeSearch = ''
            this.materialSearch = ''
            this.factorySearch = ''
        },
        confirmNewMaterialAdd() {
            if (this.materialSelectRow === null) {
                ElMessageBox.alert('材料不能为空！', '警告', { confirmButtonText: '确认' })
                return
            }

            const isDuplicate = this.newAssetPurchaseData.some(
                (item) => item.materialName === this.materialSelectRow.materialName
            )

            if (isDuplicate) {
                ElMessageBox.alert('材料名称必须唯一！', '警告', { confirmButtonText: '确认' })
                return
            }

            this.newAssetPurchaseData.push({
                materialName: this.materialSelectRow.materialName,
                materialType: this.materialSelectRow.materialType,
                warehouseName: this.materialSelectRow.warehouseName,
                supplierName: this.materialSelectRow.supplierName,
                materialSpecification: this.materialSelectRow.materialSpecification,
                color: '',
                unit: this.materialSelectRow.unit,
                purchaseAmount: 0,
                isPurchaseOrder: 'G',
                orderId: '',
                comment: ''
            })
            this.addAssetName = ''
            this.newMaterialVis = false
            this.materialTypeSearch = ''
            this.materialSearch = ''
            this.factorySearch = ''
        },
        getFilteredFactoryOptions(materialName) {
            const filteredOptions = this.factoryOptions.filter(
                (option) => option.materialName === materialName
            )
            return [{ supplierName: '询价' }, ...filteredOptions]
        },
        deleteCurrentRow(index, datafield) {
            this.$confirm('确定删除此行吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(() => {
                    datafield.splice(index, 1)
                    this.$message({
                        type: 'success',
                        message: '删除成功!'
                    })
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    })
                })
        },
        async newSizePurchaseOrderSave() {
            const response = await axios.post(
                `${this.$apiBaseUrl}/logistics/newpurchaseordersave`,
                {
                    data: this.lastData,
                    purchaseOrderId: this.newSizePurchaseOrderId,
                    purchaseDivideOrderType: 'S'
                }
            )
            if (response.status === 200) {
                this.$message({
                    type: 'success',
                    message: '保存成功'
                })
                this.lastData = []
                this.isLastPurchaseOrderDialogVisible = false
                this.newSizePurchaseOrderId = ''
            } else {
                this.$message({
                    type: 'error',
                    message: '保存失败'
                })
            }
        },
        async editSizePurchaseOrderSave() {
            const response = await axios.post(
                `${this.$apiBaseUrl}/logistics/editsavedpurchaseorderitems`,
                {
                    data: this.editLastData,
                    purchaseOrderId: this.editPurchaseOrderId,
                    purchaseDivideOrderType: 'S'
                }
            )
            if (response.status === 200) {
                this.$message({
                    type: 'success',
                    message: '保存成功'
                })
                this.editLastData = []
                this.editLastPurchaseOrderDialogVisible = false
                this.editSizePurchaseOrderId = ''
            } else {
                this.$message({
                    type: 'error',
                    message: '保存失败'
                })
            }
        },
        async editPurchaseOrderSave() {
            const response = await axios.post(
                `${this.$apiBaseUrl}/logistics/editsavedpurchaseorderitems`,
                {
                    data: this.editAssetPurchaseData,
                    purchaseOrderId: this.editPurchaseOrderId,
                    purchaseDivideOrderType: 'N'
                }
            )
            if (response.status === 200) {
                this.$message({
                    type: 'success',
                    message: '保存成功'
                })
                this.editAssetPurchaseData = []
                this.editVis = false
                this.editPurchaseOrderId = ''
            } else {
                this.$message({
                    type: 'error',
                    message: '保存失败'
                })
            }
        },
        async newPurchaseOrderSave() {
            const response = await axios.post(
                `${this.$apiBaseUrl}/logistics/newpurchaseordersave`,
                {
                    data: this.newAssetPurchaseData,
                    purchaseOrderId: this.newPurchaseOrderId,
                    purchaseDivideOrderType: 'N'
                }
            )
            if (response.status === 200) {
                this.$message({
                    type: 'success',
                    message: '保存成功'
                })
                this.newAssetPurchaseData = []
                this.createVis = false
                this.newPurchaseOrderId = ''
            } else {
                this.$message({
                    type: 'error',
                    message: '保存失败'
                })
            }
        },
        async deleteUnsubmitPurchaseOrder(row) {
            this.$confirm('确定删除此订单吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(async () => {
                        const response = await axios.delete(
                            `${this.$apiBaseUrl}/logistics/deleteunsubmitpurchaseorder`,
                            {
                                params: {
                                    purchaseOrderId: row.materialPurchaseOrderId
                                }
                            }
                        )
                    if (response.status === 200) {
                        this.$message({
                            type: 'success',
                            message: '删除成功'
                        })
                        this.getUnsubmitPurchaseOrder()
                    } else {
                        this.$message({
                            type: 'error',
                            message: '删除失败'
                        })
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    })
                })
        },
    }
}
</script>
