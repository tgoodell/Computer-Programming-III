docker build -t hangmanserver .
docker stop hangmanserver
docker rm hangmanserver
docker run --cpus="1" -m 256m --name hangmanserver -d --restart always -p 9220:2345 factorator

