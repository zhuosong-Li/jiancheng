import app from '@/main';
import axios from 'axios';

export const getShoeSizesName = async (orderId) => {
    let params = { "orderId": orderId }
    let response = await axios.get(`${app.config.globalProperties.$apiBaseUrl}/batchtype/getorderbatchtype`, { params })
    return response.data
}
