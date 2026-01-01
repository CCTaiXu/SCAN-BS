<template>
  <div class="guide-container">
    <Card class="guide-card" shadow>
      <template #title>
        <div class="card-header-custom">
          <div class="header-icon">
            <Icon type="ios-book" size="24" />
          </div>
          <div class="header-text">
            <h3>使用指南</h3>
            <p>了解如何使用Solidity漏洞检测系统</p>
          </div>
        </div>
      </template>

      <div class="guide-content">
        <Collapse accordion>
          <!-- 快速开始 -->
          <Panel name="getting-started">
            <div class="panel-header">
              <Icon type="ios-play" />
              快速开始
            </div>
            <template #content>
              <div class="panel-content">
              <div class="steps-list">
                <div class="step-item">
                  <div class="step-number">1</div>
                  <div class="step-content">
                    <h5>用户注册/登录</h5>
                    <p>点击登录页面，注册新账号或使用现有账号登录系统</p>
                  </div>
                </div>
                <div class="step-item">
                  <div class="step-number">2</div>
                  <div class="step-content">
                    <h5>进入检测页面</h5>
                    <p>登录成功后，通过侧边栏导航进入"漏洞检测"页面</p>
                  </div>
                </div>
                <div class="step-item">
                  <div class="step-number">3</div>
                  <div class="step-content">
                    <h5>输入代码</h5>
                    <p>在左侧代码输入框中粘贴或输入您的Solidity智能合约代码</p>
                  </div>
                </div>
                <div class="step-item">
                  <div class="step-number">4</div>
                  <div class="step-content">
                    <h5>开始检测</h5>
                    <p>点击"开始检测"按钮，系统将自动分析代码中的安全漏洞</p>
                  </div>
                </div>
                <div class="step-item">
                  <div class="step-number">5</div>
                  <div class="step-content">
                    <h5>查看结果</h5>
                    <p>在右侧查看详细的检测结果，包括发现的漏洞和安全建议</p>
                  </div>
                </div>
              </div>
            </div>
            </template>
          </Panel>

          <!-- 支持的漏洞类型 -->
          <Panel name="vulnerabilities">
            <div class="panel-header">
              <Icon type="ios-shield" />
              支持的漏洞类型
            </div>
            <template #content>
              <div class="panel-content">
              <div class="vulnerabilities-grid">
                <div class="vulnerability-category">
                  <h5 class="category-title">
                    <Icon type="ios-warning" />
                    常见漏洞类型
                  </h5>
                  <div class="vulnerability-list">
                    <div class="vulnerability-item">
                      <Tag color="error">重入攻击</Tag>
                      <span>合约在调用外部合约前未更新状态</span>
                    </div>
                    <div class="vulnerability-item">
                      <Tag color="warning">整数溢出</Tag>
                      <span>算术运算超出类型范围</span>
                    </div>
                    <div class="vulnerability-item">
                      <Tag color="warning">访问控制</Tag>
                      <span>权限检查不当或缺失</span>
                    </div>
                    <div class="vulnerability-item">
                      <Tag color="info">未初始化变量</Tag>
                      <span>使用未初始化的存储变量</span>
                    </div>
                    <div class="vulnerability-item">
                      <Tag color="error">拒绝服务</Tag>
                      <span>合约可能被恶意阻断</span>
                    </div>
                    <div class="vulnerability-item">
                      <Tag color="warning">时间依赖</Tag>
                      <span>依赖区块时间戳的逻辑漏洞</span>
                    </div>
                  </div>
                </div>

                <div class="detection-capabilities">
                  <h5 class="category-title">
                    <Icon type="ios-analytics" />
                    检测能力
                  </h5>
                  <div class="capability-list">
                    <div class="capability-item">
                      <Icon type="ios-checkmark-circle" />
                      <span>基于图神经网络的智能分析</span>
                    </div>
                    <div class="capability-item">
                      <Icon type="ios-checkmark-circle" />
                      <span>AST静态分析技术</span>
                    </div>
                    <div class="capability-item">
                      <Icon type="ios-checkmark-circle" />
                      <span>模式匹配检测算法</span>
                    </div>
                    <div class="capability-item">
                      <Icon type="ios-checkmark-circle" />
                      <span>置信度评分系统</span>
                    </div>
                    <div class="capability-item">
                      <Icon type="ios-checkmark-circle" />
                      <span>详细的位置信息</span>
                    </div>
                    <div class="capability-item">
                      <Icon type="ios-checkmark-circle" />
                      <span>修复建议生成</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </template>
          </Panel>

          <!-- API文档 -->
          <Panel name="api">
            <div class="panel-header">
              <Icon type="ios-code" />
              API 文档
            </div>
            <template #content>
              <div class="panel-content">
              <div class="api-info">
                <div class="api-server">
                  <h5>后端服务地址</h5>
                  <div class="server-url">
                    <code>http://127.0.0.1:8000</code>
                    <Button
                      type="primary"
                      size="small"
                      @click="openApiDocs"
                      style="margin-left: 12px;"
                    >
                      <Icon type="ios-link" />
                      打开API文档
                    </Button>
                  </div>
                </div>

                <div class="api-endpoints">
                  <h5>主要API端点</h5>
                  <div class="endpoint-list">
                    <div class="endpoint-item">
                      <Tag color="success">POST</Tag>
                      <code>/api/auth/register</code>
                      <span>用户注册</span>
                    </div>
                    <div class="endpoint-item">
                      <Tag color="success">POST</Tag>
                      <code>/api/auth/login</code>
                      <span>用户登录</span>
                    </div>
                    <div class="endpoint-item">
                      <Tag color="primary">POST</Tag>
                      <code>/api/detect</code>
                      <span>漏洞检测</span>
                    </div>
                    <div class="endpoint-item">
                      <Tag color="info">GET</Tag>
                      <code>/api/stats</code>
                      <span>获取统计信息</span>
                    </div>
                    <div class="endpoint-item">
                      <Tag color="info">GET</Tag>
                      <code>/api/health</code>
                      <span>服务健康检查</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </template>
          </Panel>

          <!-- 使用提示 -->
          <Panel name="tips">
            <div class="panel-header">
              <Icon type="ios-lightbulb" />
              使用提示
            </div>
            <template #content>
              <div class="panel-content">
              <Alert type="info" show-icon class="tips-alert">
                <template #title>
                  <Icon type="ios-information-circle" />
                  重要提示
                </template>
                <p>检测结果仅供参考，建议结合人工审核和专业安全工具进行全面的安全评估。</p>
              </Alert>

              <div class="tips-grid">
                <div class="tips-section">
                  <h5>代码要求</h5>
                  <ul>
                    <li>确保Solidity代码语法正确</li>
                    <li>支持完整的合约代码</li>
                    <li>包含必要的import语句</li>
                    <li>使用标准的Solidity版本</li>
                  </ul>
                </div>

                <div class="tips-section">
                  <h5>性能说明</h5>
                  <ul>
                    <li>检测过程可能需要几秒到几十秒</li>
                    <li>复杂合约检测时间较长</li>
                    <li>请耐心等待检测完成</li>
                    <li>避免频繁重复检测</li>
                  </ul>
                </div>

                <div class="tips-section">
                  <h5>数据存储</h5>
                  <ul>
                    <li>历史记录保存在浏览器本地存储中</li>
                    <li>清除浏览器数据将丢失历史记录</li>
                    <li>建议定期备份重要检测结果</li>
                    <li>不同浏览器间数据不共享</li>
                  </ul>
                </div>

                <div class="tips-section">
                  <h5>系统维护</h5>
                  <ul>
                    <li>定期检查后端服务状态</li>
                    <li>保持网络连接稳定</li>
                    <li>使用最新版本的浏览器</li>
                    <li>如遇问题请查看控制台错误信息</li>
                  </ul>
                </div>
              </div>
            </div>
            </template>
          </Panel>
        </Collapse>
      </div>
    </Card>
  </div>
</template>

<script>
import { Card, Icon, Collapse, Panel, Tag, Button, Alert } from 'view-ui-plus'

export default {
  name: 'UserGuide',
  components: {
    Card,
    Icon,
    Collapse,
    Panel,
    Tag,
    Button,
    Alert
  },
  methods: {
    openApiDocs() {
      window.open('http://127.0.0.1:8000/docs', '_blank')
    }
  }
}
</script>

<style scoped>
.guide-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.guide-card {
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

.guide-content {
  padding: 0 24px 24px;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.panel-content {
  margin-top: 16px;
  padding: 0 20px;
}

/* 快速开始步骤 */
.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h5 {
  margin: 0 0 8px;
  color: #2c3e50;
  font-size: 16px;
}

.step-content p {
  margin: 0;
  color: #5a6c7d;
  line-height: 1.5;
}

/* 漏洞类型网格 */
.vulnerabilities-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.vulnerability-category, .detection-capabilities {
  display: flex;
  flex-direction: column;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
}

.vulnerability-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vulnerability-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.vulnerability-item span {
  color: #5a6c7d;
  font-size: 14px;
  line-height: 1.4;
}

.capability-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.capability-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #27ae60;
  font-size: 14px;
}

/* API文档 */
.api-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.api-server h5, .api-endpoints h5 {
  margin: 0 0 12px;
  color: #2c3e50;
  font-size: 16px;
}

.server-url {
  display: flex;
  align-items: center;
  gap: 12px;
}

.server-url code {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 8px 12px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  color: #2c3e50;
}

.endpoint-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.endpoint-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.endpoint-item code {
  background: #e9ecef;
  border-radius: 4px;
  padding: 2px 6px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 12px;
  color: #2c3e50;
}

.endpoint-item span {
  color: #5a6c7d;
  font-size: 14px;
}

/* 使用提示 */
.tips-alert {
  margin-bottom: 24px;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.tips-section {
  display: flex;
  flex-direction: column;
}

.tips-section h5 {
  margin: 0 0 12px;
  color: #2c3e50;
  font-size: 15px;
  font-weight: 600;
}

.tips-section ul {
  margin: 0;
  padding-left: 20px;
}

.tips-section li {
  color: #5a6c7d;
  margin-bottom: 6px;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .vulnerabilities-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .tips-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .guide-container {
    padding: 15px;
  }

  .card-header-custom {
    padding: 20px 20px 12px;
  }

  .guide-content {
    padding: 0 20px 20px;
  }

  .step-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }

  .step-number {
    align-self: center;
  }

  .vulnerabilities-grid {
    gap: 20px;
  }

  .endpoint-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .server-url {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .server-url code {
    word-break: break-all;
  }
}

/* 自定义滚动条 */
:deep(.ivu-collapse-item) {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
}

:deep(.ivu-collapse-header) {
  background: #f8f9fa;
  border: none;
  padding: 16px 20px;
}

:deep(.ivu-collapse-content) {
  border-top: 1px solid #e9ecef;
  background: white;
}
</style>