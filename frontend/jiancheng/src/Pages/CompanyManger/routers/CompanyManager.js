import CostCalcAndProfitAnalysis from '../components/CostCalcAndProfitAnalysis/CostCalcAndProfitAnalysis.vue'

export default [
    {
        path: '/companyManager/content/orderid=:orderId',
        name: 'CostCalculation_And_ProfitAnalysis',
        component: CostCalcAndProfitAnalysis,
        props: true,
        meta: {
            requiresAuth: true,
            role: 2
        }
    }
]
