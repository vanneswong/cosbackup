"""
腾讯云对象存储备份工具
版本: 1.0
作者: 客水

功能描述:
1. 将本地文件和目录备份到腾讯云对象存储(COS)
2. 支持递归上传整个目录结构
3. 记录详细的备份日志

依赖:
- 腾讯云COS SDK v5.4.6
"""
import os
import time
from qcloud_cos import CosConfig, CosS3Client
import backup_config

# 日志文件配置
LOG_FILE = 'cosbackup.log'

def write_log(message):
    """
    写入日志信息到日志文件
    
    参数:
        message (str): 要记录的日志内容
    
    返回值:
        None
    
    日志格式:
        [YYYY-MM-DD HH:MM:SS] 日志内容
    """
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        f.write(f'[{timestamp}] {message}\n')

def upload_file(client, local_path, bucket, target_key):
    """
    上传单个文件到腾讯云COS
    
    参数:
        client (CosS3Client): 已初始化的COS客户端对象
        local_path (str): 要上传的本地文件绝对路径
        bucket (str): 目标存储桶名称
        target_key (str): 云端目标路径(包含文件名)
    
    返回值:
        None
    
    异常:
        捕获所有异常并记录到日志文件
    """
    try:
        with open(local_path, 'rb') as fp:
            client.put_object(
                Bucket=bucket,
                Key=target_key,
                Body=fp
            )
        msg = f'上传成功: {local_path} -> {target_key}'
        print(msg)
        write_log(msg)
    except Exception as e:
        msg = f'上传失败 {local_path}: {str(e)}'
        print(msg)
        write_log(msg)

def upload_directory(client, local_dir, bucket, target_prefix):
    """
    递归上传整个目录到腾讯云COS
    
    参数:
        client (CosS3Client): 已初始化的COS客户端对象
        local_dir (str): 要上传的本地目录绝对路径
        bucket (str): 目标存储桶名称
        target_prefix (str): 云端目标路径前缀
    
    返回值:
        None
    
    说明:
        1. 会保留目录结构
        2. 使用upload_file函数逐个上传文件
    """
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            target_key = os.path.join(target_prefix, relative_path).replace('\\', '/')
            upload_file(client, local_path, bucket, target_key)

def main():
    """
    程序主入口
    
    功能流程:
        1. 加载配置文件
        2. 初始化COS客户端
        3. 遍历备份配置项
        4. 根据类型调用文件或目录上传函数
    
    返回值:
        None
    """
    # 加载配置
    config = backup_config.config
    
    # 初始化COS客户端
    cos_config = CosConfig(
        Region=config['region'],
        SecretId=config['secret_id'],
        SecretKey=config['secret_key']
    )
    client = CosS3Client(cos_config)
    
    # 处理备份项
    for item in config['backup_config']:
        local_path = os.path.join(os.getcwd(), item)
        target_key = os.path.join(config['target_dir'], item).replace('\\', '/')
        
        if os.path.isfile(local_path):
            upload_file(client, local_path, config['bucket'], target_key)
        elif os.path.isdir(local_path):
            upload_directory(client, local_path, config['bucket'], target_key)
        else:
            msg = f'警告: 路径不存在 {local_path}'
            print(msg)
            write_log(msg)

if __name__ == '__main__':
    main()