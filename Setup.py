from setuptools import setup, find_packages

setup(
    name='Camouflage-AI',
    version='1.0.0',
    author='Vishnu',
    author_email='vishnu.tppr@gmail.com',
    description='Camofluge AI – An AI-powered desktop tool for removing video backgrounds using YOLOv8 segmentation.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Vishnu-tppr/Camouflage-AI',  
    packages=find_packages(),
    py_modules=["Camouflage AI"], 
    install_requires=[
        'customtkinter',
        'opencv-python',
        'numpy',
        'rembg',
        'pillow',
        'moviepy',
        'matplotlib',
        'scikit-image',
        'tqdm',
        'pyperclip'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Video',
        'Intended Audience :: Developers',
        'Environment :: Win32 (MS Windows)',
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
