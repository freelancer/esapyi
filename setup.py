from setuptools import setup, find_packages

setup(
    name='esapyi',
    version='1.0',
    description=(
        'A dockerized and production ready python API template with no '
        'setup required.'
    ),
    author='Adishwar Rishi',
    author_email='adiswa123@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask==1.1.1',
        'mypy_extensions',
        'uWSGI==2.0.18',
        'SQLAlchemy==1.3.13',
        'PyMySQL==0.9.3',
        'cryptography==2.8',
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
