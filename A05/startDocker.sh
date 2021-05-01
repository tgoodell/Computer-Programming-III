docker build -t factorator .
docker stop factorator1
docker rm factorator1
docker stop factorator2
docker rm factorator2
docker stop factorator3
docker rm factorator3
docker run --cpus="1" -m 256m --name factorator1 -d --restart always -p 9201:1234 factorator  
docker run --cpus="1" -m 256m --name factorator2 -d --restart always -p 9202:1234 factorator  
docker run --cpus="1" -m 256m --name factorator3 -d --restart always -p 9203:1234 factorator  
