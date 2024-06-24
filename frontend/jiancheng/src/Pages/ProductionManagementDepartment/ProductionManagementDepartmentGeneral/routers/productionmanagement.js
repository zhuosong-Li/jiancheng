import OrderDetails from '../components/OrderDetailView.vue'

export default [
  {
    path: '/productiongeneral/productiondetail/customerid=:customerId',
    name: 'inproduction-details',
    component: OrderDetails,
    props: true
  }
]