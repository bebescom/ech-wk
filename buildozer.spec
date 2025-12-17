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

# (str) 源代码目录（必需配置）
source.dir = .

# (list) 包含的文件扩展名
source.include_exts = py,kv,txt,bin,png,jpg,js,sh,go,exe

# (list) 排除的文件扩展名
source.exclude_exts = spec,pyc,pyo
source.exclude_patterns = android-ndk-r25*/**/*.py

# (list) 包含的目录
source.include_dirs = .

# (list) 应用依赖
# ✅ 统一Python版本为3.10.13
requirements = python3==3.10.13,kivy==2.3.0,pillow,requests

# (str) Python版本
python.version = 3.10

# (list) Android权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

# (list) Android架构
android.archs = armeabi-v7a

# (str) 自定义AndroidManifest.xml模板
# ✅ 修复空列表配置 - 使用空字符串而不是 []
android.manifest.intent_filters = 

# (list) 额外的Java依赖
# ✅ 修复空列表配置 - 使用空字符串而不是 []
android.add_java = 

# (list) 额外的AAR依赖
# ✅ 修复空列表配置 - 使用空字符串而不是 []
android.add_aars = 

# (list) 额外的库目录
# ✅ 修复空列表配置 - 使用空字符串而不是 []
android.add_libs = 

# (bool) 启用AndroidX
android.use_androidx = True

# (bool) 启用Jetifier
android.enable_jetifier = True

# ✅ 启用AAB支持
android.enable_aab = True
android.release_artifact = aab
android.debug_artifact = apk

# Target Android API (稳定版)
android.api = 33

# Minimum API
android.minapi = 21

# Android SDK version
android.sdk = 33

# Build-Tools 版本
android.build_tools = 33.0.2

# NDK 路径
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25c

# 自动接受 license
android.accept_sdk_license = True

# 跳过系统 libffi 检查
p4a.libffi_no_system = True

# 强制旧 Cython
p4a.cython = 0.29.36

# ✅ 使用稳定版本
p4a.branch = v2024.01.21

# 下载重试增强
android.download_timeout = 600
android.download_retry = True
android.download_max_retries = 20

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

# (int) 全局超时时间（秒）
timeout = 300

# (bool) 允许重试
retry = True

# (int) 最大重试次数
max_retries = 3
