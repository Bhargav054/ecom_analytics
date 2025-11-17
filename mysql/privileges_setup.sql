CREATE USER 'datauser'@'localhost' IDENTIFIED BY 'Data@123';
GRANT ALL PRIVILEGES ON ecom_db.* TO 'datauser'@'localhost';
FLUSH PRIVILEGES;