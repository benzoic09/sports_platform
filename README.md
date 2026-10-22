# sports_platform

# Prerequisites
mkdir sports_platform
cd sports_platform

python -m venv venv

# Windows
venv\Scripts\activate

pip install django
pip install psycopg2-binary
pip install pillow
pip install qrcode

django-admin startproject config .

python manage.py startapp accounts
python manage.py startapp sports