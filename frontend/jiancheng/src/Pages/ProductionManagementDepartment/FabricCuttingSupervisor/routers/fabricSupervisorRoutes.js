import ShoeTypeList from '../views/ShoeTypeList.vue'
import AmountReportList from '../views/AmountReportList.vue'
import PriceReport from '../views/PriceReportView.vue'

export default [
    {
        path: '/fabriccutting/shoetypelist',
        name: 'fabriccutting-shoetypelist',
        component: ShoeTypeList,
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
        path: '/fabriccutting/shoetypelist/amountreportlist',
        name: 'fabriccutting-shoetypelist-amountreportlist',
        component: AmountReportList,
        props: route => (
            {
                shoeTypeId: route.query.shoeTypeId,
                groupType: route.query.groupType
            })
    },
    {
        path: '/fabriccutting/pricereport',
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