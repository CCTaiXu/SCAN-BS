<template>
  <div class="system-container">
    <div class="system-grid">
      <!-- 前端信息卡片 -->
      <Card class="info-card frontend-card" shadow>
        <template #title>
          <div class="card-header-custom">
            <div class="header-icon">
              <Icon type="ios-desktop" size="24" />
            </div>
            <div class="header-text">
              <h3>前端信息</h3>
              <p>客户端技术栈</p>
            </div>
          </div>
        </template>

        <div class="info-content">
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-code" />
                框架版本
              </div>
              <div class="info-value">
                <Tag color="success">Vue.js 3</Tag>
              </div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-color-palette" />
                UI框架
              </div>
              <div class="info-value">
                <Tag color="primary">View UI Plus</Tag>
              </div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-build" />
                构建工具
              </div>
              <div class="info-value">
                <Tag color="warning">Vue CLI 5</Tag>
              </div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-globe" />
                浏览器兼容
              </div>
              <div class="info-value">
                <Tag color="info">现代浏览器</Tag>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- 后端信息卡片 -->
      <Card class="info-card backend-card" shadow>
        <template #title>
          <div class="card-header-custom">
            <div class="header-icon">
              <Icon type="ios-server" size="24" />
            </div>
            <div class="header-text">
              <h3>后端信息</h3>
              <p>服务端技术栈</p>
            </div>
          </div>
        </template>

        <div class="info-content">
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-settings" />
                Web框架
              </div>
              <div class="info-value">
                <Tag color="success">FastAPI</Tag>
              </div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-nuclear" />
                AI模型
              </div>
              <div class="info-value">
                <Tag color="error">GNN + TensorFlow</Tag>
              </div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-code-working" />
                目标语言
              </div>
              <div class="info-value">
                <Tag color="primary">Solidity</Tag>
              </div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <Icon type="ios-lock" />
                认证方式
              </div>
              <div class="info-value">
                <Tag color="warning">JWT Token</Tag>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- 服务状态卡片 -->
      <Card class="status-card" shadow>
        <template #title>
          <div class="card-header-custom">
            <div class="header-icon">
              <Icon type="ios-heart" size="24" />
            </div>
            <div class="header-text">
              <h3>服务状态</h3>
              <p>系统运行状态监控</p>
            </div>
          </div>
        </template>

        <div class="status-content">
          <!-- API状态 -->
          <div class="status-item">
            <div class="status-info">
              <div class="status-name">
                <Icon type="ios-cloud" />
                后端API服务
              </div>
              <div class="status-url">
                <code>http://127.0.0.1:8000</code>
              </div>
            </div>
            <div class="status-indicator">
              <Tag :color="apiStatus ? 'success' : 'error'" size="large">
                <Icon :type="apiStatus ? 'ios-checkmark-circle' : 'ios-close-circle'" />
                {{ apiStatus ? '在线' : '离线' }}
              </Tag>
            </div>
          </div>

          <!-- 数据库状态 -->
          <div class="status-item">
            <div class="status-info">
              <div class="status-name">
                <Icon type="ios-folder" />
                用户数据库
              </div>
              <div class="status-url">
                SQLite (本地文件)
              </div>
            </div>
            <div class="status-indicator">
              <Tag color="success" size="large">
                <Icon type="ios-checkmark-circle" />
                正常
              </Tag>
            </div>
          </div>

          <!-- 模型状态 -->
          <div class="status-item">
            <div class="status-info">
              <div class="status-name">
                <Icon type="ios-nuclear" />
                GNN模型
              </div>
              <div class="status-url">
                TensorFlow 1.14
              </div>
            </div>
            <div class="status-indicator">
              <Tag :color="modelStatus ? 'success' : 'warning'" size="large">
                <Icon :type="modelStatus ? 'ios-checkmark-circle' : 'ios-alert'" />
                {{ modelStatus ? '已加载' : '未加载' }}
              </Tag>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="status-actions">
            <Button
              type="primary"
              :loading="checking"
              @click="checkAPI"
              size="large"
            >
              <Icon type="ios-refresh" />
              {{ checking ? '检查中...' : '刷新状态' }}
            </Button>
          </div>

          <!-- 状态信息 -->
          <div class="status-footer">
            <div class="last-check">
              <Icon type="ios-time" />
              最后检查: {{ lastCheckTime }}
            </div>
            <div class="uptime" v-if="apiStatus">
              <Icon type="ios-timer" />
              服务正常运行中
            </div>
          </div>
        </div>
      </Card>

      <!-- 系统资源卡片 -->
      <Card class="resource-card" shadow>
        <template #title>
          <div class="card-header-custom">
            <div class="header-icon">
              <Icon type="ios-speedometer" size="24" />
            </div>
            <div class="header-text">
              <h3>系统资源</h3>
              <p>性能和资源使用情况</p>
            </div>
          </div>
        </template>

        <div class="resource-content">
          <div class="resource-grid">
            <div class="resource-item">
              <div class="resource-label">
                <Icon type="ios-hardware-chip" />
                CPU使用率
              </div>
              <div class="resource-value">
                <Progress :percent="cpuUsage" :stroke-width="8" />
                <span class="percentage">{{ cpuUsage }}%</span>
              </div>
            </div>

            <div class="resource-item">
              <div class="resource-label">
                <Icon type="ios-server" />
                内存使用
              </div>
              <div class="resource-value">
                <Progress :percent="memoryUsage" :stroke-width="8" status="warning" />
                <span class="percentage">{{ memoryUsage }}%</span>
              </div>
            </div>

            <div class="resource-item">
              <div class="resource-label">
                <Icon type="ios-folder" />
                存储空间
              </div>
              <div class="resource-value">
                <Progress :percent="storageUsage" :stroke-width="8" status="success" />
                <span class="percentage">{{ storageUsage }}%</span>
              </div>
            </div>

            <div class="resource-item">
              <div class="resource-label">
                <Icon type="ios-wifi" />
                网络状态
              </div>
              <div class="resource-value">
                <Tag :color="networkStatus ? 'success' : 'error'">
                  <Icon :type="networkStatus ? 'ios-wifi' : 'ios-wifi-off'" />
                  {{ networkStatus ? '正常' : '异常' }}
                </Tag>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- 系统提示 -->
    <Alert type="info" show-icon class="system-alert">
      <template #title>
        <Icon type="ios-information-circle" />
        系统提示
      </template>
      <div class="alert-content">
        <p><strong>服务依赖：</strong>确保Python后端服务正在运行，否则API调用将失败。</p>
        <p><strong>模型加载：</strong>GNN模型在首次检测时加载，可能需要一些时间。</p>
        <p><strong>数据存储：</strong>用户数据存储在SQLite数据库中，历史记录保存在浏览器本地存储。</p>
        <p><strong>性能优化：</strong>系统针对Solidity智能合约安全检测进行了专门优化。</p>
      </div>
    </Alert>
  </div>
</template>

<script>
import { Card, Icon, Tag, Button, Progress, Alert } from 'view-ui-plus'

export default {
  name: 'SystemInfo',
  components: {
    Card,
    Icon,
    Tag,
    Button,
    Progress,
    Alert
  },
  data() {
    return {
      apiStatus: null,
      modelStatus: true, // 模拟模型状态
      checking: false,
      lastCheckTime: '未检查',
      cpuUsage: 25,
      memoryUsage: 45,
      storageUsage: 30,
      networkStatus: true
    }
  },
  mounted() {
    this.checkAPI()
    this.updateResourceUsage()
  },
  methods: {
    async checkAPI() {
      this.checking = true
      try {
        const response = await fetch('http://127.0.0.1:8000/')
        this.apiStatus = response.ok
      } catch {
        this.apiStatus = false
      }
      this.lastCheckTime = new Date().toLocaleTimeString('zh-CN')
      this.checking = false
    },

    updateResourceUsage() {
      // 模拟资源使用情况更新
      setInterval(() => {
        this.cpuUsage = Math.floor(Math.random() * 30) + 10
        this.memoryUsage = Math.floor(Math.random() * 40) + 30
        this.storageUsage = Math.floor(Math.random() * 20) + 25
        this.networkStatus = Math.random() > 0.1 // 90%正常
      }, 5000)
    }
  }
}
</script>

<style scoped>
.system-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.system-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.info-card, .status-card, .resource-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.card-header-custom {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 24px 24px 16px;
}

.header-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.frontend-card .header-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.backend-card .header-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.status-card .header-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.resource-card .header-icon {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.header-text h3 {
  margin: 0 0 4px;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.header-text p {
  margin: 0;
  font-size: 14px;
  color: #7f8c8d;
}

.info-content, .status-content, .resource-content {
  padding: 0 24px 24px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.info-value {
  flex-shrink: 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 12px;
  border-left: 4px solid #27ae60;
}

.status-info {
  flex: 1;
}

.status-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.status-url {
  font-size: 12px;
  color: #7f8c8d;
}

.status-url code {
  background: #e9ecef;
  border-radius: 4px;
  padding: 2px 6px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
}

.status-indicator {
  flex-shrink: 0;
}

.status-actions {
  text-align: center;
  margin: 20px 0;
}

.status-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  font-size: 12px;
  color: #7f8c8d;
}

.last-check, .uptime {
  display: flex;
  align-items: center;
  gap: 6px;
}

.resource-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.resource-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.resource-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #2c3e50;
  font-size: 14px;
}

.resource-value {
  display: flex;
  align-items: center;
  gap: 12px;
}

.percentage {
  font-weight: 600;
  color: #2c3e50;
  min-width: 40px;
}

.system-alert {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.alert-content {
  margin-top: 12px;
}

.alert-content p {
  margin: 8px 0;
  color: #5a6c7d;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .system-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .system-container {
    padding: 15px;
  }

  .card-header-custom {
    padding: 20px 20px 12px;
  }

  .info-content, .status-content, .resource-content {
    padding: 0 20px 20px;
  }

  .status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .status-footer {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  .resource-value {
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
  }

  .alert-content p {
    font-size: 14px;
  }
}

/* 自定义进度条样式 */
:deep(.ivu-progress-bg) {
  border-radius: 4px;
}

:deep(.ivu-progress-outer) {
  background: #e9ecef;
}

/* 状态卡片特殊样式 */
.status-card {
  grid-column: 1 / -1;
}

.resource-card {
  grid-column: 1 / -1;
}

/* 动画效果 */
.info-item, .status-item {
  transition: all 0.3s ease;
}

.info-item:hover, .status-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>