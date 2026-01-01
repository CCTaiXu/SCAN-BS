<template>
  <div class="app-layout">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2 class="logo">
          <Icon type="ios-shield" />
          Solidity检测系统
        </h2>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">
          <Icon type="ios-home" />
          <span>主页</span>
        </router-link>

        <router-link to="/detect" class="nav-item">
          <Icon type="ios-search" />
          <span>漏洞检测</span>
        </router-link>

        <router-link to="/history" class="nav-item">
          <Icon type="ios-time" />
          <span>检测历史</span>
        </router-link>

        <router-link to="/guide" class="nav-item">
          <Icon type="ios-book" />
          <span>使用指南</span>
        </router-link>

        <router-link to="/system" class="nav-item">
          <Icon type="ios-desktop" />
          <span>系统信息</span>
        </router-link>

        <div class="nav-item logout-btn" @click="handleLogout">
          <Icon type="ios-log-out" />
          <span>退出登录</span>
        </div>
      </nav>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'AppLayout',
  setup() {
    const router = useRouter()

    const handleLogout = () => {
      // 清除登录状态
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 跳转到登录页
      router.push('/login')
    }

    return {
      handleLogout
    }
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.logo .ivu-icon {
  font-size: 24px;
  color: #667eea;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 24px;
  color: #5a6c7d;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-left-color: #667eea;
}

.nav-item.router-link-active {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
  border-left-color: #667eea;
}

.nav-item .ivu-icon {
  font-size: 18px;
  min-width: 18px;
}

.nav-item span {
  font-size: 15px;
}

.logout-btn {
  margin-top: auto;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  color: #e74c3c;
}

.logout-btn:hover {
  background: rgba(231, 76, 60, 0.1);
  color: #c0392b;
}

.main-content {
  flex: 1;
  overflow: auto;
  background: #f8f9fa;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 240px;
  }

  .nav-item {
    padding: 12px 20px;
  }

  .nav-item span {
    font-size: 14px;
  }
}
</style>