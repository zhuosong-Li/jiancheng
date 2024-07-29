import OrderShoeList from '../views/OrderShoeList.vue'
import AmountReportList from '../views/AmountReportList.vue'
import PriceReport from '../views/PriceReportView.vue'

export default [
    {
        path: '/sewingmachine/ordershoelist',
        name: 'sewingMachine-ordershoelist',
        component: OrderShoeList,
        props: route => (
            {
                orderId: route.query.orderId,
                createTime: route.query.createTime,
                prevTime: route.query.prevTime,
                prevDepart: route.query.prevDepart,
                prevUser: route.query.prevUser,
                orderType: route.query.orderType
            })
    },
    {
        path: '/sewingmachine/ordershoelist/amountreportlist',
        name: 'sewingMachine-ordershoelist-amountreportlist',
        component: AmountReportList,
        props: route => (
            {
                shoeTypeId: route.query.shoeTypeId,
                groupType: route.query.groupType
            })
    },
    {
        path: '/sewingmachine/pricereport',
        name: 'sewingMachine-priceReport',
        component: PriceReport,
        props: route => (
            {
                orderId: route.query.orderId,
                createTime: route.query.createTime,
                prevTime: route.query.prevTime,
                prevDepart: route.query.prevDepart,
                prevUser: route.query.prevUser,
                orderType: route.query.orderType
            })
    }
]