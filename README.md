# 📡 5G 信号可视化看板

> **"Code with AI" 极客探索赛 - 海选赛作品**

一个基于 Streamlit 和 PyDeck 构建的交互式 5G 信号数据可视化看板，支持 2D/3D 地图展示、实时筛选和数据统计分析。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57.0-red.svg)
![PyDeck](https://img.shields.io/badge/PyDeck-0.9.2-green.svg)

## ✨ 功能特性

### 🟢 基础功能

- **📊 数据加载**：使用 pandas 读取 CSV 格式的 5G 信号样本数据
- **🗺️ 交互式地图**：基于 PyDeck 渲染的信号覆盖地图
  - 根据信号强度 (RSRP) 自动着色：
    - 🟢 绿色：信号优秀 (> -90 dBm)
    - 🟡 黄色：信号一般 (-90 ~ -110 dBm)
    - 🔴 红色：信号较差 (< -110 dBm)
  - 支持鼠标悬停查看详细信息
- **📈 数据统计图表**：
  - 各频段基站数量分布柱状图
  - 终端类型占比统计

### 🟡 进阶功能

- **🔍 侧边栏联动筛选**：
  - 频段下拉菜单筛选
  - RSRP 范围滑动条筛选
  - 终端类型筛选
  - 筛选条件实时同步更新地图和图表
- **🌐 3D 视觉体验**：
  - 一键切换 2D/3D 地图视图
  - 3D 模式下信号点以柱状形式展示
  - 柱子高度与下载速率成正比
- **📝 工程化规范**：
  - 完整的代码注释和文档字符串
  - 单元测试覆盖核心功能

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run app.py
```

应用将自动在浏览器中打开（默认地址：http://localhost:8501）

### 运行测试

```bash
python -m pytest test_app.py -v
```

## 📁 项目结构

```
.
├── app.py                 # 主应用程序
├── test_app.py           # 单元测试
├── requirements.txt      # 依赖列表
├── README.md            # 项目说明文档
├── AI_PROMPTS.md        # AI 交互日志
└── data/
    └── signal_samples.csv  # 5G 信号样本数据
```

## 📊 数据说明

数据集包含以下字段：

| 字段名 | 说明 | 示例 |
|--------|------|------|
| Latitude | 纬度 | 31.209143 |
| Longitude | 经度 | 121.482867 |
| CellID | 小区 ID | 1926 |
| Band | 频段 | n28, n41, n78 |
| RSRP_dBm | 信号强度 (dBm) | -94.94 |
| SINR_dB | 信噪比 (dB) | 5.44 |
| TerminalType | 终端类型 | Smartphone, CPE, IoT |
| Download_Mbps | 下载速率 (Mbps) | 138.21 |

## 🛠️ 技术栈

- **Streamlit**：Web 应用框架
- **PyDeck**：地理数据可视化
- **Pandas**：数据处理
- **NumPy**：数值计算
- **Pytest**：单元测试

## 📝 版本历史

### v1.0.0 (2025-05-08)

- ✅ 完成基础关卡：数据加载、2D 地图、统计图表
- ✅ 完成进阶关卡：侧边栏筛选、3D 地图、单元测试
- ✅ 完善项目文档和 AI 交互日志

## 📄 许可证

本项目为 "Code with AI" 比赛参赛作品。

---

**Made with ❤️ by AI Coding Agent**
