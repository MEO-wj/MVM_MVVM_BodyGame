"""扩展 B：MediaPipe 手势识别后端，实现 IGestureSource——待实现。

用 MediaPipe Hands（或表情/姿态识别）替换 CNN 流水线，识别结果同样映射为
{"jump", "duck", None} 回调上报。
接入方式：main.py 中把 source = CnnSource(...) 换成本实现，
recognition/ 与其余各层均不改。
"""
