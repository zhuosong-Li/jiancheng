import QuantityReportList from '../../ProductionSharedPages/QuantityReportPages/QuantityReportList.vue'

export default [
    {
        path: '/productionclerk/amountreportlist',
        name: 'productionclerk-amountreportlist',
        component: QuantityReportList,
        props: route => (
            {
                orderId: route.query.orderId,
                orderShoeId: route.query.orderShoeId,
                team: route.query.team
            }
        )
    },
]
