from setuptools import setup, find_packages

setup(
    name="itto-yolo-tool",
    version="2.0.1",
    author="rinst",
    author_email="544250926@qq.com",
    description="A integrated GUI tool for YOLO model training and annotation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RinST-Dreaming/Yolo-integrated-training-tool",
    packages=find_packages(),
    include_package_data=True, 
    
    install_requires=[
        "PyQt5>=5.15.0",
        "opencv-python>=4.5.0",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "itto=itto_yolo_tool.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)