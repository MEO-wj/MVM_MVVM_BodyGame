"""CNN 手势识别源：实现 IGestureSource——待实现。

流水线：摄像头取帧 → 手部区域裁剪（参考 frontend/data_collection.py 的
hand_area）→ backend/segment.py 肤色分割 → backend/classifier.py 三分类
→ 映射为 {"jump", "duck", None} 事件回调上报。

模型文件 model.pth 由 backend/train.py 训练得到。
"""
