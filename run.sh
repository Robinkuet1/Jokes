sudo sh backend/build.sh
sudo docker kill jokeweb
sudo docker rm jokeweb
sudo docker run --restart always -p 5679:5679 -v $pwd/frontend:/usr/share/nginx/html:ro -d --name jokeweb nginx
