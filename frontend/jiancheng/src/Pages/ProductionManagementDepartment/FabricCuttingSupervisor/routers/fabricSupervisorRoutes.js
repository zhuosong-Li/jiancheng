import AmountReportList from '../views/AmountReportList.vue'
import PriceReport from '../views/PriceReportView.vue'

export default [
    {
        path: '/fabriccutting/amountreportlist',
        name: 'fabriccutting-amountreportlist',
        component: AmountReportList,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
            })
    },
    {
        path: '/fabriccutting/pricereport',
        name: 'fabriccutting-priceReport',
        component: PriceReport,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
            })
    }
]