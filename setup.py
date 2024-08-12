from setuptools import setup, find_packages

setup(
    name='cm',
    version='0.1.0',
    packages=find_packages(include=['cm']),
    package_data={'cm': ['data/*']},
    install_requires=[
        'pillow',
        'pystray',
        'pywin32'
    ],
    entry_points={
        'console_scripts': ['cm=cm.__main__:main']
    },
    windows = [
        {
            'icon_resources': [(1, "cm/cm.ico")],
            'console':False
        }
    ]
)
