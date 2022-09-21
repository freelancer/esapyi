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
        'Flask==2.2.2',
        'mypy_extensions',
        'uWSGI==2.0.20',
        'SQLAlchemy==1.4.41',
        'PyMySQL==1.0.2',
        'cryptography==38.0.1',
        'bcrypt==4.0.0',
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
