import QuantityReportList from '../../ProductionSharedPages/QuantityReportPages/QuantityReportList.vue'
import PriceReportView from '../../ProductionSharedPages/PriceReportPages/PriceReportView.vue'

export default [
    {
        path: '/sewingmachine/amountreportlist',
        name: 'sewingmachine-amountreportlist',
        component: QuantityReportList,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
                team: route.query.team
            })
    },
    {
        path: '/sewingmachine/pricereport',
        name: 'sewingmachine-priceReport',
        component: PriceReportView,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
                teams: route.query.teams
            })
    }
]