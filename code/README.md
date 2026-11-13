# code/ 目录说明

> 本项目：基于 MVP 架构的体感小游戏（摄像头手势识别控制 Dino 跳跃游戏）。
> `backend/`、`frontend/`、`docs/` 下的代码来自授课教师陈泰舟（Taizhou CHEN,
> 汕头大学）提供的教学示例（文件头部均保留原作者署名），是本项目的
> **参考实现与素材**；顶层 `contracts.py` / `model.py` / `view.py` /
> `presenter.py` / `main.py` 等为按 `docs/prompt.md` 搭建的 **MVP 正式框架**，
> 目前为待实现的骨架占位（文件内 docstring 已写明各自职责与实现要点）。

## 目录结构

```
code/
├── README.md                  # 本说明文件
│
│  ========== MVP 正式框架（按 docs/prompt.md 搭建，待实现）==========
├── contracts.py               # ★ 接口契约层（全项目"宪法"）
│                              #   IGameView 前端接口 + IGestureSource 后端接口
├── main.py                    # 唯一入口：组装 View + Presenter + Model（依赖注入）
│                              #   替换前端/后端时【只改这一个文件】
├── model.py                   # Model 层：纯游戏逻辑（不碰 Qt，可独立测试）
├── view.py                    # View 层：PySide6 被动视图（不含业务逻辑）
├── presenter.py               # Presenter 层：事件协调 + 30fps 游戏循环（纯 Python）
├── recognition/               # 后端手势识别实现包（实现 IGestureSource）
│   └── cnn_source.py          #   CNN 版：摄像头 → segment 分割 → classifier 三分类
├── alt/                       # ★ 替换扩展实现包（评分关键）
│   ├── cli_view.py            #   扩展A：命令行前端（实现 IGameView）
│   └── mp_source.py           #   扩展B：MediaPipe 识别后端（实现 IGestureSource）
├── tests/                     # pytest 单元测试（不启动 GUI）
│   └── test_model.py          #   Model 层游戏规则用例
│
│  ========== 老师教学示例（参考实现与素材）==========
├── backend/                   # 后端算法原型 → 重构进 recognition/cnn_source.py
│   ├── segment.py             #   手部肤色分割
│   ├── dataset.py             #   PyTorch 数据集加载
│   ├── classifier.py          #   CNN 网络结构
│   └── train.py               #   训练 / 测试入口（产出 model.pth）
├── frontend/                  # 前端参考 → 重构进 view.py（仅参考写法）
│   └── data_collection.py     #   PySide6 摄像头数据采集工具
└── docs/                      # 老师提供的文档资料
    └── prompt.md              #   MVP 恐龙游戏需求提示词（正式框架的架构依据）
```

## 一、架构与替换机制（评分核心）

依赖只能自上而下指向抽象接口，跨层禁止直连：

```
main.py（组装层，唯一知道具体类的地方）
   │ 依赖注入
   ├──────────────┐
   ▼              ▼
view.py        recognition/        ← 各自实现 contracts 中的接口
(IGameView)    (IGestureSource)
   │              │
   └──▶ presenter.py ◀──┘          ← 只依赖接口，30fps 驱动
                │
                ▼
            model.py                ← 纯游戏逻辑，谁都不知道它上面的存在
```

**替换规则**（替换时 contracts.py / model.py / presenter.py / 各实现文件一行不改）：

| 替换什么 | 改哪里 | 替换前 → 替换后 |
|----------|--------|-----------------|
| 前端（界面） | `main.py` 一行 | `view.MainView`（PySide6 窗口）→ `alt.cli_view.CliView`（命令行） |
| 后端（识别引擎） | `main.py` 一行 | `recognition.cnn_source.CnnSource`（CNN）→ `alt.mp_source.MediaPipeSource`（MediaPipe） |

Model（游戏逻辑）与 Presenter 全程不动——这正是"不改变代码框架的前提下，
替换前端或后端"的课程要求落点。

## 二、数据流（一条流水线讲清两层含义）

```
【识别流水线】
摄像头 ─▶ 手部区域裁剪 ─▶ segment.py 肤色分割 ─▶ classifier.py 三分类
（frontend/ 参考写法）  （backend/）              （backend/）
        └─▶ 映射为 action ∈ {"jump", "duck", None} ─▶ 上报 Presenter

【游戏事件流】
键盘/手势输入 ─▶ Presenter.on_key / 手势回调 ─▶ model.jump() / model.set_duck()
 Presenter.timerEvent(30fps) ─▶ model.update() ─▶ view.update(model.snapshot())
```

键盘输入与手势输入走同一个 Presenter 入口——输入源可换而游戏逻辑不变，
本身就是解耦的直接证据。

## 三、参考代码说明（backend/ 与 frontend/）

一条完整但**单体式（未按 MVP 分层）**的手势识别流水线示例，实现"摄像头采集 →
手部分割 → CNN 训练 → 识别 Fist / Palm Up / Palm Down 三种手势"。
它**不是** MVP 分层源码，定位如下：

| 参考文件 | 在本项目中的定位 |
|----------|------------------|
| `backend/segment.py`、`backend/classifier.py` | **后端算法原型**——包装为 `recognition/cnn_source.py` 的内部实现 |
| `backend/dataset.py`、`backend/train.py` | 训练工具——产出 `model.pth` 供 CNN 版识别源加载 |
| `frontend/data_collection.py` | **前端写法参考**——PySide6 界面 + OpenCV 摄像头 + 手部区域裁剪逻辑（`hand_area`），view 层按被动视图规范重写 |
| `docs/prompt.md` | **架构范本**——main/model/view/presenter 四文件职责与接口定义，正式框架的搭建依据 |

### backend/ 文件作用

| 文件 | 作用 |
|------|------|
| `segment.py` | 手部分割：光照归一化 → BGR 转 YCrCb → 按肤色范围 `(0,133,77)~(255,173,127)` 提取掩膜 → 开/闭运算去噪 → 只保留最大连通域，输出手部二值图；被 `dataset.py` 调用，也可单独运行预览 |
| `dataset.py` | PyTorch Dataset：递归扫描 `dataset/**/*.jpg`，用上级文件夹名（0/1/2）作为标签；`__getitem__` 中调用 `segment()` 生成掩膜，缩放到 128×128 并归一化为 float32 |
| `classifier.py` | `GestureClassifier` CNN：Conv(1→64, k7) → Conv(64→128, k3) ×2，各接 MaxPool；Flatten 后接 1024/2048 全连接，输出 3 类 logits；输入为 1×128×128 灰度掩膜 |
| `train.py` | 训练/测试入口：8:2 随机划分训练/验证集，Adam（lr=1e-4）+ CrossEntropyLoss 训练，默认 10 epoch，保存整个模型到 `model.pth`；`-test` 模式加载模型并在给定数据集上报告准确率 |

### frontend/ 文件作用

| 文件 | 作用 |
|------|------|
| `data_collection.py` | PySide6 采集工具：打开摄像头，画面右侧绿色框出手部区域；下拉框选标签（0=Fist，1=Plam Up，2=Plam Down），点击 Start Recording 或按 R 键后每 0.5 秒自动裁剪保存一张 JPG 到 `dataset/<标签序号>/` |

## 四、运行方法

### 4.1 训练识别模型（用老师的参考流水线）

依赖：Python 3.10+，`torch`、`opencv-python`、`numpy`、`PySide6`、`tqdm`

```bash
# 1. 采集数据（GUI 窗口，需摄像头）
python frontend/data_collection.py            # 数据保存到 ./dataset

# 2. 训练（产出 model.pth，供 recognition/cnn_source.py 加载）
python backend/train.py -data_path dataset

# 3. 测试
python backend/train.py -data_path dataset -model_path model.pth -test
```

> `backend/` 内部以平级模块互相导入，从任意位置运行均可；但数据路径是相对路径
> （`dataset/`、`model.pth`），采集与训练建议使用同一工作目录以共用数据。

### 4.2 运行游戏（框架实现完成后）

```bash
python main.py                                # 替换前：PySide6 + CNN
# 换前端：main.py 中 view = MainView() 改为 CliView()，再运行
# 换后端：main.py 中 source = CnnSource(...) 改为 MediaPipeSource()，再运行
```

## 五、参考代码已知问题（重构时需修复）

1. `data_collection.py`：`self.read_failures` 在 `update_frame` 中使用但未在
   `__init__` 中初始化，摄像头读取失败时会抛 `AttributeError`。
2. `data_collection.py`：标签拼写 `Plam Up / Plam Down` 应为 `Palm`（仅显示名，
   不影响训练，实际标签是文件夹序号 0/1/2）。
3. `train.py`：`-test` 模式加载模型时硬编码 `"model.pth"`，未使用 `-model_path` 参数。
4. `train.py`：`torch.save(model)` 保存了整个模型对象而非 `state_dict`，跨版本加载较脆弱。
5. 未分层：UI、摄像头、算法混在单文件中，正是本项目用 MVP 架构重构解决的点。

## 六、开发路线（对照 docs/prompt.md 与开发文档第 5 节）

- [ ] 定稿 `contracts.py`（IGameView / IGestureSource，契约先行，两人并行）
- [ ] 实现 `model.py` 游戏逻辑 + `tests/test_model.py` 单测全绿（不启动 GUI）
- [ ] 实现 `presenter.py`（键盘输入 + 30fps 循环）+ mock View 测试
- [ ] 实现 `view.py`（PySide6 被动视图，800×260）
- [ ] 实现 `recognition/cnn_source.py`（采集数据 → 训练 model.pth → 接入游戏）
- [ ] ★ 扩展A：`alt/cli_view.py` 命令行前端；★ 扩展B：`alt/mp_source.py` MediaPipe 后端
- [ ] 现场演示"只改 main.py 一行"切换前端/后端，录屏留证
- [ ] README 补齐依赖清单（requirements.txt / pyproject.toml）与部署说明
