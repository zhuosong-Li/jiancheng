import { ref } from 'vue';
import axios from 'axios';

export default function () {
    // 放进来是为了独立数据，防止因为响应式特性造成数据污染
    let materialData = ref({});

    async function getMaterialData(params) {
        const response = await axios.get(params.routeMsg, { params });
        materialData.value = response.data;
    }

    return { materialData, getMaterialData };
}
