import FirstLogisticsOrder from '../views/FirstOrderBOMView.vue'
import SecondLogisticsOrder from '../views/SecondOrderBOMView.vue'
export default [
  {
    path: '/logistics/firstpurchase/orderid=:orderId',
    name: 'logistics-firstpurchase',
    component: FirstLogisticsOrder,
    props: true
  },
  {
    path: '/logistics/secondpurchase/orderid=:orderId',
    name: 'logistics-secondpurchase',
    component: SecondLogisticsOrder,
    props: true
  },
]