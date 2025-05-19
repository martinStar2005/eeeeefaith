from setuptools import setup, find_packages

setup(
    name="martin_faith",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Django==5.0.2",
        "django-parler==2.3",
        "django-rosetta==0.9.9",
        "Pillow==10.1.0",
        "django-hitcount==1.3.5",
        "django-crispy-forms==2.1",
        "crispy-bootstrap5==2023.10",
        "python-decouple==3.8",
        "django-ckeditor==6.7.0",
    ],
    author="Martin Faith",
    author_email="info@martinfaith.com",
    description="A multilingual Christian website with news, bible verses, FAQs, and testimonials",
)