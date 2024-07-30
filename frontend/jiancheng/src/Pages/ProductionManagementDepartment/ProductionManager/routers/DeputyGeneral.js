import OrdershoeOutSourceApprovalView from "../views/OrdershoeOutSourceApprovalView.vue"
import WagesApprovalPage from "../views/WagesApprovalPage.vue"
export default [

  {
    path: '/productionmanager/productionoutsource/orderid=:orderId&ordershoeid=:orderShoeId',
    name: 'deputy-outsource-page',
    component: OrdershoeOutSourceApprovalView,
    props: true
  },
  {
    path: '/productionmanager/productionwageapproval/orderid=:orderId&ordershoeid=:orderShoeId',
    name: 'wage-approval-page',
    component: WagesApprovalPage,
    props: true
  },

]
