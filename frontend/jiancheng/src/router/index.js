import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginPage from '@/Pages/LoginPage.vue'
import GeneralManager from '../Pages/GeneralManager/GeneralManager/views/GeneralManager.vue'
import Logistics from '../Pages/LogisticsControlDepartment/LogisticsControlManager/views/LogisticsControlManager.vue'
import ProductionManagementDepartmentGeneral from '../Pages/ProductionManagementDepartment/ProductionManagementDepartmentGeneral/views/ProductionManagementDepartmentGeneral.vue'
import ProductionManager from '../Pages/ProductionManagementDepartment/ProductionManager/views/ProductionManager.vue'
import TechenicalDepartmentClerk from '../Pages/TechnologyDepartment/TechnicalDepartmentClerk/views/TechnicalDepartmentClerk.vue'
import TechnicalManager from '../Pages/TechnologyDepartment/TechnicalManager/views/TechnicalManager.vue'
import HeadOfWareHouse from '../Pages/TotalWarehouse/HeadOfWarehouse/views/HeadOfWarehouse.vue'
import FabricCuttingSupervisor from '../Pages/ProductionManagementDepartment/FabricCuttingSupervisor/views/FabricCuttingSupervisor.vue'
import SewingMachineSupervisor from '../Pages/ProductionManagementDepartment/SewingMachineSupervisor/views/SewingMachineSupervisor.vue'
import MoldingSupervisor from '../Pages/ProductionManagementDepartment/MoldingSupervisor/views/MoldingSupervisor.vue'
import UsageCalculation from '../Pages/UsageCalculation/views/UsageCalculation.vue'
import BussinessManager from '@/Pages/BussinessManager/views/BussinessManager.vue'
import DevelopmentManager from '@/Pages/DevelopmentManager/views/DevelopmentManager.vue'
import HumanResourcesDepartment from '@/Pages/HumanResourcesDepartment/views/HumanResourcesDepartment.vue'

//引入子路由
import LogisticsRoutes from '../Pages/LogisticsControlDepartment/LogisticsControlManager/routers/logistics'
import ProductionRoutes from '../Pages/ProductionManagementDepartment/ProductionManagementDepartmentGeneral/routers/productionmanagement'
import TechenicalDepartmentClerkRoutes from '../Pages/TechnologyDepartment/TechnicalDepartmentClerk/routers/technicalclerk'
import HeadOfWarehouseRoutes from '../Pages/TotalWarehouse/HeadOfWarehouse/routers/totalWarehouse'
import FabricSupervisorRoutes from '../Pages/ProductionManagementDepartment/FabricCuttingSupervisor/routers/fabricSupervisorRoutes'
import SewingSupervisorRoutes from '../Pages/ProductionManagementDepartment/SewingMachineSupervisor/routers/sewingSupervisorRoutes'
import MoldingSupervisorRoutes from '../Pages/ProductionManagementDepartment/MoldingSupervisor/routers/moldingSupervisorRoutes'
import DeputyGeneral from '@/Pages/ProductionManagementDepartment/ProductionManager/routers/DeputyGeneral'
import UsageCalculationRoutes from '../Pages/UsageCalculation/routers/UsageCalculation'
import DevelopmentManagerRoutes from '@/Pages/DevelopmentManager/routers/DevelopmentManager'
import TechnicalManagerRoutes from '../Pages/TechnologyDepartment/TechnicalManager/routers/technicalManager'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path :'/generalmanager',
      name : 'generalmanager',
      component: GeneralManager,
      meta:{
        requiresAuth: true,
        role: 2
      }
    },
    {
      path :'/logistics',
      name : 'logistics',
      component: Logistics,
      meta:{
        requiresAuth: true,
        role: 9
      }
    },
    {
      path :'/productiongeneral',
      name : 'productiongeneral',
      component: ProductionManagementDepartmentGeneral,
      meta:{
        requiresAuth: true,
        role: 3
      }
    },
    {
      path :'/productionmanager',
      name : 'productionmanager',
      component: ProductionManager,
      meta:{
        requiresAuth: true,
        role: 6
      }
    },
    {
      path :'/technicalclerk',
      name : 'technicalclerk',
      component: TechenicalDepartmentClerk,
      meta:{
        requiresAuth: true,
        role: 17
      }
    },
    {
      path :'/technicalmanager',
      name : 'technicalmanager',
      component: TechnicalManager,
      meta:{
        requiresAuth: true,
        role: 5
      }
    },
    {
      path :'/headofwarehouse',
      name : 'headofwarehouse',
      component: HeadOfWareHouse,
      meta:{
        requiresAuth: true,
        role: 8
      }
    },
    {
      path :'/fabriccutting',
      name : 'fabriccutting',
      component: FabricCuttingSupervisor,
      meta:{
        requiresAuth: true,
        role: 11
      }
    },
    {
      path :'/sewingmachine',
      name : 'sewingmachine',
      component: SewingMachineSupervisor,
      meta:{
        requiresAuth: true,
        role: 12
      }
    },
    {
      path :'/molding',
      name : 'molding',
      component: MoldingSupervisor,
      meta:{
        requiresAuth: true,
        role: 13
      }
    },
    {
      path :'/usagecalculation',
      name : 'usagecalculation',
      component: UsageCalculation,
      meta:{
        requiresAuth: true,
        role: 18
      }
    },
    {
      path :'/bussinessmanager',
      name : 'bussinessmanager',
      component: BussinessManager,
      meta:{
        requiresAuth: true,
        role: 4
      }
    },
    {
      path :'/developmentmanager',
      name : 'developmentmanager',
      component: DevelopmentManager,
      meta:{
        requiresAuth: true,
        role: 7
      }
    },
    {
      path :'/humanresourcesdepartment',
      name : 'humanresourcesdepartment',
      component: HumanResourcesDepartment,
      meta:{
        requiresAuth: true,
        role: 14
      }
    },
    ...LogisticsRoutes,
    ...ProductionRoutes,
    ...TechenicalDepartmentClerkRoutes,
    ...HeadOfWarehouseRoutes,
    ...FabricSupervisorRoutes,
    ...SewingSupervisorRoutes,
    ...MoldingSupervisorRoutes,
    ...DeputyGeneral,
    ...UsageCalculationRoutes,
    ...DevelopmentManagerRoutes,
    ...TechnicalManagerRoutes

  ]
})
import axios from 'axios'

const Logout = () => {
  axios.post('http://localhost:8000/logout')
  localStorage.removeItem('token');
  localStorage.removeItem('role');
}

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userRole = parseInt(localStorage.getItem('role'));
  console.log('token', token);
  console.log('userRole', userRole);
  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
      // If no token, redirect to login
      if (!token) {
        console.log('no token');
          next({ name: 'login' });
      } else {
          console.log(to.meta.role === userRole);
          // If the route has a role requirement, check the user's role
          if (to.meta.role && to.meta.role !== userRole) {
              Logout();
              // If role doesn't match, redirect to login or home
              next({ name: 'login' }); // or next({ name: 'Home' });
          } else {
              // Token and role are valid, allow access
              next();
          }
      }
  } else {
      // If the route doesn't require authentication, proceed as normal
      next();
  }
});

export default router
