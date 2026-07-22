#!/bin/bash
echo "Waiting for MySQL..."

while ! python -c "
import MySQLdb, os
try:
    MySQLdb.connect(
        host=os.environ.get('DB_HOST','db'),
        user=os.environ.get('DB_USER','root'),
        passwd=os.environ.get('DB_PASSWORD','root123'),
        db=os.environ.get('DB_NAME','library_db')
    )
    exit(0)
except Exception as e:
    print(e)
    exit(1)
"; do
  echo "MySQL not ready — retrying in 3s..."
  sleep 3
done

echo "MySQL ready!"
python manage.py migrate
exec gunicorn --bind 0.0.0.0:8000 Library_Management.wsgi