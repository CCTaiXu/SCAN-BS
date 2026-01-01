<template>
  <div class="history-container">
    <Card class="history-card" shadow>
      <template #title>
        <div class="card-header-custom">
          <div class="header-icon">
            <Icon type="ios-time" size="24" />
          </div>
          <div class="header-text">
            <h3>检测历史记录</h3>
            <p>查看您之前的漏洞检测结果</p>
          </div>
        </div>
      </template>

      <div class="history-content">
        <!-- 空状态 -->
        <div v-if="history.length === 0" class="empty-state">
          <div class="empty-icon">
            <Icon type="ios-folder-open" size="64" />
          </div>
          <h4>暂无检测历史</h4>
          <p>您还没有进行过漏洞检测，开始您的第一次检测吧！</p>
          <Button type="primary" @click="$router.push('/detect')">
            <Icon type="ios-search" />
            开始检测
          </Button>
        </div>

        <!-- 历史记录列表 -->
        <div v-else class="history-list">
          <!-- 操作栏 -->
          <div class="action-bar">
            <div class="stats-info">
              <Icon type="ios-document" />
              共 {{ history.length }} 条记录
            </div>
            <Button type="error" size="small" @click="clearHistory">
              <Icon type="ios-trash" />
              清空历史
            </Button>
          </div>

          <!-- 历史记录项 -->
          <div class="history-items">
            <Card
              v-for="(item, index) in history"
              :key="index"
              class="history-item"
              shadow
            >
              <div class="history-header">
                <div class="history-meta">
                  <div class="history-time">
                    <Icon type="ios-calendar" />
                    {{ formatDate(item.timestamp) }}
                  </div>
                  <div class="history-duration">
                    <Icon type="ios-time" />
                    耗时: {{ item.result.processing_time ? item.result.processing_time.toFixed(2) + 's' : '未知' }}
                  </div>
                </div>
                <div class="history-status">
                  <Tag :color="getStatusColor(item.result)" size="large">
                    <Icon :type="getStatusIcon(item.result)" />
                    {{ getStatusText(item.result) }}
                  </Tag>
                </div>
              </div>

              <div class="history-body">
                <div class="history-grid">
                  <!-- 代码预览 -->
                  <div class="code-section">
                    <h5 class="section-title">
                      <Icon type="ios-code" />
                      代码片段
                    </h5>
                    <div class="code-preview">
                      <pre>{{ item.code.substring(0, 200) }}{{ item.code.length > 200 ? '...' : '' }}</pre>
                    </div>
                  </div>

                  <!-- 检测结果 -->
                  <div class="result-section">
                    <h5 class="section-title">
                      <Icon type="ios-analytics" />
                      检测结果
                    </h5>
                    <div class="result-content">
                      <div v-if="item.result.vulnerabilities && item.result.vulnerabilities.length > 0" class="vulnerabilities-list">
                        <div
                          v-for="(vuln, vIndex) in item.result.vulnerabilities.slice(0, 3)"
                          :key="vIndex"
                          class="vulnerability-item"
                        >
                          <Tag color="warning" size="small">
                            {{ vuln.type }}
                          </Tag>
                          <span class="vulnerability-desc">{{ vuln.description.substring(0, 40) }}{{ vuln.description.length > 40 ? '...' : '' }}</span>
                        </div>
                        <div v-if="item.result.vulnerabilities.length > 3" class="more-vulnerabilities">
                          <Icon type="ios-more" />
                          还有 {{ item.result.vulnerabilities.length - 3 }} 个漏洞...
                        </div>
                      </div>
                      <div v-else class="no-vulnerabilities">
                        <Icon type="ios-checkmark-circle" />
                        未发现漏洞
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 展开详情 -->
                <div class="detail-section">
                  <Collapse>
                    <Panel name="details">
                      查看完整详情
                      <template #content>
                        <div class="full-details">
                        <Tabs>
                          <TabPane label="完整代码" name="code">
                            <div class="code-block">
                              <pre>{{ item.code }}</pre>
                            </div>
                          </TabPane>
                          <TabPane label="检测结果" name="result">
                            <div class="result-block">
                              <pre>{{ JSON.stringify(item.result, null, 2) }}</pre>
                            </div>
                          </TabPane>
                        </Tabs>
                      </div>
                      </template>
                    </Panel>
                  </Collapse>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
import { Card, Icon, Button, Tag, Collapse, Panel, Tabs, TabPane } from 'view-ui-plus'

export default {
  name: 'DetectionHistory',
  components: {
    Card,
    Icon,
    Button,
    Tag,
    Collapse,
    Panel,
    Tabs,
    TabPane
  },
  data() {
    return {
      history: []
    }
  },
  mounted() {
    this.loadHistory()
  },
  methods: {
    loadHistory() {
      this.history = JSON.parse(localStorage.getItem('detectionHistory') || '[]')
    },
    clearHistory() {
      this.$Modal.confirm({
        title: '确认清空',
        content: '确定要清空所有历史记录吗？此操作不可恢复。',
        onOk: () => {
          localStorage.removeItem('detectionHistory')
          this.history = []
        }
      })
    },
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    },
    getStatusColor(result) {
      const count = result.vulnerabilities ? result.vulnerabilities.length : 0
      if (count === 0) return 'success'
      if (count <= 2) return 'warning'
      return 'error'
    },
    getStatusIcon(result) {
      const count = result.vulnerabilities ? result.vulnerabilities.length : 0
      if (count === 0) return 'ios-checkmark-circle'
      if (count <= 2) return 'ios-warning'
      return 'ios-close-circle'
    },
    getStatusText(result) {
      const count = result.vulnerabilities ? result.vulnerabilities.length : 0
      if (count === 0) return '安全'
      return `${count} 个漏洞`
    }
  }
}
</script>

<style scoped>
.history-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.history-card {
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
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  flex-shrink: 0;
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

.history-content {
  padding: 0 24px 24px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  color: #cbd5e0;
  margin-bottom: 20px;
}

.empty-state h4 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.empty-state p {
  color: #7f8c8d;
  margin-bottom: 30px;
}

.history-list {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stats-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #5a6c7d;
  font-weight: 500;
}

.history-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-item {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.history-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.history-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-time, .history-duration {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #7f8c8d;
}

.history-status {
  flex-shrink: 0;
}

.history-body {
  padding: 20px;
}

.history-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 20px;
}

.code-section, .result-section {
  display: flex;
  flex-direction: column;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
}

.code-preview {
  flex: 1;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 12px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.4;
  max-height: 120px;
  overflow-y: auto;
}

.result-content {
  flex: 1;
}

.vulnerabilities-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.vulnerability-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.vulnerability-item:last-child {
  border-bottom: none;
}

.vulnerability-desc {
  font-size: 12px;
  color: #5a6c7d;
  flex: 1;
}

.more-vulnerabilities {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #7f8c8d;
  padding: 8px 0;
}

.no-vulnerabilities {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #27ae60;
  font-weight: 500;
  padding: 12px 0;
}

.detail-section {
  margin-top: 20px;
}

.full-details {
  margin-top: 16px;
}

.code-block, .result-block {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 16px;
  margin-top: 8px;
}

.code-block pre, .result-block pre {
  margin: 0;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.4;
  max-height: 300px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .history-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .history-container {
    padding: 15px;
  }

  .card-header-custom {
    padding: 20px 20px 12px;
  }

  .history-content {
    padding: 0 20px 20px;
  }

  .history-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .history-meta {
    flex-direction: row;
    gap: 16px;
  }

  .action-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .empty-state {
    padding: 60px 20px;
  }
}

/* 自定义滚动条 */
.code-preview::-webkit-scrollbar,
.code-block pre::-webkit-scrollbar,
.result-block pre::-webkit-scrollbar {
  width: 6px;
}

.code-preview::-webkit-scrollbar-track,
.code-block pre::-webkit-scrollbar-track,
.result-block pre::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.code-preview::-webkit-scrollbar-thumb,
.code-block pre::-webkit-scrollbar-thumb,
.result-block pre::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.code-preview::-webkit-scrollbar-thumb:hover,
.code-block pre::-webkit-scrollbar-thumb:hover,
.result-block pre::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>