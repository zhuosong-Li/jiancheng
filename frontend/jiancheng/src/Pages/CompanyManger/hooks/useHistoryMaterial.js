import { ref } from 'vue';
import axios from 'axios';

let apiBaseUrl = '';
fetch('/frontend_config.json')
    .then((response) => response.json())
    .then((config) => {
        apiBaseUrl = config.api_base_url
    });

export default function () {
    // 放进来是为了独立数据，防止因为响应式特性造成数据污染
    let materialData = ref({});

    async function getMaterialData(value) {
        const params = {
            id: value || ''
        }
        const response = await axios.get(`${apiBaseUrl}/后续路由`, { params });
        materialData.value = response.data.result;
    }

    return { materialData, getMaterialData };
}
