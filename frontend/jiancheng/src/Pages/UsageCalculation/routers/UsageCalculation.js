import UsageCalculationInput from "../views/UsageCalculationInput.vue";

export default [
    {
        path: '/usagecalculation/usagecalculationinput/orderid=:orderId',
        name: 'usagecalculation-usagecalculationinput',
        component: UsageCalculationInput,
        props: true
    }
]