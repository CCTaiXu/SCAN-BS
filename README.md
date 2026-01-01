# Solidity 智能合约漏洞检测系统

基于图神经网络 (GNN) 的智能合约安全漏洞检测系统。本项目利用深度学习技术，通过分析 Solidity 代码的控制流图 (CFG) 来识别潜在的安全漏洞（如重入攻击、时间戳依赖等）。系统包含完整的 FastAPI 后端和 Vue.js 前端界面。

## 📚 项目背景

本项目基于以下研究工作实现：
> Zhuang, Yuan, et al. "Smart Contract Vulnerability Detection using Graph Neural Network." IJCAI. 2020.

核心 GNN 模型代码参考自: [GNNSCVulDetector](https://github.com/Messi-Q/GNNSCVulDetector)

## 🛠️ 环境要求

为了确保系统正常运行，请严格遵守以下环境要求：

- **操作系统**: Windows / Linux / macOS
- **Python**: **3.7** (必须，因为 TensorFlow 1.14.0 仅支持 Python 3.7 及以下)
- **Node.js**: 14+ (推荐 16 LTS)
- **Java**: JDK 8+ (用于解析 Solidity 代码生成图结构)

## ⚡ 快速开始

### 1. 环境安装

#### 后端 (Backend)

建议使用虚拟环境以避免依赖冲突。

```bash
# 1. 创建虚拟环境 (Python 3.7)
python -m venv .venv

# 2. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. 安装依赖
pip install -r backend/requirements.txt
```

#### 前端 (Frontend)

```bash
cd frontend/web
npm install
```

### 2. 模型训练 (可选)

如果需要重新训练模型，请执行以下步骤。项目中已包含预训练模型，可直接跳过此步。

```bash
# 确保在根目录下且已激活虚拟环境
cd gnn_core
python BasicModel.py
```
训练完成后，模型将保存至 `gnn_core/saved_models/`。

### 3. 启动系统

#### 启动后端服务

```bash
# 在项目根目录下
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
后端服务将在 `http://localhost:8000` 启动。

#### 启动前端界面

```bash
# 打开新的终端窗口
cd frontend/web
npm run serve
```
前端服务通常会在 `http://localhost:8080` 或 `http://localhost:8081` 启动 (取决于端口占用情况，请查看终端输出)。

## 📖 使用指南

1. **访问系统**: 打开浏览器访问前端地址。
2. **用户登录**: 点击左侧 "用户登录"。
   - 如果是首次使用，系统会自动处理或使用默认测试账号（视具体配置而定）。
   - 登录成功后获取 Token，用于后续检测请求。
3. **漏洞检测**:
   - 进入 "漏洞检测" 页面。
   - 在代码编辑框中粘贴 Solidity 智能合约代码。
   - 点击 "开始检测"。
4. **查看结果**:
   - 系统将显示检测结果（安全/存在漏洞）。
   - 显示漏洞类型（如 Reentrancy）。
   - 显示模型置信度 (Confidence)。

## 📂 项目结构

```
.
├── backend/                # Python 后端 (FastAPI)
│   ├── app/
│   │   ├── main.py         # API 入口
│   │   ├── inference.py    # 模型推理逻辑
│   │   ├── preprocess.py   # 数据预处理
│   │   └── ...
│   └── requirements.txt    # 后端依赖
├── frontend/               # Vue.js 前端
│   └── web/
│       ├── src/            # 源代码
│       └── package.json    # 前端依赖
├── gnn_core/               # GNN 模型核心代码
│   ├── BasicModel.py       # 模型定义与训练脚本
│   ├── tools/              # 图提取与特征处理工具
│   └── data/               # 训练数据集
└── README.md               # 项目说明文档
```

## 🔧 常见问题

- **检测结果置信度为 0?**
  - 请确保后端代码已更新，正确计算并返回 `confidence` 字段。
- **报错 "KeyError: ['NULL']"?**
  - 这是由于数据预处理时的格式问题，请确保 `preprocess.py` 中正确处理了列表转字符串的逻辑。
- **无法检测到漏洞?**
  - 检查 Solidity 代码语法是否标准。
  - 可以在 `backend/app/inference.py` 中调整检测阈值 (Threshold)。

## 📝 许可证

MIT License
