import LogisticsOrder from '../views/FirstOrderBOMView.vue'

export default [
  {
    path: '/logistics/firstpurchase/orderid=:orderId',
    name: 'logistics-firstpurchase',
    component: LogisticsOrder,
    props: true
  }
]