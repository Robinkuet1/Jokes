sudo docker kill JokeAPI
sudo docker rm JokeAPI
sudo docker build . -t robinkuet1/JokeAPI
sudo docker run --restart always -p 5678:5678 --link database:db -d --name JokeAPI robinkuet1/JokeAPI
