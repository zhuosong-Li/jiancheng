import ProductionOrderCreateView from "../views/ProductionOrderCreateView.vue";

export default [
    {
        path: "/developmentmanager/productionorder/create/orderid=:orderId",
        name: "developmentmanager-productionorder-create",
        component: ProductionOrderCreateView,
        props: true,
        meta: {
            requiresAuth: true,
            role: 7
        }
    }
];