#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"generatorlabs": ["py.typed"]},
)
