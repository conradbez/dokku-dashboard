ssh-keygen -b 2048 -t rsa -f ./.ssh -q -N "ThisIsMyLoginPassword"

ssh root@128.199.180.162 dokku ssh-keys:remove streamlitdokkugui
cat ./.ssh.pub | ssh root@128.199.180.162 dokku ssh-keys:add streamlitdokkugui

ssh  -o StrictHostKeyChecking=no root@128.199.180.162 dokku apps:create gui

git remote add dokku dokku@128.199.180.162:gui

git add *
git commit -m "deploying"
git push dokku master

