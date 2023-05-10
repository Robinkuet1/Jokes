cd backend
sudo sh build.sh
cd ..
sudo docker kill jokeweb
sudo docker rm jokeweb
sudo docker run --restart always -p 5679:80 -v $(pwd)/frontend:/usr/share/nginx/html:ro -d --name jokeweb nginx
