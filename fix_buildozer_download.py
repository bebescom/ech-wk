#!/usr/bin/env python3
"""
修复Buildozer下载函数的脚本
将urlretrieve替换为更可靠的curl下载方式
"""

import os
import sys
import subprocess
import tempfile
import shutil

def find_buildozer_install_path():
    """查找Buildozer的安装路径"""
    try:
        import buildozer
        return os.path.dirname(buildozer.__file__)
    except ImportError:
        print("错误：未找到Buildozer模块")
        return None

def patch_buildozer_download_function(buildozer_path):
    """修补Buildozer的下载函数"""
    if not buildozer_path:
        return False
        
    # Buildozer主文件路径
    buildozer_init_path = os.path.join(buildozer_path, '__init__.py')
    
    if not os.path.exists(buildozer_init_path):
        print(f"错误：未找到文件 {buildozer_init_path}")
        return False
        
    print(f"正在修补Buildozer文件：{buildozer_init_path}")
    
    # 读取原始文件内容
    with open(buildozer_init_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找download函数
    download_func_start = content.find('def download(self, url, filename,')
    if download_func_start == -1:
        print("错误：未找到download函数")
        return False
        
    # 查找函数结束
    lines = content[download_func_start:].split('\n')
    indent_level = 0
    func_end = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('def '):
            indent_level = len(line) - len(stripped)
        elif stripped.endswith(':') and not stripped.startswith('#'):
            indent_level += 4
        elif stripped == '':
            continue
        elif len(line) - len(stripped) < indent_level and stripped:
            func_end = i
            break
    
    if func_end == 0:
        print("错误：无法确定download函数的结束位置")
        return False
    
    # 新的下载函数代码
    new_download_code = '''    def download(self, url, filename,
                 progressbar=True, replace=False, cwd=None):
        """
        替换原有的urlretrieve下载函数，使用curl进行更可靠的下载
        """
        import subprocess
        import os
        
        if os.path.exists(filename) and not replace:
            self.info('File already exists, skipping download.')
            return True
            
        # 创建临时文件
        temp_filename = filename + '.part'
        
        try:
            # 使用curl下载，支持重试和断点续传
            self.info(f'Downloading {{url}}')
            self.info(f'Saving to {{filename}}')
            
            # 构建curl命令
            curl_cmd = [
                'curl', '-L', '--retry', '10', '--retry-delay', '10',
                '--max-time', '600', '--progress-bar',
                '-o', temp_filename, url
            ]
            
            # 执行curl命令
            result = subprocess.run(
                curl_cmd,
                cwd=cwd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.error(f'Curl download failed: {{result.stderr}}')
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
                return False
                
            # 验证文件大小
            if os.path.getsize(temp_filename) == 0:
                self.error('Downloaded file is empty')
                os.unlink(temp_filename)
                return False
                
            # 重命名临时文件
            if os.path.exists(filename):
                os.unlink(filename)
            os.rename(temp_filename, filename)
            
            self.info('Download successful')
            return True
            
        except Exception as e:
            self.error(f'Download error: {{str(e)}}')
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            return False'''
    
    # 替换函数内容
    new_content = (
        content[:download_func_start] +
        new_download_code +
        '\n' + content[download_func_start + sum(len(line) + 1 for line in lines[:func_end]) :]
    )
    
    # 创建备份
    backup_path = buildozer_init_path + '.backup'
    shutil.copy2(buildozer_init_path, backup_path)
    print(f"已创建备份文件：{backup_path}")
    
    # 写入修改后的文件
    with open(buildozer_init_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Buildozer下载函数修补成功！")
    return True

def main():
    """主函数"""
    print("=== Buildozer下载函数修复工具 ===")
    print("这个工具会将Buildozer的urlretrieve下载替换为更可靠的curl方式")
    print()
    
    # 查找Buildozer路径
    buildozer_path = find_buildozer_install_path()
    if not buildozer_path:
        print("无法找到Buildozer安装路径")
        return 1
    
    print(f"找到Buildozer安装在：{buildozer_path}")
    
    # 修补下载函数
    if patch_buildozer_download_function(buildozer_path):
        print()
        print("修复完成！现在Buildozer会使用curl进行下载，具有更好的稳定性和重试机制。")
        print("注意：这个修改会在Buildozer更新时被覆盖，需要重新运行此脚本。")
        return 0
    else:
        print("修复失败")
        return 1

if __name__ == '__main__':
    sys.exit(main())
