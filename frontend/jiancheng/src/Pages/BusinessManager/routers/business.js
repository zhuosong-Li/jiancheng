import BusinessOrderDetail from '../views/BusinessOrderDetail.vue'
export default [
  {
    path: '/business/businessorderdetail/orderid=:orderId',
    name: 'business-orderdetail',
    component: BusinessOrderDetail,
    props: true,
    meta: {
      requiresAuth: true,
      role: 4
    }
  },
  // {
  //   path: '/logistics/secondpurchase/orderid=:orderId',
  //   name: 'logistics-secondpurchase',
  //   component: SecondLogisticsOrder,
  //   props: true,
  //   meta: {
  //     requiresAuth: true,
  //     role: 9
  //   }
  // },
  // {
  //   path: '/testgraph',
  //   name: 'testgraph',
  //   component: TestGraph,
  //   props: true,
  //   meta: {
  //     requiresAuth: true,
  //     role: 9
  //   }
  // },
]