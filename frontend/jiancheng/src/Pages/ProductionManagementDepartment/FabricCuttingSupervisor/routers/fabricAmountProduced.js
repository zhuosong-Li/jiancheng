import AmountProduced from '../views/AmountProducedView.vue'

export default [
    {
        path: '/fabriccutting/amountProduced',
        name: 'fabriccutting-amountProduced',
        component: AmountProduced,
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