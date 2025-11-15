<div align="center">

# CubeSimulator

_一个简单的三阶魔方桌面模拟器，支持键盘和图形界面操作。_

</div>

## 概览

CubeSimulator 是一个三阶魔方模拟器项目，特点是：

- 使用 **pygame** 绘制魔方的伪 3D 视图（展示三个面）
- 使用 **Tkinter** 提供控制面板（按钮、打乱、计时器等）
- 使用 **kociemba** 库作为求解器（两阶段算法）

魔方转动记号采用常见的 WCA / Singmaster 记号：

- 大写字母（R、L、U、D、F、B）表示单层转动
- 小写字母（r、l、u、d、f、b）表示双层转动
- 中层记号（M、S、E）与整体旋转（x、y、z）也可通过按钮或键盘触发

项目地址：<https://github.com/DecarbonizedGlucose/CubeSimulator/>

## 功能特性

- 一键复原魔方
- 通过 GUI 按钮或实体键盘控制魔方旋转
- 支持随机打乱，并展示本次打乱公式
- 支持用户按一定格式输入当前魔方状态（非法状态会给出提示）
- 基于当前状态求解（使用 kociemba 算法）
- 按解法序列自动逐步还原魔方（带短暂停顿以增加观感）
- 为玩家还原魔方计时（不建议在计时中使用自动还原）

> 说明：  
> 自动复原功能本可以“瞬间复原”，为了视觉效果更好，程序在每一步之间  
> 人为加入了 `0.03` 秒的停顿。

## 运行环境与依赖

### 基本环境

- Python **3.8 及以上**（在 CPython 3.9 下测试）
- 桌面环境支持：
  - Tk 图形界面（Tkinter）
  - SDL2（供 pygame 使用）

推荐安装字体（可选，但能让界面更好看）：

- `Microsoft YaHei`（微软雅黑，用于中文界面）
- `Consolas`（英文等宽字体，用于按钮标签）

### Python 第三方库

需要安装以下 Python 包：

- `kociemba` —— 魔方求解器
- `pygame` 或 `pygame-ce` —— 图像绘制与键盘输入

使用 pip 安装示例：

```sh
pip install kociemba
pip install pygame-ce  # 或：pip install pygame
```

在某些 Linux 发行版（例如 Arch Linux）上，建议先安装 SDL2 和 Tk 相关的
系统库，再安装 Python 包，例如：

## 快速开始

1. 克隆仓库：
2. 确保已安装依赖（参考上面的依赖章节）
3. 运行主程序：

正常情况下，会弹出两个窗口：

1. **pygame** 窗口：显示魔方视图
2. **Tkinter** 窗口：控制面板（按钮、菜单、计时器等）

如果只有一个窗口或完全没有窗口，请参考下方“常见问题排查”。

## 键盘操作说明

魔方旋转键位（Singmaster 风格）：

Tk 控制窗口中也提供了对应的按钮，包括：

- 各个面的单层 / 双层旋转
- 中层（M、S、E）旋转
- 整体旋转（x、y、z）
- 随机打乱、手动输入状态、求解、自动复原
- 计时开始 / 停止 / 清零

## 常见问题排查（FAQ）

### 1. 程序无法启动 / 没有窗口弹出

建议先在终端中运行，并观察是否有报错信息：

如果使用的是 Linux，且报错类似：

这通常表示当前环境或线程中无法创建 OpenGL 上下文。当前版本已经：

- 不再主动请求显式 OpenGL 上下文；
- 将 pygame 主循环放在主线程中；

在大多数桌面环境（含 Wayland + XWayland）下，这可以避免上述错误。
如果你依然遇到该问题，建议在 issues 中附上：

- 操作系统与发行版
- 桌面环境 / 窗口系统（X11 / Wayland）
- Python 版本
- pygame / pygame-ce 版本

### 2. 报错 `ImportError: No module named tkinter`

说明你的 Python 没有安装 Tk 运行库或未正确链接。

- 在 **Arch Linux** 上可执行：
- 在 **Ubuntu / Debian** 上可执行：

安装完成后重新运行：

### 3. 报错 `ModuleNotFoundError: No module named 'kociemba'` 或 `pygame`

说明缺少必要的 Python 包。请先确保虚拟环境（如有）已激活，然后执行：

安装完成后再次运行主程序。

### 4. 点击“退出程序”后进程没有完全退出

当前版本中，提供了一个统一的 `sysQuit()` 函数，用于：

- 停止 pygame 主循环；
- 关闭 Tk 控制窗口；
- 释放相关资源并正常退出进程。

推荐使用：

- Tk 窗口菜单中的“退出程序”，或
- 关闭 Tk 窗口的系统关闭按钮（右上角 X），

来结束程序。如果依然出现僵尸进程或异常，请在 issue 中提供终端输出。

## 建议的开发 / 调试方式

- 使用虚拟环境：
- 在修改代码后，从终端重新运行 `python CubeSimulator.py`，及时观察
  Traceback 信息，便于定位问题。

## 许可证

本项目以 MIT License 开源（如仓库中包含 `LICENSE` 文件，请以其为准）。

## 其他

如果你对魔方有更深的研究或有更多功能想法（如：

- 全局 3D 视角、
- 更多求解算法、
- 统计练习数据等），
  欢迎在 GitHub 仓库中提 issue 或发起 PR，一起把这个小工具变得更好用。