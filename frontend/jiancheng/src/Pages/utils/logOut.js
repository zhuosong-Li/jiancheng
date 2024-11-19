import app from '@/main';
import axios from 'axios'

export const logout = async () => {
    await axios.post(`${app.config.globalProperties.$apiBaseUrl}/logout`)
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    app.config.globalProperties.$router.push('/login')
}
