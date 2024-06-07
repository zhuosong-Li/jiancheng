import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GeneralManager from '../Pages/GeneralManager/GeneralManager/views/GeneralManager.vue'
import Logistics from '../Pages/LogisticsControlDepartment/LogisticsControlManager/views/LogisticsControlManager.vue'
import ProductionManagementDepartmentGeneral from '../Pages/ProductionManagementDepartment/ProductionManagementDepartmentGeneral/views/ProductionManagementDepartmentGeneral.vue'
import ProductionManager from '../Pages/ProductionManagementDepartment/ProductionManager/views/ProductionManager.vue'
import TechenicaDepartmentClerk from '../Pages/TechnologyDepartment/TechnicalDepartmentClerk/views/TechnicalDepartmentClerk.vue'
import TechnicalManager from '../Pages/TechnologyDepartment/TechnicalManager/views/TechnicalManager.vue'
import HeadOfWareHouse from '../Pages/TotalWarehouse/HeadOfWarehouse/views/HeadOfWarehouse.vue'
import FabricCuttingSupervisor from '../Pages/ProductionManagementDepartment/FabricCuttingSupervisor/views/FabricCuttingSupervisor.vue'
import SewingMachineSupervisor from '../Pages/ProductionManagementDepartment/SewingMachineSupervisor/views/SewingMachineSupervisor.vue'
import MoldingSupervisor from '../Pages/ProductionManagementDepartment/MoldingSupervisor/views/MoldingSupervisor.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path :'/generalmanager',
      name : 'generalmanager',
      component: GeneralManager
    },
    {
      path :'/logistics',
      name : 'logistics',
      component: Logistics
    },
    {
      path :'/productiongeneral',
      name : 'productiongeneral',
      component: ProductionManagementDepartmentGeneral
    },
    {
      path :'/productionmanager',
      name : 'productionmanager',
      component: ProductionManager
    },
    {
      path :'/technicalclerk',
      name : 'technicalclerk',
      component: TechenicaDepartmentClerk
    },
    {
      path :'/technicalmanager',
      name : 'technicalmanager',
      component: TechnicalManager
    },
    {
      path :'/headofwarehouse',
      name : 'headofwarehouse',
      component: HeadOfWareHouse
    },
    {
      path :'/fabriccutting',
      name : 'fabriccutting',
      component: FabricCuttingSupervisor
    },
    {
      path :'/sewingmachine',
      name : 'sewingmachine',
      component: SewingMachineSupervisor
    },
    {
      path :'/molding',
      name : 'molding',
      component: MoldingSupervisor
    },
    
  ]
})

export default router
