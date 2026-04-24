from setuptools import setup
import os
from glob import glob

package_name = 'my_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # launch 파일 등록
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='My robot package',
    license='TODO: License declaration',

    # 🔥 여기 하나만 있어야 함
    entry_points={
        'console_scripts': [
            'pure_pursuit = my_bot.pure_pursuit:main',
            'click_to_goal = my_bot.click_to_goal:main',
            'pure_pursuit_obstacle = my_bot.pure_pursuit_obstacle:main',
	    'astar_planner = my_bot.a_star_planner:main',
	    'astar_pure_pursuit = my_bot.astar_pure_pursuit:main',
	    'emergency_stop = my_bot.emergency_stop:main',
    	    'fake_detector = my_bot.fake_detector:main',
        ],
    },
)
