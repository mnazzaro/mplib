from setuptools import setup

setup(
    name='mplib',
    version='0.1.0',    
    description='The backend library for Metal Poker',
    url='https://github.com/mnazzaro/mplib',
    author='Mark Nazzaro',
    author_email='marknazzaro2@gmail.com',
    license='BSD 2-clause',
    packages=['mplib'],
    install_requires=['Flask==2.2.2',
                      'Flask_Login==0.6.2',
                      'flask_sqlalchemy==3.0.3',
                      'pydantic==1.10.4',
                      'PyJWT==2.6.0',
                      'pytz==2022.7',
                      'redis==3.5.3',
                      'setuptools==65.5.0',
                      'SQLAlchemy==1.4.46',
                      'typing_extensions==4.5.0',
                      'Werkzeug==2.2.2',
                      'WTForms==3.0.1'
                    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: None',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9'
    ],
)