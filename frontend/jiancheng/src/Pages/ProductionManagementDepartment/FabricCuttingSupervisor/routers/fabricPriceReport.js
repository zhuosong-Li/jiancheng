import PriceReport from '../views/PriceReportView.vue'

export default [
    {
        path: '/fabriccutting/priceReport',
        name: 'fabriccutting-priceReport',
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