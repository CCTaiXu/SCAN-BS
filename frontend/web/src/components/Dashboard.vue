<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h1 class="page-title">
        <Icon type="ios-home" />
        主页
      </h1>
      <div class="page-subtitle">欢迎使用 Solidity 漏洞检测系统</div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <Card class="stat-card processing-card">
        <div class="stat-content">
          <div class="stat-icon">
            <Icon type="ios-timer" size="32" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.processingContracts }}</div>
            <div class="stat-label">正在检测合约</div>
          </div>
        </div>
      </Card>

      <Card class="stat-card total-size-card">
        <div class="stat-content">
          <div class="stat-icon">
            <Icon type="ios-stats" size="32" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ formatFileSize(stats.totalSize) }}</div>
            <div class="stat-label">合约总大小</div>
          </div>
        </div>
      </Card>

      <Card class="stat-card total-count-card">
        <div class="stat-content">
          <div class="stat-icon">
            <Icon type="ios-document" size="32" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalContracts }}</div>
            <div class="stat-label">合约总数</div>
          </div>
        </div>
      </Card>

      <Card class="stat-card vulnerabilities-card">
        <div class="stat-content">
          <div class="stat-icon">
            <Icon type="ios-warning" size="32" />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalVulnerabilities }}</div>
            <div class="stat-label">发现漏洞</div>
          </div>
        </div>
      </Card>
    </div>

    <!-- 最新合约列表 -->
    <Card class="recent-contracts-card">
      <div class="card-header">
        <h3>
          <Icon type="ios-time" />
          最新合约
        </h3>
        <Button type="primary" size="small" @click="$router.push('/history')">
          查看全部
          <Icon type="ios-arrow-forward" />
        </Button>
      </div>

      <div class="contracts-list">
        <div
          v-for="contract in recentContracts"
          :key="contract.id"
          class="contract-item"
        >
          <div class="contract-info">
            <div class="contract-name">{{ contract.name }}</div>
            <div class="contract-meta">
              <span class="contract-size">{{ formatFileSize(contract.size) }}</span>
              <span class="contract-time">{{ formatTime(contract.timestamp) }}</span>
            </div>
          </div>
          <div class="contract-status">
            <Tag
              :color="getStatusColor(contract.status)"
              size="small"
            >
              {{ getStatusText(contract.status) }}
            </Tag>
          </div>
        </div>

        <div v-if="recentContracts.length === 0" class="empty-state">
          <Icon type="ios-document-outline" size="48" />
          <p>暂无检测记录</p>
          <Button type="primary" @click="$router.push('/detect')">
            开始检测
          </Button>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { Card, Tag, Button, Icon } from 'view-ui-plus'

export default {
  name: 'DashboardPage',
  components: {
    Card,
    Tag,
    Button,
    Icon
  },
  data() {
    return {
      stats: {
        processingContracts: 0,
        totalSize: 0,
        totalContracts: 0,
        totalVulnerabilities: 0
      },
      recentContracts: []
    }
  },
  mounted() {
    this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        // 获取统计数据
        const statsResponse = await fetch('http://127.0.0.1:8000/api/stats', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })

        if (statsResponse.ok) {
          const statsData = await statsResponse.json()
          this.stats = {
            processingContracts: statsData.processing_contracts || 0,
            totalSize: statsData.total_size || 0,
            totalContracts: statsData.total_contracts || 0,
            totalVulnerabilities: statsData.total_vulnerabilities || 0
          }
        }

        // 获取最近合约
        const history = JSON.parse(localStorage.getItem('detectionHistory') || '[]')
        this.recentContracts = history.slice(0, 10).map((item, index) => ({
          id: index,
          name: item.name || '未命名合约',
          size: item.code ? item.code.length : 0,
          timestamp: item.timestamp,
          status: item.result && item.result.vulnerabilities ? 'completed' : 'processing'
        }))

      } catch (error) {
        console.error('加载仪表板数据失败:', error)
        // 使用模拟数据
        this.stats = {
          processingContracts: 2,
          totalSize: 15432,
          totalContracts: 15,
          totalVulnerabilities: 8
        }
        this.recentContracts = [
          {
            id: 1,
            name: 'TokenContract.sol',
            size: 2048,
            timestamp: Date.now() - 3600000,
            status: 'completed'
          },
          {
            id: 2,
            name: 'DEXContract.sol',
            size: 5120,
            timestamp: Date.now() - 7200000,
            status: 'processing'
          }
        ]
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
    },

    formatTime(timestamp) {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      return date.toLocaleDateString()
    },

    getStatusColor(status) {
      switch (status) {
        case 'completed': return 'success'
        case 'processing': return 'warning'
        case 'failed': return 'error'
        default: return 'default'
      }
    },

    getStatusText(status) {
      switch (status) {
        case 'completed': return '检测完成'
        case 'processing': return '检测中'
        case 'failed': return '检测失败'
        default: return '未知状态'
      }
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.page-title .ivu-icon {
  color: #667eea;
}

.page-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: none;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.processing-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.total-size-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.total-count-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.vulnerabilities-card {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  opacity: 0.9;
}

.stat-info {
  flex: 1;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.recent-contracts-card {
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
  margin-bottom: 16px;
}

.card-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.contracts-list {
  max-height: 400px;
  overflow-y: auto;
}

.contract-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f1f1f1;
  transition: background-color 0.2s ease;
}

.contract-item:hover {
  background-color: #f8f9fa;
}

.contract-item:last-child {
  border-bottom: none;
}

.contract-info {
  flex: 1;
}

.contract-name {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.contract-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #7f8c8d;
}

.contract-status {
  flex-shrink: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  color: #7f8c8d;
}

.empty-state .ivu-icon {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-page {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .stat-content {
    padding: 16px;
  }

  .stat-value {
    font-size: 28px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .contract-meta {
    flex-direction: column;
    gap: 4px;
  }
}

/* 自定义滚动条 */
.contracts-list::-webkit-scrollbar {
  width: 6px;
}

.contracts-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.contracts-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.contracts-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>