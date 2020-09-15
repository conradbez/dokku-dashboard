# Get password from user
echo Enter a secure password you will use to access your dokku instance \(will be used to encrypt your ssh key\)
read user_password

# Get host name from user
echo Enter a your dokku domain or IP address
read dokku_host

# Write hostname to config file, to be read by app after deployment
rm dokku_host.config
echo $dokku_host >> dokku_host.config

ssh-keygen -f ./.ssh -N $user_password


# add the created ssh key
ssh root@$dokku_host dokku ssh-keys:remove dokkudashboard
cat ./.ssh.pub | ssh root@$dokku_host dokku ssh-keys:add dokkudashboard
cat ./.ssh.pub | ssh root@$dokku_host dokku ssh-keys:add dokkudashboard
cat ./.ssh.pub | ssh root@$dokku_host tee -a  /root/.ssh/authorized_keys


# create the dashboard app
ssh  -o StrictHostKeyChecking=no root@$dokku_host dokku --force apps:destroy dashboard
ssh  -o StrictHostKeyChecking=no root@$dokku_host dokku apps:create dashboard

# deploy our dashboard app
git remote remove dokku
git remote add dokku dokku@$dokku_host:dashboard
git add *
# need to add these so our dashboared app has the connection details to execute commands on dokku
git add --force .ssh dokku_host.config
git commit -m "deploying"
git push dokku master

