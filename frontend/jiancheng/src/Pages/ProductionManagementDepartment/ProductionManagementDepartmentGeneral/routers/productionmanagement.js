import OrderDetails from '../components/OrderDetailView.vue'
import ProductionOutsourcePage from '../views/ProductionOutsourcePage.vue'
import ProductionAmountApprovalPage from '../views/ProductionAmountApprovalPage.vue'
import ProductionStatusTrackingPage from '../views/ProductionStatusTrackingPage.vue'
export default [
  {
    path: '/productiongeneral/productiondetail',
    name: 'inproduction-details',
    component: OrderDetails,
    props: route => (
      {
        orderId: route.query.orderId,
        orderRId: route.query.orderRId,
      }
    )
  },
  {
    path: '/productiongeneral/productionoutsource',
    name: 'outsource-page',
    component: ProductionOutsourcePage,
    props: route => (
      {
        orderId: route.query.orderId,
        orderShoeId: route.query.orderShoeId,
      }
    )
  },
  {
    path: '/productiongeneral/productionamountapproval',
    name: 'amount-approval',
    component: ProductionAmountApprovalPage,
    props: route => (
      {
        orderId: route.query.orderId,
        orderShoeId: route.query.orderShoeId,
      }
    )
  },
  {
    path: '/productiongeneral/productionstatustracking',
    name: 'production-status-tracking',
    component: ProductionStatusTrackingPage,
    props: route => (
      {
        orderId: route.query.orderId,
        orderShoeId: route.query.orderShoeId,
      }
    )
  }
]
