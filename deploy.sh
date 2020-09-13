
echo Enter a secure password you will use to access your dokku instance \(will be used to encrypt your ssh key\)

read user_password
echo  $user_password

echo Enter a your dokku domain or IP address

read dokku_host
echo  $dokku_host
echo $dokku_host >> dokku_host.config


ssh root@$dokku_host dokku ssh-keys:remove streamlitdokkugui
cat ./.ssh.pub | ssh root@$dokku_host dokku ssh-keys:add streamlitdokkugui

ssh  -o StrictHostKeyChecking=no root@$dokku_host dokku --force apps:destroy gui
ssh  -o StrictHostKeyChecking=no root@$dokku_host dokku apps:create gui

git remote add dokku dokku@$dokku_host:gui


git add *
git add --force .ssh dokku_host.config
git commit -m "deploying"
git push dokku master

