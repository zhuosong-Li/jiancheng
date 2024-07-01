<template>
  <el-container :direction="vertical">
      <el-header height="">
          <AllHeader></AllHeader>
      </el-header>
      <el-main height="">
          <el-row :gutter="20" style="text-align: center;">
              <el-col :span="24" :offset="0" style="font-size: xx-large; text-align: center;">订单生产详情</el-col>
          </el-row>
          <el-row :gutter="20">
              <el-col :span="24" :offset="0">
                  <el-descriptions title="订单信息" :column="2">
                      <el-descriptions-item label="客人编号">{{ testOrderData.customerId }}</el-descriptions-item>
                      <el-descriptions-item label="订单编号">{{ testOrderData.orderId}}</el-descriptions-item>
                      <el-descriptions-item label="订单创建时间">{{ testOrderData.createTime }}</el-descriptions-item>
                      <el-descriptions-item label="订单出货日期">{{testOrderData.deadLineTime}}</el-descriptions-item>
                      <!-- <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                      <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                      <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item>
                      <el-descriptions-item label="订单状态">{{ testOrderData.orderrStatus }}</el-descriptions-item> -->
                  </el-descriptions></el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 20px;">
              <el-col :span="24" :offset="0">
                  <el-table :data="testOrderData.productDataList" border style="height: 800px;">
                    <el-table-column type="expand">
                      <template #default="props">
                        <h3> 鞋型详情 </h3>
                        <el-table :data="props.row.grouping" :border="childBorder">
                            <el-table-column label="配码编号" prop="sizeQuant" />
                            <el-table-column label="订单总数" prop="totalQuant" />
                            <el-table-column label="面料辅料" prop="materialLogistics" />
                            <el-table-column label="扣件拉链鞋带" prop="metalmaterialLogistics" />
                            <el-table-column label="裁断进度" prop="fabricCuttingProgress" />
                            <el-table-column label="预备进度" prop="preproductionProgress" />
                            <el-table-column label="针车进度" prop="sewingProgress" />
                            <el-table-column label="鞋底物料" prop="soleLogistics" />
                            <el-table-column label="中底物料" prop="insoleLogistics" />
                            <el-table-column label="鞋盒物料" prop="packagingMaterialLogistics" />
                            <el-table-column label="楦型" prop="lasttypeLogistics" />
                            <el-table-column label="成型进度" prop="moldingProgress" />
                            <el-table-column label="出货日期" prop="shippingDate" />
                            <el-table-column label="出库状态" prop="deliveryStatus" />

                        </el-table>
                      </template>
                    </el-table-column>
                        
                        <!-- <el-table-column prop="imageurl" label="预览图">
                            <template slot-scope="scope">
                                <img :src="scope.row.imageurl"/>
                            </template>
                        </el-table-column> -->
                      <el-table-column label="预览图">
                      </el-table-column>
                      <el-table-column prop="localProductId" label="公司编号"></el-table-column>
                      <el-table-column prop="foreignProductId" label="客户型号"></el-table-column>
                      <el-table-column prop="color" label="颜色"></el-table-column>
                      <el-table-column prop="status" label="状态"></el-table-column>
                      <el-table-column prop="totalQuantity" label="当前鞋型订单总数"></el-table-column>
                      <el-table-column label="操作"> <template #default="scope">
                              <el-button v-if="scope.row.status === '未生成采购订单'" type="primary"
                                  @click="handleGenerate(scope.row)">生成</el-button>
                              <el-button v-else-if="scope.row.status === '已生成采购订单'" type="primary"
                                  @click="handleView(scope.row)">查看</el-button>
                              <div v-else-if="scope.row.status === '已保存采购订单'">
                                  <el-button type="primary" @click="handleGenerate(scope.row)">编辑</el-button>
                                  <el-button type="success" @click="openPreviewDialog(scope.row)">预览</el-button>
                                  <el-button type="warning" @click="handleConfirm(scope.row)">确认下发</el-button>
                              </div>
                          </template></el-table-column>
                  </el-table></el-col>
          </el-row>
          <el-dialog title="采购订单 K2402121116202024061101F" v-model="createVis" width="90%"
              @close="handleGenerateClose">
              <el-descriptions title="订单信息" :column="2">
                  <el-descriptions-item label="订单编号">{{ testOrderData.orderId }}</el-descriptions-item>
                  <el-descriptions-item label="订单创建时间">{{ testOrderData.createTime }}</el-descriptions-item>
                  <el-descriptions-item label="前序流程下发时间">{{ testOrderData.prevTime }}</el-descriptions-item>
                  <el-descriptions-item label="前序处理部门">{{ testOrderData.prevDepart }}</el-descriptions-item>
                  <el-descriptions-item label="前序处理人">{{ testOrderData.prevUser }}</el-descriptions-item>
                  <el-descriptions-item label="订单状态">{{ testOrderData.orderrStatus }}</el-descriptions-item>
                  <el-descriptions-item label="BOM编号">{{ testOrderData.orderrStatus }}</el-descriptions-item>
              </el-descriptions>
              <el-table :data="bomTestData" border style="height: 400px;">
                  <el-table-column prop="partName" label="部件名称" />
                  <el-table-column prop="color" label="颜色" />
                  <el-table-column prop="materialName" label="材料名称" />
                  <el-table-column prop="unit" label="单位" />
                  <el-table-column prop="unitUsage" label="单位用量" />
                  <el-table-column prop="approvedUsage" label="核定用量" />
                  <el-table-column label="采购数量">
                      <template #default="scope">
                          <el-input-number v-model="scope.row.purchaseAmount" :min="0" />
                      </template>
                  </el-table-column>
                  <el-table-column label="工厂名称">
                      <template #default="scope">
                          <el-select v-model="scope.row.factoryName" placeholder="选择工厂">
                              <el-option v-for="factory in getFilteredFactoryOptions(scope.row.materialName)"
                                  :key="factory.factoryName" :label="factory.factoryName"
                                  :value="factory.factoryName" />
                          </el-select>
                      </template>
                  </el-table-column>
                  <el-table-column prop="internalModel" label="公司型号" />
                  <el-table-column prop="customerModel" label="客户型号" />
              </el-table>

              <template #footer>
                  <span>
                      <el-button @click="handleGenerateClose">取消</el-button>
                      <el-button type="primary" @click="handleSave">保存</el-button>
                  </span>
              </template>
          </el-dialog>

          <el-dialog
              title="预览采购订单 K2402121116202024061101F"
              v-model="isPreviewDialogVisible"
              width="90%">
              <el-descriptions title="订单信息" :column="2">
                  <el-descriptions-item label="订单编号">{{ orderId }}</el-descriptions-item>
              </el-descriptions>
              <el-row :gutter="20">
                  <el-col :span="24" :offset="0"></el-col>
              </el-row>
              
              <template #footer>
              <span>
                  <el-button @click="handleCancel">Cancel</el-button>
                  <el-button type="primary" @click="handleSave">OK</el-button>
              </span>
              </template>
          </el-dialog>
          

          <!-- Main content -->
      </el-main>

  </el-container>

</template>

<script>
import AllHeader from '@/components/AllHeader.vue';
export default {
  props: ['orderId'],
  components: {
      AllHeader,
  },
  data() {
      return {
          createVis: false,
          testOrderData: {
              orderId: "2111620",
              customerId:"K24-020（1）客人37 ",
              createTime: "2024-02-27",
              deadLineTime: "2024-05-05",
              prevTime: "2024-06-11 12:00:00",
              prevDepart: "技术部",
              prevUser: "XXX",
              orderStatus: '生产中',
              productDataList: [{
                localProductId: "0E21922",
                foreignProductId: "170995",
                color: "黑色 BLACK",
                status: "生产中(成型60%：针车80%：裁断100%)",
                totalQuantity:'1800',
                imageurl:"../assets/2111620/0E21922.png",
                grouping:[
                    {sizeQuant:"S12A",
                    totalQuant:"768",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"200/768",
                    preproductionProgress:"768/768",
                    sewingProgress:"700/768",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"768/768",
                    shippingDate:"4/30",
                    deliveryStatus:"准备出库"
                    },
                    {
                    sizeQuant:"S12B",
                    totalQuant:"168",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"100/168",
                    preproductionProgress:"150/168",
                    sewingProgress:"150/168",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"168/168",
                    shippingDate:"4/30",
                    deliveryStatus:"已经出库"
                    },
                    {
                    sizeQuant:"S6A1",
                    totalQuant:"84",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"100/168",
                    preproductionProgress:"150/168",
                    sewingProgress:"150/168",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"168/168",
                    shippingDate:"4/30",
                    deliveryStatus:"已经出库"
                    },
                    {
                    sizeQuant:"S6A2",
                    totalQuant:"60",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"100/168",
                    preproductionProgress:"150/168",
                    sewingProgress:"150/168",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"168/168",
                    shippingDate:"4/30",
                    deliveryStatus:"已经出库"
                    },
                    {
                    sizeQuant:"S6B1",
                    totalQuant:"12",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"100/168",
                    preproductionProgress:"150/168",
                    sewingProgress:"150/168",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"168/168",
                    shippingDate:"4/30",
                    deliveryStatus:"已经出库"
                    },
                    {
                    sizeQuant:"S6B2",
                    totalQuant:"36",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"100/168",
                    preproductionProgress:"150/168",
                    sewingProgress:"150/168",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"168/168",
                    shippingDate:"4/30",
                    deliveryStatus:"已经出库"
                    },
                    {
                    sizeQuant:"S8A1",
                    totalQuant:"384",
                    materialLogistics:"3/11已定/已到",
                    metalmaterialLogistics:"3/12已定",
                    fabricCuttingProgress:"100/168",
                    preproductionProgress:"150/168",
                    sewingProgress:"150/168",
                    soleLogistics:"已到",
                    insoleLogistics:"3/13已定",
                    packagingMaterialLogistics:"已到",
                    lasttypeLogistics:"已到",
                    moldingProgress:"168/168",
                    shippingDate:"4/30",
                    deliveryStatus:"已经出库"
                    },

                ]
                },
                {
                  localProductId: "0E21922",
                  foreignProductId: "170995",
                  color: "褐色 TAUPE",
                  status: "生产中(成型70%：针车100%：裁断100%)"
                },
                {
                  localProductId: "0E19550",
                  foreignProductId: "171975",
                  color: "黑色 BLACK",
                  status: "未开始生产(成型物料到齐：针车物料未到齐：裁断物料到齐)"
                },
                {
                  localProductId: "0E19550",
                  foreignProductId: "171975",
                  color: "褐色 TAUPE",
                  status: "未开始生产(成型物料采购中:针车物料采购中：裁断物料到齐)"
                },]
          },
          testTableData: [{
              bomId: "K24021211162020240611180001",
              bomType: "一次采购BOM",
              bomLink: "0E20620,0E20621",
              Status: "未生成采购订单"
          },
          {
              bomId: "K24021211162020240611180002",
              bomType: "一次采购BOM",
              bomLink: "0E20620,0E20621",
              Status: "已生成采购订单"
          },
          {
              bomId: "K24021211162020240611180001",
              bomType: "一次采购BOM",
              bomLink: "0E20620,0E20621",
              Status: "已保存采购订单"
          },],
          bomTestData: [{
              partName: "鞋面",
              color: "黑色",
              materialName: "黑色超软镜面PU",
              unit: "米",
              unitUsage: 10.35,
              approvedUsage: 186,
              purchaseAmount: 0,
              factoryName: "",
              internalModel: "0E202620",
              customerModel: "VRA-1020"
          }],
          originalBomTestData: [],
          factoryOptions: [
              { materialName: '黑色超软镜面PU', factoryName: '一一鞋材' },
              { materialName: '黑色超软镜面PU', factoryName: '深源皮革' },
              { materialName: '黑色超软镜面PU', factoryName: '嘉泰皮革' },
              // Add more options here
          ],
          purchaseTestData:[{
              
          }],
          isPreviewDialogVisible: false,
          selectedFile: null
      }
  },
  methods: {
      handleGenerate() {
          this.originalBomTestData = JSON.parse(JSON.stringify(this.bomTestData));
          this.createVis = true
      },
      handleGenerateClose() {
          this.bomTestData = JSON.parse(JSON.stringify(this.originalBomTestData)); // Restore original data
          this.createVis = false;
      },
      getFilteredFactoryOptions(materialName) {
          const filteredOptions = this.factoryOptions.filter(option => option.materialName === materialName);
          return [{ factoryName: '询价' }, ...filteredOptions];
      },
      openPreviewDialog() {
          // Replace this with the actual logic to get the file
          this.isPreviewDialogVisible = true;
      },
      handleSave() {
      },
      handleCancel() {
      },
      handleConfirm() {
      },
      handleView(row) {
        return row.orderStatus
      }
  }
}
</script>

<style scoped>
/* Add your styles here */
</style>