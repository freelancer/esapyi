from setuptools import setup, find_packages

setup(
    name='dm_management',
    version='0.1',
    description='A set of DM management tools',
    author='Adishwar Rishi',
    author_email='adiswa123@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask==1.0.2',
        'mypy_extensions',
        'uWSGI==2.0.18',
        'SQLAlchemy==1.3.1',
        'PyMySQL==0.9.3',
        'cryptography==2.6.1',
        'bcrypt==3.1.6',
        'pavlova==0.1.3',
    ],
    extras_require={
        'dev': [
            'pylint',
            'mypy',
            'alembic',
            'pytest',
        ],
    },
)
