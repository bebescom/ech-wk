[app]
# (str) 应用名称
title = ECH Workers

# (str) 包名 (格式: com.username.appname)
package.name = echworkers

# (str) 包域名 (反序)
package.domain = org.ech

# (str) 应用版本
version = 1.3.0

# (str) 应用描述
description = ECH Workers 代理客户端，支持 ECH 加密和智能分流

# (str) 应用作者
author = byJoey
author.email = your.email@example.com

# (str) 应用URL
url = https://github.com/byJoey/ech-wk

# (str) 应用图标路径
icon.filename = %(source.dir)s/app_icon.png

# (str) 应用启动画面
presplash.filename = %(source.dir)s/app_icon.png

# (str) 应用方向 (portrait/landscape)
orientation = portrait

# (list) 包含的文件扩展名
source.include_exts = py,png,jpg,kv,atlas,js,sh,go,exe

# (list) 排除的文件扩展名
source.exclude_exts = spec,pyc,pyo

# (list) 包含的目录
source.include_dirs = .

# (list) Python依赖
requirements = python3,pyqt5,pyside2,pystray,pillow,requests

# (str) Python版本
python.version = 3.9

# (list) Android权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

# (int) Android API级别
android.api = 31

# (int) Android构建工具版本
android.build_tools = 31.0.0

# (str) Android NDK版本
android.ndk = 25.1.8937393

# (list) Android架构
android.arch = armeabi-v7a

# (str) Android SDK下载URL (使用国内镜像加速)
android.sdk_download_url = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) Android NDK下载URL (使用国内镜像加速)
android.ndk_download_url = https://mirrors.tuna.tsinghua.edu.cn/android/repository/

# (str) 自定义AndroidManifest.xml模板
android.manifest.intent_filters = []

# (list) 额外的Java依赖
android.add_java = []

# (list) 额外的AAR依赖
android.add_aars = []

# (list) 额外的库目录
android.add_libs = []

# (bool) 启用AndroidX
android.use_androidx = True

# (bool) 启用Jetifier
android.enable_jetifier = True

[buildozer]
# (int) 日志级别 (0 = 静默, 1 = 错误, 2 = 警告, 3 = 信息, 4 = 调试)
log_level = 2

# (bool) 缓存下载的依赖
cache_dir = .buildozer/cache

# (bool) 清理构建目录
clean_build = False

# (str) 构建输出目录
output_dir = bin

# (str) 构建日志文件
log_file = buildozer.log