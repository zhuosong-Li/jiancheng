import AdjustUpload from "../views/AdjustUpload.vue";
export default [
    {
        path: '/technicalmanager/uploadprocesssheet/orderid=:orderId',
        name: 'technicalmanager-uploadprocesssheet',
        component: AdjustUpload,
        props: true,
        meta: {
          requiresAuth: true,
          role: 5
        }
    }
]