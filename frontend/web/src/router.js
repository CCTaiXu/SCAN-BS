import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from './components/UserLogin.vue'
import AppLayout from './components/AppLayout.vue'
import VulnerabilityDetect from './components/VulnerabilityDetect.vue'
import DetectionHistory from './components/DetectionHistory.vue'
import UserGuide from './components/UserGuide.vue'
import SystemInfo from './components/SystemInfo.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/',
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('./components/Dashboard.vue')
      },
      {
        path: '/detect',
        name: 'Detect',
        component: VulnerabilityDetect
      },
      {
        path: '/history',
        name: 'History',
        component: DetectionHistory
      },
      {
        path: '/guide',
        name: 'Guide',
        component: UserGuide
      },
      {
        path: '/system',
        name: 'System',
        component: SystemInfo
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router