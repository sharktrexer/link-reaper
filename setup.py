from setuptools import setup, find_packages

setup(
    name='link_reaper',
    version='0.1.0',
    packages=find_packages(
        where='src',
        include=['link_reaper*'],),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'link_reaperreap = link_reaper.reap.py:cli',
        ],
    },
)