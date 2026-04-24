from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_turtle_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # 🔥 launch 파일 등록 (필수)
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),

        # 🔥 YAML(config) 등록 (필수)
        (os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'circle_node = my_turtle_pkg.circle_turtle:main',
            'talker = my_turtle_pkg.my_talker:main',
            'listener = my_turtle_pkg.my_listener:main',
	    'image_repub = my_turtle_pkg.image_repub:main',
            'image_listener = my_turtle_pkg.image_listener:main',
        ],
    },
)
