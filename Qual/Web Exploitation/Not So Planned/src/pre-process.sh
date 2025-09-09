sudo docker build -t not-so-planned-builder ./client &&
sudo docker create --name temp-artifact not-so-planned-builder &&
sudo docker cp temp-artifact:/output/ ./ &&
mv ./output ./spawner/bot/dist