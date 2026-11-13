"""组装入口（依赖注入）：全项目唯一知道具体类的地方——待实现。

结构（按 docs/prompt.md 骨架扩展）：

    def main():
        model = GameModel()
        view = MainView()           # 换前端：改为 alt.cli_view.CliView
        presenter = Presenter(model, view)
        source = CnnSource(...)     # 换后端：改为 alt.mp_source.MediaPipeSource
        ...

验收标准：替换前端/后端时，仅允许改动本文件。
"""
