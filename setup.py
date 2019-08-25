from setuptools import setup, find_packages

setup(
    name='api_boilerplate',
    version='0.1',
    description='A python API boilerplate',
    author='Adishwar Rishi',
    author_email='adiswa123@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask==1.1.1',
        'mypy_extensions',
        'uWSGI==2.0.18',
        'SQLAlchemy==1.3.7',
        'PyMySQL==0.9.3',
        'cryptography==2.7',
        'bcrypt==3.1.7',
        'pavlova==0.1.3',
    ],
    extras_require={
        'dev': [
            'pylint',
            'mypy',
            'alembic',
            'pytest',
            'pytest-cov',
        ],
    },
)
