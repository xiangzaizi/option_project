# -*- coding:utf-8 -*-

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10
    from pip._internal.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)

with open('./VERSION.txt', 'rb') as f:
    version = f.read().strip()
    """
       作为一个合格的模块，应该要有版本号
    """
    setup(
        name='scrapy_option',  # 模块名称
        version=version,
        description='A mini spider framework, like Scrapy',  # 描述
        packages=find_packages(exclude=[]),
        author='ian',
        author_email='test@email.com',
        license='Apache License v2',  # BSD百度, 遵循linux...协议
        package_data={'': ['*.*']},
        url='#',
        # 获取第三方的工具
        install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],  # 所需的运行环境
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )

# 说明: 切换到setup.py所在目录, 执行python setup.py install