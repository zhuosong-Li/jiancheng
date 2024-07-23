import OrderDetails from '../components/OrderDetailView.vue'
import ProductionOutsourcePage from '../views/ProductionOutsourcePage.vue'
import ProductionAmountApprovalPage from '../views/ProductionAmountApprovalPage.vue'
export default [
  {
    path: '/productiongeneral/productiondetail/customerid=:customerId',
    name: 'inproduction-details',
    component: OrderDetails,
    props: true
  },
  {
    path: '/productiongeneral/productionoutsource/orderid=:orderId&ordershoeid=:orderShoeId',
    name: 'outsource-page',
    component: ProductionOutsourcePage,
    props: true
  },
  {
    path: '/productiongeneral/productionamountapproval/orderid=:orderId&ordershoeid=:orderShoeId',
    name: 'amount-approval',
    component: ProductionAmountApprovalPage,
    props: true
  }
]
