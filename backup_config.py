"""
腾讯云COS备份配置文件
版本: 1.0
作者: 客水

功能描述:
定义备份配置项和腾讯云COS连接参数
"""

config = {
    # 备份配置：需要备份的文件/目录列表(相对路径)
    # 类型: list[str]
    # 示例: ['file1.txt', 'dir1']
    'backup_config': ['backuptest.txt', 'backuptest'],
    
    # 腾讯云COS配置
    # 存储桶名称(格式: <bucketname>-<appid>)
    'bucket': '',
    
    # 地域代码(参考腾讯云文档)
    'region': 'ap-guangzhou',
    
    # API密钥ID(需保密)
    'secret_id': '',
    
    # API密钥Key(需保密)
    'secret_key': '',
    
    # 目标路径配置
    # 云端目标目录(需以/开头和结尾)
    'target_dir': '/backups/'
}