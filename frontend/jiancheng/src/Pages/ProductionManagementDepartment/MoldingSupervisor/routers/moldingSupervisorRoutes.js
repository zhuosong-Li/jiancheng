import AmountReportList from '../views/AmountReportList.vue'
import PriceReport from '../views/PriceReportView.vue'

export default [
    {
        path: '/molding/amountreportlist',
        name: 'molding-amountreportlist',
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
        path: '/molding/pricereport',
        name: 'molding-priceReport',
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