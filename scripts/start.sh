docker stop $(docker ps -a -q)
docker-compose down
docker-compose up -d
sleep 5
#python3 scripts/startup_db.py
docker-compose logs -f api