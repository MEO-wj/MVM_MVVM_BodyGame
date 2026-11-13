"""Presenter 层：居中协调——待实现。

纯 Python，禁止导入 PySide6。持有 View / Model / 手势源引用（类型写为
contracts 中的接口，依赖注入）。

- on_key(event)：把键盘事件转成 model.jump() / model.set_duck() 调用
- 手势回调：IGestureSource 识别出的 action 同样转成上述 Model 调用
- startTimer/timerEvent 以 30fps 驱动游戏循环：
  model.update() → view.update(model.snapshot())
"""
