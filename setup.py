import setuptools

setuptools.setup(
    name="LolSapiensApi",
    version="0.1.0",
    description="This is LolSapiens API.",
    packages=setuptools.find_packages(),
    install_requires=[
        "fastapi",
        "python-dotenv",
        "requests",
        "scikit-learn",
        "uvicorn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
