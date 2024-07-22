
import OrderDetails from '../components/OrderDetailView.vue'
import ProrductionOutsourcePage from '../views/ProrductionOutsourcePage.vue'
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
    component: ProrductionOutsourcePage,
    props: true
  }
  
]