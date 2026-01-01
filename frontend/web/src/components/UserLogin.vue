<template>
  <div class="login-wrapper">
    <div class="login-background">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <div class="login-container">
      <div class="login-card-wrapper">
        <Card class="login-card" shadow>
          <template #title>
            <div class="login-header">
              <div class="logo-container">
                <div class="logo-icon">
                  <Icon type="ios-shield" size="32" />
                </div>
                <div class="logo-text">
                  <h2>Solidity 漏洞检测</h2>
                  <p>智能合约安全分析平台</p>
                </div>
              </div>
            </div>
          </template>

          <div class="login-body">
            <!-- 消息提示 -->
            <div v-if="message" class="message-container">
              <Alert :type="messageType" show-icon>
                {{ message }}
                <template #close>
                  <Icon type="ios-close" @click="message = null" />
                </template>
              </Alert>
            </div>

            <!-- 登录表单 -->
            <Form :model="form" :rules="rules" ref="form" @submit="login" v-if="!showRegister">
              <div class="form-section">
                <h3 class="form-title">
                  <Icon type="ios-log-in" />
                  用户登录
                </h3>

                <FormItem label="用户名" prop="username" class="form-item">
                  <Input
                    v-model="form.username"
                    placeholder="请输入用户名"
                    size="large"
                    clearable
                    @on-enter="login"
                  >
                    <template #prepend>
                      <Icon type="ios-person" />
                    </template>
                  </Input>
                </FormItem>

                <FormItem label="密码" prop="password" class="form-item">
                  <Input
                    v-model="form.password"
                    type="password"
                    placeholder="请输入密码"
                    size="large"
                    clearable
                    @on-enter="login"
                  >
                    <template #prepend>
                      <Icon type="ios-lock" />
                    </template>
                  </Input>
                </FormItem>

                <FormItem class="form-item">
                  <Button
                    type="primary"
                    size="large"
                    long
                    :loading="loading"
                    @click="login"
                    class="login-btn"
                  >
                    <Icon type="ios-log-in" />
                    {{ loading ? '登录中...' : '登录' }}
                  </Button>
                </FormItem>
              </div>
            </Form>

            <!-- 注册表单 -->
            <Form v-if="showRegister" :model="regForm" :rules="regRules" ref="regForm" @submit="register">
              <div class="form-section">
                <h3 class="form-title">
                  <Icon type="ios-person-add" />
                  注册账号
                </h3>

                <FormItem label="用户名" prop="username" class="form-item">
                  <Input
                    v-model="regForm.username"
                    placeholder="请输入用户名"
                    size="large"
                    clearable
                  >
                    <template #prepend>
                      <Icon type="ios-person" />
                    </template>
                  </Input>
                </FormItem>

                <FormItem label="密码" prop="password" class="form-item">
                  <Input
                    v-model="regForm.password"
                    type="password"
                    placeholder="请输入密码（至少6位）"
                    size="large"
                    clearable
                  >
                    <template #prepend>
                      <Icon type="ios-lock" />
                    </template>
                  </Input>
                </FormItem>

                <FormItem class="form-item">
                  <Button
                    type="success"
                    size="large"
                    long
                    :loading="loading"
                    @click="register"
                    class="register-btn"
                  >
                    <Icon type="ios-person-add" />
                    {{ loading ? '注册中...' : '注册' }}
                  </Button>
                </FormItem>
              </div>
            </Form>

            <!-- 切换按钮 -->
            <div class="switch-container">
              <Divider>
                <span class="divider-text">{{ showRegister ? '已有账号？' : '还没有账号？' }}</span>
              </Divider>
              <Button
                type="text"
                @click="showRegister = !showRegister"
                class="switch-btn"
              >
                {{ showRegister ? '返回登录' : '立即注册' }}
              </Button>
            </div>

            <!-- 底部信息 -->
            <div class="footer-info">
              <p>
                <Icon type="ios-information-circle-outline" />
                基于GNN的智能合约漏洞检测系统
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script>
import { Card, Form, FormItem, Input, Button, Icon, Divider, Alert } from 'view-ui-plus'

export default {
  name: 'UserLogin',
  components: {
    Card,
    Form,
    FormItem,
    Input,
    Button,
    Icon,
    Divider,
    Alert
  },
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      regForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码至少6位', trigger: 'blur' }
        ]
      },
      regRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码至少6位', trigger: 'blur' }
        ]
      },
      showRegister: false,
      loading: false,
      message: null,
      messageType: null
    }
  },
  methods: {
    async login() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          this.loading = true
          this.message = null
          try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                username: this.form.username,
                password: this.form.password
              })
            })
            if (response.ok) {
              const data = await response.json()
              localStorage.setItem('token', data.access_token)
              localStorage.setItem('username', this.form.username)
              this.showMessage('登录成功！', 'success')
              setTimeout(() => {
                this.$router.push('/dashboard')
              }, 1000)
            } else {
              const error = await response.json()
              this.showMessage(error.detail || '登录失败', 'error')
            }
          } catch (err) {
            this.showMessage('网络错误，请检查后端服务', 'error')
          }
          this.loading = false
        }
      })
    },
    async register() {
      this.$refs.regForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          this.message = null
          try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                username: this.regForm.username,
                password: this.regForm.password
              })
            })
            if (response.ok) {
              this.showMessage('注册成功，请登录', 'success')
              this.showRegister = false
              this.regForm = { username: '', password: '' }
            } else {
              const error = await response.json()
              this.showMessage(error.detail || '注册失败', 'error')
            }
          } catch (err) {
            this.showMessage('网络错误，请检查后端服务', 'error')
          }
          this.loading = false
        }
      })
    },
    showMessage(msg, type) {
      this.message = msg
      this.messageType = type
      setTimeout(() => {
        this.message = null
      }, 5000)
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: -1;
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 60px;
  height: 60px;
  top: 20%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.login-container {
  width: 100%;
  max-width: 480px;
  padding: 20px;
  z-index: 1;
}

.login-card-wrapper {
  animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.login-header {
  text-align: center;
  padding: 30px 20px 20px;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.logo-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.logo-text h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #7f8c8d;
  font-weight: 400;
}

.login-body {
  padding: 30px;
}

.message-container {
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-section {
  margin-bottom: 30px;
}

.form-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 25px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item :deep(.ivu-form-item-label) {
  font-weight: 500;
  color: #34495e;
}

.login-btn, .register-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

.register-btn {
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.2);
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(39, 174, 96, 0.3);
}

.switch-container {
  text-align: center;
  margin: 30px 0;
}

.divider-text {
  color: #7f8c8d;
  font-size: 14px;
}

.switch-btn {
  font-size: 14px;
  color: #667eea;
  font-weight: 500;
}

.switch-btn:hover {
  color: #764ba2;
}

.footer-info {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ecf0f1;
}

.footer-info p {
  margin: 0;
  font-size: 12px;
  color: #95a5a6;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: 15px;
  }

  .login-body {
    padding: 20px;
  }

  .logo-text h2 {
    font-size: 20px;
  }

  .form-title {
    font-size: 16px;
  }
}

/* 自定义滚动条 */
:deep(.ivu-card-body) {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

:deep(.ivu-card-body::-webkit-scrollbar) {
  width: 6px;
}

:deep(.ivu-card-body::-webkit-scrollbar-track) {
  background: #f7fafc;
  border-radius: 3px;
}

:deep(.ivu-card-body::-webkit-scrollbar-thumb) {
  background: #cbd5e0;
  border-radius: 3px;
}

:deep(.ivu-card-body::-webkit-scrollbar-thumb:hover) {
  background: #a0aec0;
}
</style>