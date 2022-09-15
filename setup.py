import setuptools

setuptools.setup(
    name="settings",
    description="Manage your application settings quickly and in a flexible way!",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=[],
    extras_require={"pydantic-encoder": ["pydantic"], "yaml-serializer": ["pyyaml"]},
)
