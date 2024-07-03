1.所有页面header,aside格式见根目录下/components/PageModel.vue 中代码
2.所有页面测试路径如下 操作时请不要更改非负责路径下内容
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path :'/generalmanager', 总经理页面
      name : 'generalmanager',
      component: GeneralManager
    },
    {
      path :'/logistics', 物控经理页面
      name : 'logistics',
      component: Logistics
    },
    {
      path :'/productiongeneral', 生产副总页面
      name : 'productiongeneral',
      component: ProductionManagementDepartmentGeneral
    },
    {
      path :'/productionmanager', 生产经理页面
      name : 'productionmanager',
      component: ProductionManager
    },
    {
      path :'/technicalclerk', 技术文员页面
      name : 'technicalclerk',
      component: TechenicaDepartmentClerk
    },
    {
      path :'/technicalmanager', 技术经理页面
      name : 'technicalmanager',
      component: TechnicalManager
    },
    {
      path :'/headofwarehouse', 总仓页面
      name : 'headofwarehouse',
      component: HeadOfWareHouse
    },
    {
      path :'/fabriccutting', 裁断主任页面
      name : 'fabriccutting',
      component: FabricCuttingSupervisor
    },
    {
      path :'/sewingmachine', 针车主任页面
      name : 'sewingmachine',
      component: SewingMachineSupervisor
    },
    {
      path :'/molding', 成型主任页面
      name : 'molding',
      component: MoldingSupervisor
    },

npm 更改国内源
$ npm config set registry http://registry.npm.taobao.org
$ npm get registry

鞋类名词中英文对照
https://annic159.pixnet.net/blog/post/117310922

