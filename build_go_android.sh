#!/bin/bash
# 交叉编译Go代码为Android arm-v7a架构

set -e

# 检查必要的命令
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "错误: 未找到命令 $1"
        exit 1
    fi
}

check_command "go"
check_command "wget"
check_command "unzip"

# 配置参数
NDK_VERSION="r25b"
NDK_URL="https://dl.google.com/android/repository/android-ndk-${NDK_VERSION}-linux.zip"
ANDROID_API="21"

# 下载并解压NDK
download_ndk() {
    if [ ! -d "android-ndk-${NDK_VERSION}" ]; then
        echo "正在下载Android NDK ${NDK_VERSION}..."
        wget -q ${NDK_URL}
        
        echo "正在解压NDK..."
        unzip -q android-ndk-${NDK_VERSION}-linux.zip
        
        # 清理压缩包
        rm -f android-ndk-${NDK_VERSION}-linux.zip
    fi
}

# 设置交叉编译环境
setup_environment() {
    export ANDROID_NDK_HOME=$(pwd)/android-ndk-${NDK_VERSION}
    
    # 检查NDK工具链
    if [ ! -d "${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/linux-x86_64" ]; then
        echo "错误: 未找到NDK工具链"
        exit 1
    fi
    
    # 设置编译器
    export CC=${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/linux-x86_64/bin/armv7a-linux-androideabi${ANDROID_API}-clang
    export CXX=${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/linux-x86_64/bin/armv7a-linux-androideabi${ANDROID_API}-clang++
    
    # 设置Go交叉编译参数
    export GOOS=android
    export GOARCH=arm
    export GOARM=7
    export CGO_ENABLED=1
    
    echo "环境变量已设置:"
    echo "ANDROID_NDK_HOME: ${ANDROID_NDK_HOME}"
    echo "CC: ${CC}"
    echo "GOOS: ${GOOS}"
    echo "GOARCH: ${GOARCH}"
}

# 编译Go代码
build_go() {
    echo "正在编译Go代码..."
    
    # 检查Go源文件
    if [ ! -f "ech-workers.go" ]; then
        echo "错误: 未找到ech-workers.go文件"
        exit 1
    fi
    
    # 编译
    go build -o ech-workers ech-workers.go
    
    # 验证编译结果
    if [ ! -f "ech-workers" ]; then
        echo "错误: 编译失败，未生成可执行文件"
        exit 1
    fi
    
    # 检查文件类型
    file_output=$(file ech-workers)
    echo "编译结果: ${file_output}"
    
    if echo "${file_output}" | grep -q "ARM, EABI5"; then
        echo "✓ 成功编译为arm-v7a架构"
    else
        echo "警告: 编译结果可能不是预期的架构"
    fi
}

# 主函数
main() {
    echo "=== ECH Workers Go代码交叉编译脚本 ==="
    
    # 下载NDK
    download_ndk
    
    # 设置环境
    setup_environment
    
    # 编译Go代码
    build_go
    
    echo "=== 编译完成 ==="
    echo "可执行文件: ech-workers"
    echo "文件大小: $(ls -lh ech-workers | awk '{print $5}')"
}

# 执行主函数
main