# استخدام نسخة محددة ومستقرة (Debian 11) لتجنب مشاكل التعريفات
FROM python:3.9-slim-bullseye

# تثبيت التعريفات (الطريقة المختصرة والمستقرة لنسخة Bullseye)
RUN apt-get update && apt-get install -y \
    curl apt-transport-https gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "gold.py"]