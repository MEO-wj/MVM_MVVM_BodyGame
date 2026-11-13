请使用 Python 编写一个最简单的键盘控制 Dino 游戏，使用MVP架构

## 基本要求

只生成四个 Python 文件：`main.py`、`model.py`、`view.py`、`presenter.py`，分别给出完整代码和简短的运行方法。

只依赖 Python 标准库和 PySide6。不使用图片素材、网络资源或其他本地模块。不使用、PyTorch、pygame、线程、抽象基类、配置系统或额外功能。用小矩形拼出像素恐龙（头、眼睛、身体、尾巴和腿）、仙人掌和飞鸟；恐龙有站立和下蹲外形，可以用分数交替实现简单的抬脚和扇翅效果。绘图全部放在 View，图形缩放到 Model 给出的矩形内，碰撞仍使用外接矩形。代码添加必要的中文注释。

实现以下基本游戏逻辑：
1. 空格或 ↑ 跳跃；持续按住不会自动连跳，空中不能二次起跳。
2. 按住 ↓ 下蹲，松开恢复站立；下蹲时不能跳跃，空中不改变碰撞高度。
3. 地面障碍碰到恐龙时结束，跳跃可以躲过。
4. 空中障碍会碰到站立恐龙，下蹲可以躲过。
5. R 重置全部游戏状态，游戏结束后也可以重开。

## 入口

`main.py` 的核心必须保留以下结构，补上所需 import 即可：

```python
def main():
    app = QApplication(sys.argv)

    model = GameModel()
    view = MainView()
    presenter = Presenter(model, view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

## MVP 架构与接口定义

### model.py

定义 `GameModel`，只保存游戏状态和实现规则，不导入 PySide6、View 或 Presenter。

提供以下方法：

- `reset()`：重置位置、速度、分数、障碍和结束状态。
- `jump()`：只在游戏未结束、恐龙落地且没有下蹲时起跳。
- `set_duck(enabled)`：设置下蹲状态。
- `update()`：推进一帧，处理重力、障碍、计分与碰撞。游戏结束后不再推进。
- `snapshot()`：返回纯数据字典供 View 绘制，包含 `width`、`height`、`ground`、`dino`、`obstacles`、`score`、`over`。矩形统一为 `(x, y, width, height)`，返回的障碍列表不可共享 Model 内部的可变列表。

采用每帧固定移动量的简单实现，不要求真实时间积分。横向固定恐龙位置，让障碍从右往左移动；适当保留障碍间距。地面障碍能跳过，空中障碍能通过下蹲躲避。

### view.py

定义继承 `QWidget` 的 `MainView`。只负责显示游戏数据字典及检测键盘输入，不导入 Model 或 Presenter，不调用任何 Model 方法。

主窗口继承 QMainWindow ，游戏的主画面单独创建一个 GameWidget 类继承 QWidget ，装入主窗口中。游戏窗口分辨率为800 x 260。


### presenter.py

定义继承 `QObject` 的 `Presenter`，使用 main 传入的对象 Model 和 View 。通过`on_key`函数传入 view 检测到的键盘事件调用对应的 model 事件。另外，presenter 需要实现游循环或定时器，用来控制游戏流程。游戏以30帧每秒的刷新率运行。


**所有文件都不要使用 PySide6 的 Signal、Slot、`.connect()` 或 `.emit()`，也不要使用 QTimer。**计时器用上述 `startTimer` / `timerEvent`。

请先简述四个文件的职责，再输出代码。以最简洁的方式输出代码，不要为了扩展性引入额外框架或复杂设计模式。