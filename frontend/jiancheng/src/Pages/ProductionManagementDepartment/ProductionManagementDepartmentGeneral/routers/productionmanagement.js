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
        orderStartDate: route.query.orderStartDate,
        orderEndDate: route.query.orderEndDate,
        taskName: route.query.taskName,
        customerName: route.query.customerName,
        orderTotalShoes: route.query.orderTotalShoes
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
        orderRId: route.query.orderRId,
        orderShoeId: route.query.orderShoeId,
        shoeRId: route.query.shoeRId,
        orderStartDate: route.query.orderStartDate,
        orderEndDate: route.query.orderEndDate,
        customerName: route.query.customerName,
      }
    )
  },
  {
    path: '/productiongeneral/productionamountapproval',
    name: 'amount-approval',
    component: ProductionAmountApprovalPage,
    props: route => (
      {
        orderRId: route.query.orderRId,
        orderShoeId: route.query.orderShoeId,
        shoeRId: route.query.shoeRId,
        orderEndDate: route.query.orderEndDate,
        customerProductName: route.query.customerProductName,
      }
    )
  },
  {
    path: '/productiongeneral/productionstatustracking',
    name: 'production-status-tracking',
    component: ProductionStatusTrackingPage,
    props: route => (
      {
        orderRId: route.query.orderRId,
        orderShoeId: route.query.orderShoeId,
      }
    )
  }
]
