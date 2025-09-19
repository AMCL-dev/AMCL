import sys
import subprocess
import shutil
import os
import json
from pathlib import Path

def load_build_config():
    config_path = Path(__file__).parent.parent / "build_config.json"
    
    if not config_path.exists():
        print(f"错误: 未找到配置文件 {config_path}")
        print("请创建 build_config.json 文件并配置工具路径")
        print("示例配置:")
        example_config = {
            "visual_studio": {
                "vcvars64_path": "D:\\Software\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat"
            },
            "cmake": {
                "executable_path": "D:\\Software\\CLion\\bin\\cmake\\win\\x64\\bin\\cmake.exe"
            },
            "build": {
                "parallel_jobs": 14
            }
        }
        print(json.dumps(example_config, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取配置文件失败: {e}")
        sys.exit(1)

def validate_config(config):
    """验证配置文件"""
    # 根据平台确定必需的配置项
    if sys.platform == "win32":
        required_keys = {
            "visual_studio": ["vcvars64_path"],
            "cmake": ["executable_path"],
            "build": ["parallel_jobs"]
        }
    else:
        # Linux和macOS不需要Visual Studio配置
        required_keys = {
            "cmake": ["executable_path"],
            "build": ["parallel_jobs"]
        }
    
    for section, keys in required_keys.items():
        if section not in config:
            print(f"错误: 配置文件中缺少 [{section}] 部分")
            sys.exit(1)
        
        for key in keys:
            if key not in config[section]:
                print(f"错误: 配置文件中缺少 [{section}].[{key}]")
                sys.exit(1)
            
            # 验证文件路径是否存在
            if key.endswith("_path"):
                path = Path(config[section][key])
                if not path.exists():
                    print(f"错误: 路径不存在: {config[section][key]}")
                    sys.exit(1)
    
    return config

def build_with_nuitka():
    project_root = Path(__file__).parent.parent
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"
    assets_dir = project_root / "amcl" / "assets"

    for d in [build_dir, dist_dir]:
        if d.exists():
            shutil.rmtree(d)
    build_dir.mkdir(parents=True, exist_ok=True)
    dist_dir.mkdir(parents=True, exist_ok=True)

    # 基础Nuitka命令
    cmd = [
        sys.executable, "-m", "nuitka",
        "-oAMCL",
        "--standalone",
        "--lto=yes",
        "--disable-ccache",
        f"--include-data-dir={assets_dir}=assets",
        "--enable-plugin=pyside6",
        "--jobs=8",
        f"--output-dir={build_dir}",
        "--remove-output",
        "--assume-yes-for-downloads",
        f"{project_root / 'amcl' / 'src' / 'amcl.py'}"
    ]

    # 根据平台添加特定参数
    if sys.platform == "win32":
        cmd.extend(["--mingw64", "--windows-console-mode=disable"])
        cmd.extend(["--windows-icon-from-ico=" + str(assets_dir / "img/logo" / "icon.ico")])
    elif sys.platform == "darwin":
        cmd.append("--macos-create-app-bundle")
        cmd.extend(["--macos-app-icon=" + str(assets_dir / "img/logo" / "icon-256x.png")])
    else:  # Linux
        cmd.extend(["--linux-icon=" + str(assets_dir / "img/logo" / "icon-256x.png")])

    print("开始使用Nuitka打包...")
    print("执行命令: " + " ".join(cmd))

    try:
        subprocess.run(cmd, check=True, cwd=project_root)
        print("Nuitka打包成功完成!")

        target_dist = dist_dir / "amcl"
        if build_dir.exists():
            if target_dist.exists():
                shutil.rmtree(target_dist)
            shutil.move(str(build_dir), str(target_dist))
            print(f"应用已打包到: {target_dist}")
        else:
            raise FileNotFoundError(f"未找到预期的输出目录: {build_dir}")

        # 编译启动器（仅Windows平台）
        if sys.platform == "win32":
            print("开始编译启动器...")
            launcher_dir = project_root / "launcher"
            build_dir = launcher_dir / "cmake-build-release"

            config = load_build_config()
            config = validate_config(config)
            
            vs_bat = config["visual_studio"]["vcvars64_path"]
            cmake_exe = config["cmake"]["executable_path"]
            parallel_jobs = config["build"]["parallel_jobs"]

            cmd_str = f'cmd /c ""{vs_bat}" && "{cmake_exe}" --build "{build_dir}" --target AMCL -j {parallel_jobs}"'
            
            try:
                subprocess.run(cmd_str, check=True, cwd=launcher_dir, shell=True)
                print("启动器编译成功完成!")
            except subprocess.CalledProcessError as e:
                print(f"启动器编译失败，返回码: {e.returncode}")
                sys.exit(1)
            except Exception as e:
                print(f"启动器编译过程中发生错误: {e}")
                sys.exit(1)
        else:
            print("非Windows平台，跳过启动器编译")

    except subprocess.CalledProcessError as e:
        print(f"Nuitka打包过程失败，返回码: {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"打包过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_with_nuitka()