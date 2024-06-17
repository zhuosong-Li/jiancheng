import FirstBOMCreate from '../views/FirstBOMCreateView.vue'
import SecondBOMCreate from '../views/SecondBOMCreateView.vue'
export default [
  {
    path: '/technicalclerk/firstBOM/orderid=:orderId',
    name: 'technicalclerk-firstBOM',
    component: FirstBOMCreate,
    props: true
  },
  {
    path: '/technicalclerk/secondBOM/orderid=:orderId',
    name: 'technicalclerk-secondBOM',
    component: SecondBOMCreate,
    props: true
  },
]