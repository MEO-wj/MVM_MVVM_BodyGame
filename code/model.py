"""Model 层：纯游戏逻辑——待实现。

不导入 PySide6、View、Presenter，可脱离界面独立运行与测试。
按 docs/prompt.md 实现：reset() / jump() / set_duck(enabled) / update() / snapshot()

snapshot() 返回纯数据字典（width / height / ground / dino / obstacles / score / over），
矩形统一为 (x, y, width, height)，障碍列表不得共享内部可变引用。
"""
