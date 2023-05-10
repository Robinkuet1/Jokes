sudo docker kill jokeapi
sudo docker rm jokeapi
sudo docker build . -t robinkuet1/jokeapi
sudo docker run --restart always -p 5678:5678 --link database:db -d --name jokeapi robinkuet1/jokeapi
