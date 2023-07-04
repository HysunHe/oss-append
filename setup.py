""" docstring """
from setuptools import setup

setup(
    name='oss_append',
    version='1.0',
    description='oss_append',
    author='hysun',
    author_email='hysunhe@foxmail.com',
    url='https://github.com/HysunHe/PythonLearn',
    license='XXX License 2.0',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python 3.8',
        'Programming Language :: Python 3.9',
        'Programming Language :: Python 3.10',
    ],
    # packages=['devlog'], # packages参数时，不会递归的打包子package！只打包当前package！
    # packages=find_packages(), #find_packages只会打包内含__init__.py的package
    # packages=find_namespace_packages(),
    include_package_data=True,  #默认值为True。当为True时，将根据http://MANIFEST.in文件来打包分发库。
    python_requires='>=3.8, <3.11',
    install_requires=[
        'oci>=2.104,<3',
        'oci-cli>=3.29,<4',
    ],
    entry_points={  #把python文件中的函数自动生成为可执行脚本
        'console_scripts': [  # key值为console_scripts
            'ossappend = main:main'
        ]
    },
    scripts=['main.py']  #把.sh、.py等可执行脚本生成到系统path中
)
