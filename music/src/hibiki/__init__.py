# Hibiki 命名空间包根目录
# 这是一个命名空间包，允许多个子包共存
__path__ = __import__('pkgutil').extend_path(__path__, __name__)