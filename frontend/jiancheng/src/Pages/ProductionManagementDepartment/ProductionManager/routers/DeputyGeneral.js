import OrdershoeOutSourceApprovalView from "../views/OrdershoeOutSourceApprovalView.vue"
export default [

  {
    path: '/productionmanager/productionoutsource/orderid=:orderId&ordershoeid=:orderShoeId',
    name: 'deputy-outsource-page',
    component: OrdershoeOutSourceApprovalView,
    props: true
  },
]
