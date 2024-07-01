import FirstWarehouseCreate from '../views/FirstWarehousingView.vue'
import SecondWarehouseCreate from '../views/SecondWarehousingView.vue'
export default [
  {
    path: '/headofwarehouse/firstWarehousing/orderid=:orderId',
    name: 'headofwarehouse-firstWarehousing',
    component: FirstWarehouseCreate,
    props: true
  },
  {
    path: '/headofwarehouse/secondWarehousing/orderid=:orderId',
    name: 'headofwarehouse-secondWarehousing',
    component: SecondWarehouseCreate,
    props: true
  },
]