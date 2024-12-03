import QuantityReportList from '../../ProductionSharedPages/QuantityReportPages/QuantityReportList.vue'
import PriceReportView from '../../ProductionSharedPages/PriceReportPages/PriceReportView.vue'

export default [
    {
        path: '/fabriccutting/amountreportlist',
        name: 'fabriccutting-amountreportlist',
        component: QuantityReportList,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
                team: route.query.team
            })
    },
    {
        path: '/fabriccutting/pricereport',
        name: 'fabriccutting-priceReport',
        component: PriceReportView,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
                teams: route.query.teams
            })
    }
]