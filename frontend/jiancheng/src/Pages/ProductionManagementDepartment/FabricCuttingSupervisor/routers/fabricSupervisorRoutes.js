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
                orderRId: route.query.orderRId,
                orderShoeId: route.query.orderShoeId,
                shoeRId: route.query.shoeRId,
                customerName: route.query.customerName,
                productionStartDate: route.query.productionStartDate,
                productionEndDate: route.query.productionEndDate
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
                orderShoeId: route.query.orderShoeId,
                shoeRId: route.query.shoeRId,
                customerName: route.query.customerName,
                productionStartDate: route.query.productionStartDate,
                productionEndDate: route.query.productionEndDate
            })
    }
]