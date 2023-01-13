from setuptools import setup

setup(
  name='taoniu',
  version='0.0.0',
  entry_points={
    'console_scripts': [
      'cryptos=cryptos:cli',
      'bt=bt:cli',
    ],
  },
)
