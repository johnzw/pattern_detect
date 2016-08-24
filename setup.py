from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='patterndetect',
      version='0.1',
      description='detect specific pattern from graph',
      long_description=readme(),
      classifiers=[
        'Development Status :: Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Pattern Recognition :: graph',
      ],
      author='zw_casia',
      author_email='rzzw456@126.com',
      license='MIT',
      packages=['patterndetect'],
      install_requires=[
          'pillow',
      ],
      scripts=['bin/detect-pattern'],
      zip_safe=False)