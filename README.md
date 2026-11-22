# 蓝白圣诞树 · 手势控制版

把原始 Pygame（`tree.py`）的 3D 粒子圣诞树搬到浏览器里，用 WebGL 单文件实现；配色改成天蓝→白柔和过渡，并加了摄像头手势控制。

在线体验：https://hhk12312.github.io/christmas-tree/

## 玩法

- 鼠标：拖动旋转（带惯性）、滚轮缩放、点击树身散开／聚合
- 底部按钮：「粒子散开」「暂停旋转」「手势模式」「加照片」「隐藏按钮」
- 界面隐藏（截图／录屏用）：
  - 鼠标静止约 4 秒，底部按钮自动淡出；动一下鼠标就回来
  - 点「隐藏按钮」或按 **H** 彻底隐藏（含手势模式的摄像头小窗），再按 H 或点右下角小圆点恢复
- 照片：
  - 点「加照片」可一次选多张（也可以直接把图片拖进画面）
  - 照片会像挂饰一样贴在树身上，沿圆锥面分布，**淡入**出现；最多 24 张
  - 转到背面时会逐渐透明直到看不见，转回正面再慢慢显出来；粒子散开时照片跟着飘到树周围围成一圈，一起旋转
  - 缩略图存在浏览器本地（IndexedDB），刷新页面还在；「清空照片」一键删掉
- 手势（需要摄像头）：
  - 五指张开 → 粒子散开
  - 握拳 → 回到合拢态
  - 保持张开并左右转手 → 相机跟着旋转（识别 15 帧/秒，画面 60 帧/秒按角速度补帧，所以转起来是连续的）
  - 手势状态切换有连续 3 帧一致性判定，手指抖动不会来回跳

## 为什么必须用 http(s) 打开

浏览器不允许 `file://` 页面调用摄像头（请求会挂住、连权限弹窗都不弹）。所以：

- 直接用在线链接，或
- 本地起个服务：在本目录执行 `python -m http.server 8088`，然后打开 `http://127.0.0.1:8088/index.html`

单文件双击也能看，动画/拖动/缩放/点击散开都正常，只有「手势模式」不可用（页面会在 6 秒后明确提示原因）。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `index.html` | **全部源代码**：HTML + 内联 CSS + 内联 JS（3D 粒子着色器、缓动、手势识别与旋转、配色参数都在里面），也是最终发布产物 |
| `圣诞树.src.html` | 构建源，和 `index.html` 内容一致，只是字体 `@font-face` 的 url 留了 `__FONT_URI__` 占位符 |
| `build.py` | 打包脚本：把 `great-vibes-latin.woff2` 转 base64 填进占位符，输出 `index.html` |
| `great-vibes-latin.woff2` | 手写体 "Merry Christmas" 用的 Great Vibes 字体（42KB） |
| `vision_bundle.mjs`、`vision_wasm_*.js/.wasm`、`hand_landmarker.task` | MediaPipe Tasks Vision 的手势识别运行库与模型，自托管兜底用；页面正常优先走 npm 镜像，加载慢时才回落到这里 |

重新构建：

```bash
python build.py
```

## 改哪里

- 粒子数量 / 树高 / 相机距离：`TREE_POINTS`、`GROUND`、`STAR`、`HEART`、`CAM_DIST`、`TREE_HEIGHT`
- 配色：着色器与填充层的颜色常量（天蓝 `(102,188,236)` → 冷白 `(248,252,250)`)
- 手势灵敏度：`handRotSm` 的 EMA 系数、`handVel` 的平滑与上限（2.2 rad/s）、识别间隔（66ms）
- 照片：`PHOTO_MAX`（上限 24）、`layoutPhotos()` 里的挂位半径与散开半径 `haloR`、绘制宽度 `1.22 * f * sc`、背面渐隐范围 `smoothFade((dep - 0.34) / 0.54)`
- 界面隐藏：自动隐藏延时 4200ms、`#stage.ui-idle` / `.ui-hide` 的过渡时长
- 画质上限：`MAX_PIX` 与 `dpr` 上限（默认按物理像素 1:1 输出，避免发糊）

## 致谢

- 几何与配色灵感来自 [ZekangLi-Zico/Christmas-Tree](https://github.com/ZekangLi-Zico/Christmas-Tree)（原版为 Python/Pygame 实现，`tree.py`）
- 手势识别使用 [MediaPipe Tasks Vision HandLandmarker](https://developers.google.com/mediapipe)
- 字体 Great Vibes（SIL Open Font License）
