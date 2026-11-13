"""接口契约层（全项目"宪法"）——待实现。

依赖方向约定：view.py / presenter.py / recognition/ / alt/ 只允许从本文件导入
接口；具体实现之间禁止互相引用。

计划接口（先经小组评审定稿，再实现各层）：

- IGameView：前端接口（任何界面都要实现）
    update(snapshot)    # 渲染 Model.snapshot() 返回的数据
    show_over(score)    # 游戏结束提示
    on_key(handler)     # 事件订阅点：键盘/手势输入统一上报
- IGestureSource：后端手势输入接口（任何识别引擎都要实现）
    start(handler)      # 开始识别，每次识别结果回调 handler(action)
    stop()              # 停止识别

action 约定 ∈ {"jump", "duck", None}。

替换规则：
- 换前端 = 换 IGameView 实现（view.py ↔ alt/cli_view.py）
- 换后端 = 换 IGestureSource 实现（recognition/cnn_source.py ↔ alt/mp_source.py）
- model.py / presenter.py / contracts.py 全程不改，只改 main.py 组装处。
"""
