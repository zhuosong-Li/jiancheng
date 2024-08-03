import OrderShoeList from '../views/OrderShoeList.vue'
import AmountReportList from '../views/AmountReportList.vue'
import PriceReport from '../views/PriceReportView.vue'

export default [
    {
        path: '/fabriccutting/ordershoelist',
        name: 'fabriccutting-ordershoelist',
        component: OrderShoeList,
        props: route => (
            {
                orderId: route.query.orderId,
                orderRId: route.query.orderRId,
                createTime: route.query.createTime,
                taskName: route.query.taskName,
                customerName: route.query.customerName
            })
    },
    {
        path: '/fabriccutting/ordershoelist/amountreportlist',
        name: 'fabriccutting-ordershoelist-amountreportlist',
        component: AmountReportList,
        props: route => (
            {
                orderId: route.query.orderId,
                orderRId: route.query.orderRId,
                createTime: route.query.createTime,
                customerName: route.query.customerName,
                orderShoeId: route.query.orderShoeId,
                shoeRId: route.query.shoeRId
            })
    },
    {
        path: '/fabriccutting/pricereport',
        name: 'fabriccutting-priceReport',
        component: PriceReport,
        props: route => (
            {
                orderId: route.query.orderId,
                orderRId: route.query.orderRId,
                createTime: route.query.createTime,
                taskName: route.query.taskName,
                customerName: route.query.customerName
            })
    }
]