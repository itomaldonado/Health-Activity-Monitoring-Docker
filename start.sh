service apache2 restart;
mongod --smallfiles & 
redis-server & 
python data.py