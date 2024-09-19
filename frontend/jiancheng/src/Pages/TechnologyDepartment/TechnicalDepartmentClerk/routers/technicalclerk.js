import FirstBOMCreate from '../views/FirstBOMCreateView.vue'
import SecondBOMCreate from '../views/SecondBOMCreateView.vue'
export default [
  {
    path: '/technicalclerk/firstBOM/orderid=:orderId',
    name: 'technicalclerk-firstBOM',
    component: FirstBOMCreate,
    props: true,
    meta: {
      requiresAuth: true,
      role: 17
    }
  },
  {
    path: '/technicalclerk/secondBOM/orderid=:orderId',
    name: 'technicalclerk-secondBOM',
    component: SecondBOMCreate,
    props: true,
    meta: {
      requiresAuth: true,
      role: 17
    }
  },

]