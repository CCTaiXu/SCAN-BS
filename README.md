# SCAN-BS: 智能合约漏洞检测系统 (GNN-SCVulScan)

[![Python Support](https://img.shields.io/badge/Python-3.7-blue.svg)](https://www.python.org/downloads/release/python-3712/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-1.14.0-orange)](https://www.tensorflow.org/)
[![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

基于图神经网络 (GNN) 的智能合约安全漏洞检测系统。本项目利用深度学习技术，通过自动化提取 Solidity 代码的图结构特征，识别 **重入攻击 (Reentrancy)**、**时间戳依赖 (Timestamp Dependence)** 及 **整数溢出 (Integer Overflow)** 等关键安全漏洞。系统集成了可视化前端、FastAPI 后端以及完整的模型训练与特征提取流水线。

## 📚 项目背景

本项目基于以下前沿研究进行扩展及工程化实现：
> Zhuang, Yuan, et al. "Smart Contract Vulnerability Detection using Graph Neural Network." IJCAI. 2020.

## 🌟 核心功能

*   **多漏洞模式检测**：支持重入攻击、时间戳依赖、整数溢出的高精准识别。
*   **双模式检测**：支持单文件实时在线审计与批量 Solidity 源码上传扫描。
*   **可视化分析**：提供合约代码图结构的可视化展示（将代码转换为节点与交互关系的图谱）。
*   **全自动训练管线**：内置自动化工具集，一键完成代码去注释化 -> 片段构建 -> 特征提取 -> JSON 序列化 -> GNN 训练。
*   **交互友好**：现代化 Vue 3 驱动的前端界面，提供直观的代码高亮、在线分析以及实时报告。

## 🛠️ 环境依赖

由于模型对特定框架版本有严格兼容性要求，请务必遵循以下环境配置：

*   **Python**: `3.7.x` (强制要求，兼容 TensorFlow 1.1x)
*   **Node.js**: `v14+` / `v16+`
*   **TensorFlow**: `1.14.0`
*   **Solidity 编译器**: `solc` 对应的指定版本依赖

## ⚡ 快速安装与启动

### 方式一：一键启动 (Windows 推荐)

直接双击运行根目录下的 `start.bat` 脚本（首次运行可使用 `install.bat` 预先安装所需模块）。

该脚本会自动：
1. 检查对应的 Python 与 Node 运行环境。
2. 激活系统的 `.venv` 虚拟环境。
3. 后台启动 FastAPI 后端服务 (默认端口 `8000`)。
4. 启动 Vue 前端开发服务器 (默认端口 `8080` / `5173`)，并打印访问网址。

### 方式二：手动配置与启动

#### 1. 后端设置

```bash
# 1. 创建并激活 Python 3.7 虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate # Linux/Mac

# 2. 安装依赖包
pip install -r backend/requirements.txt
```

#### 2. 前端设置

```bash
cd frontend/web
npm install
```

#### 3. 运行服务

*   **启动后端**: `uvicorn backend.app.main:app --reload`
*   **启动前端**: 在 `frontend/web` 目录下执行 `npm run serve` (或 `npm run dev`)

## 🧠 模型开发与训练指南

如果您希望基于我们的 GNN 算法训练自定义的新型漏洞识别模型，可直接利用其自动化流水线。

### 1. 数据准备
将收集好的 Solidity 源码 (.sol) 分类放入指定的原始代码文件夹，例如：
* `gnn_core/data/reentrancy/source_code/`
* `gnn_core/data/timestamp/source_code/`
* `gnn_core/data/integeroverflow/source_code/`

### 2. 标签建立
在对应的特征工具目录下，确保定义了相关的合约名与漏洞标签映射：
*   映射列表：`gnn_core/features/[vulnerability_type]/contract_name_train.txt`
*   专家标签：`gnn_core/features/[vulnerability_type]/label_by_experts_train.txt` (仅需要 1 或 0)

### 3. 一键特征工程
系统将自动完成代码修剪、抽象语法树 (AST) 图转化到向量化的全过程：
```bash
python gnn_core/run_pipeline.py
```

### 4. 开启训练
生成的序列化数据集输入图神经网络进行深度特征匹配与泛化学习：
```bash
cd gnn_core
bash train.sh
# 或手动配置超参
python GNNSCModel.py --thresholds 0.5
```

## 📂 核心目录结构

```text
SCAN-BS/
├── backend/                # FastAPI 后端服务 (提供编译、检测及图生成 API)
│   ├── app/
│   │   ├── main.py         # 路由和接口注册
│   │   ├── preprocess.py   # 源码预处理与验证
│   │   └── inference.py    # GNN 推理调用封装
├── frontend/               # Vue 网页前端代码
├── gnn_core/               # 核心 GNN 模型及算法实现 (基于 TensorFlow 1.x)
│   ├── tmp_pipeline/       # 自动生成的代码中间件与图谱解析日志
│   ├── tools/              # 特征解析工具 (如 AST 到图结构)
│   ├── data/               # 原始和处理后得图数据存储区
│   └── saved_models/       # 预训练参数与模型持久化备份
└── start.bat / install.bat # Windows 快捷启动配置
```

## 🤝 贡献与开源许可

欢迎提交 Issue 和 Pull Request！
本项目使用 MIT License 开源，详见代码仓。
如有学术使用需求请务必引用原文或保留致谢声明。
│   ├── data/               # 原始数据集存放
│   ├── train_data/         # 训练用的 JSON 数据
│   ├── run_pipeline.py     # ✅ 自动化数据处理脚本
│   └── GNNSCModel.py       # 模型训练主程序
└── start.bat               # Windows 一键启动脚本
```

## ⚠️ 注意事项

*   **代码注释**: 为了提升图提取工具 `AutoExtractGraph` 的解析稳定性，我们引入了正则去注释机制。复杂的注释结构可能会影响特征提取。
*   **模型兼容性**: 由于使用 TensorFlow 1.x 的旧版 API，请务必保持 Python 版本为 3.7。

## 📜 版权信息

本项目代码遵循 MIT 协议开源。核心算法参考自 [GNNSCVulDetector](https://github.com/Messi-Q/GNNSCVulDetector)。
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
