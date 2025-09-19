# AMCL 多平台构建系统

本项目支持在 Windows、macOS 和 Linux 三个平台上进行构建。

## 本地构建

### 1. 准备工作

#### Windows 平台
- 安装 Python 3.13
- 安装 Visual Studio 2022（包含 C++ 开发工具）
- 安装 CMake
- 安装 Nuitka: `pip install nuitka pyside6`

#### macOS 平台
- 安装 Python 3.13
- 安装 Xcode 命令行工具: `xcode-select --install`
- 安装 Homebrew
- 安装 CMake: `brew install cmake`
- 安装 Nuitka: `pip install nuitka pyside6`

#### Linux 平台 (Ubuntu/Debian)
- 安装 Python 3.13
- 安装构建工具: `sudo apt-get install build-essential`
- 安装图形库依赖: `sudo apt-get install libgl1-mesa-glx libglib2.0-0`
- 安装 CMake: `sudo apt-get install cmake`
- 安装 Nuitka: `pip install nuitka pyside6`

### 2. 配置构建

在项目根目录创建 `build_config.json` 文件：

#### Windows 配置示例
```json
{
  "visual_studio": {
    "vcvars64_path": "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars64.bat"
  },
  "cmake": {
    "executable_path": "cmake"
  },
  "build": {
    "parallel_jobs": 4
  }
}
```

#### macOS/Linux 配置示例
```json
{
  "cmake": {
    "executable_path": "cmake"
  },
  "build": {
    "parallel_jobs": 4
  }
}
```

### 3. 执行构建

```bash
python scripts/build.py
```

构建完成后，可执行文件将在 `dist/amcl` 目录中。

## GitHub Actions 自动构建

当创建新的版本标签（格式为 `v*`）时，GitHub Actions 会自动构建三个平台的版本：

- Windows: `AMCL-Windows-x64`
- macOS: `AMCL-macOS-x64`
- Linux: `AMCL-Linux-x64`

### 构建流程

1. **设置环境**：根据不同平台安装相应的依赖
2. **配置构建**：创建平台特定的构建配置文件
3. **Nuitka 打包**：使用 Nuitka 将 Python 应用打包为独立可执行文件
4. **启动器编译**（仅 Windows）：编译 C++ 启动器
5. **打包产物**：将构建产物按平台分类打包
6. **发布版本**：自动创建 GitHub Release 并上传构建产物

### 构建产物

每个平台的构建产物包含：
- 可执行文件
- 所有必需的动态链接库
- PySide6 组件
- 应用资源文件
- 图标文件

## 注意事项

1. **配置文件**：`build_config.json` 包含个人开发环境的路径信息，已被添加到 `.gitignore` 中，不会被提交到版本控制。
2. **平台差异**：
   - Windows 平台会编译额外的 C++ 启动器
   - macOS 平台会生成应用包（.app）
   - Linux 平台生成标准的可执行文件
3. **图标文件**：确保 `amcl/assets/img/logo/` 目录中包含所需的图标文件：
   - `icon.ico` (Windows)
   - `icon-256x.png` (macOS/Linux)
4. **性能优化**：构建过程使用了 LTO（链接时优化）和 UPX（可执行文件压缩）来优化最终产物的大小和性能。

## 故障排除

### Windows 构建问题
- 确保 Visual Studio 2022 已正确安装
- 检查 `vcvars64.bat` 路径是否正确
- 确保 CMake 在 PATH 中或路径配置正确

### macOS 构建问题
- 确保 Xcode 命令行工具已安装
- 检查 Homebrew 是否正确安装
- 确保有足够的磁盘空间进行构建

### Linux 构建问题
- 确保已安装所有必需的系统依赖
- 检查 Python 开发头文件是否安装
- 确保有权限写入项目目录

## 贡献指南

如果您需要为项目贡献代码，请确保：
1. 在您的开发平台上测试构建过程
2. 不要提交个人的 `build_config.json` 文件
3. 确保所有平台的构建配置都能正常工作
4. 在提交 PR 之前运行完整的构建测试