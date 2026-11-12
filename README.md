# MVM_MVVM_BodyGame

> ISI3003A Python 开发实训 2026 秋季课程项目
> 基于 MVP/MVVM 架构的体感小游戏，支持在不改动核心框架的前提下替换前端或后端。

## 项目简介

（待补充：一段话说明游戏玩法——如摄像头手势/姿态识别驱动的交互小游戏）

## 技术栈

| 分类 | 选型 | 说明 |
|------|------|------|
| 架构 | MVP / MVVM | 前后端解耦，接口契约层 `contracts.py` 为全项目核心 |
| 语言 | Python 3.10+ | 主要开发语言（课程要求后端必须 Python） |
| 前端 | （待定：PySide6 / Pygame） | 界面渲染与事件采集 |
| 后端 | （待定：MediaPipe / OpenCV） | 体感识别算法 |
| 测试 | pytest | Model / Presenter 层单元测试 |
| 环境 | uv（或 pip + requirements.txt） | 按课程提交要求锁定依赖清单 |

## 目录结构

```
2026课程项目_工作区/
├── code/        # 项目源代码（MVP 分层：contracts / core / view / presenter）
├── docs/        # 课程要求 PDF、开发文档
├── figures/     # 报告用图：架构图、运行截图
└── report/      # LaTeX 技术报告（XeLaTeX 编译）
```

## 快速开始

```bash
cd code
# 环境初始化（待补充：uv sync 或 pip install -r requirements.txt）
# 运行（待补充：python main.py）
```

## 开发进度

- [x] 建立工作区（code / docs / figures / report）
- [x] 报告 LaTeX 模板（XeLaTeX 可编译）
- [x] 开发文档（需求解读、架构原理、实现步骤）
- [ ] 确定选题与契约层 contracts.py
- [ ] Model 层实现与单元测试
- [ ] Presenter 层实现与 mock 测试
- [ ] View 层实现
- [ ] 前端/后端替换扩展（评分关键）
- [ ] 技术报告撰写、演示视频录制

## 小组成员

| 成员 | 分工 |
|------|------|
| 陈子俊（2024612033） | （待填写） |
| （待填写） | （待填写） |
