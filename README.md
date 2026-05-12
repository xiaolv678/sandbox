# Calculator App

一个用 Python `tkinter` 写的桌面计算器示例项目。

## 这是不是一个真正的 App

是。源码运行时需要 Python；打包后可以生成别人双击运行的桌面程序。

注意：桌面 App 需要按系统分别打包。

- Windows 用户：打包成 `Calculator.exe`
- Linux 用户：打包成 `Calculator`
- macOS 用户：打包成 macOS app，需要在 macOS 上构建

## 运行

如果运行时提示 `No module named 'tkinter'`，先安装系统依赖：

```bash
sudo apt install python3-tk
```

```bash
cd calculator_app
python3 main.py
```

如果提示 `no display name and no $DISPLAY environment variable`，说明当前终端没有连接到图形桌面，窗口弹不出来。可以在系统桌面里的终端运行，或者先用终端模式：

```bash
python3 main.py --cli
```

## 打包给别人下载

### Linux

在 Linux 图形桌面或服务器上都可以构建 Linux 可执行文件：

```bash
cd calculator_app
chmod +x build_app.sh
./build_app.sh
```

生成文件：

```text
dist/Calculator
```

把这个文件发给 Linux 用户即可。对方可能需要给它执行权限：

```bash
chmod +x Calculator
./Calculator
```

### Windows

Windows 的 `.exe` 最好在 Windows 环境里打包。原因是 PyInstaller 基本是“在哪个系统打包，就生成哪个系统的程序”：Linux 上生成 Linux 可执行文件，Windows 上生成 `.exe`。

建议使用 Python 3.10、3.11 或 3.12 的官方 Windows 安装包，并确认安装时包含 Tcl/Tk。可以先检查：

```powershell
py -c "import tkinter; root = tkinter.Tk(); root.destroy(); print('tkinter OK')"
```

如果这一步报错，说明当前 Python 的桌面窗口组件没有装好，需要重新安装 Python，并勾选 Tcl/Tk 相关组件。

方案一：把整个 `calculator_app` 文件夹复制到 Windows 电脑，然后在 PowerShell 里运行：

```powershell
cd calculator_app
.\build_windows.ps1
```

也可以在 Windows 命令提示符里运行：

```bat
cd calculator_app
build_windows.bat
```

生成文件：

```text
dist\Calculator.exe
```

这个 `Calculator.exe` 就可以发给别人下载、双击运行。

如果打包日志里出现：

```text
WARNING: tkinter installation is broken. It will be excluded from the application
```

说明这个 Python 环境里的 `tkinter`/Tcl/Tk 不完整。虽然可能仍然生成了 `dist\Calculator.exe`，但这个 exe 很可能打不开图形界面。换一个安装完整 Tcl/Tk 的官方 Python 后重新打包。

方案二：用 GitHub Actions 自动打包。把 `calculator_app` 目录里的代码推到 GitHub 仓库，GitHub 会用 Windows runner 构建，并在 Actions 页面生成 `Calculator-Windows` 下载产物。

项目里已经包含自动构建配置：

```text
.github/workflows/build-windows.yml
```

### 为什么不能直接在这台服务器上看到窗口

你当前连接的是服务器终端，不是图形桌面会话。没有 `DISPLAY` 或 `WAYLAND_DISPLAY` 时，桌面窗口没地方显示。但这不影响写代码和打包发布。

## 测试

```bash
cd calculator_app
python3 -m unittest discover
```

## 功能

- 支持加、减、乘、除、取模
- 支持小数和括号
- 支持键盘输入
- 支持回车计算、退格删除、Esc 清空
- 计算逻辑和界面分离，方便继续扩展

## 项目文件

- `main.py`：桌面界面入口
- `calculator.py`：计算逻辑
- `tests/`：单元测试
- `calculator.spec`：PyInstaller 打包配置
- `build_app.sh`：Linux 打包脚本
- `build_windows.ps1`：Windows 打包脚本
- `build_windows.bat`：Windows 命令提示符打包脚本
- `.github/workflows/build-windows.yml`：GitHub Actions 自动构建 Windows `.exe`
