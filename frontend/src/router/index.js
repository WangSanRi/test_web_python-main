import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/login.vue'
import Products from '../views/products.vue'
import Contact from '../views/contact.vue'
import Home from '../views/home.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
        meta: { requiresAuth: true }
    },
    {
        path: '/products',
        name: 'Products',
        component: Products,
        meta: { requiresAuth: true }
    },
    {
        path: '/contact',
        name: 'Contact',
        component: Contact,
        meta: { requiresAuth: true }
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})

// 全局路由守卫，用于验证用户是否登录
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth &&!localStorage.getItem('token')) {
    // 如果要访问的页面需要登录验证且本地存储中没有token（即未登录）
    next('/login');
  } else {
    next();
  }
});

// 最后导出初始化好的router
export default router;