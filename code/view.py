"""View 层：PySide6 被动视图——待实现。

只负责"画"与"上报输入"，不含业务逻辑；不导入 model.py / presenter.py。
- MainView(QMainWindow) + GameWidget(QWidget)，游戏窗口 800×260
- update(snapshot)：用小矩形绘制恐龙（站立/下蹲两态）、仙人掌、飞鸟、地面、分数
- 键盘与手势输入统一转发给 Presenter 处理
- 遵循 docs/prompt.md：不使用 Signal/Slot/QTimer，计时用 startTimer/timerEvent

写法参考（仅参考，不照抄）：frontend/data_collection.py 的 PySide6 + OpenCV 用法。
"""
