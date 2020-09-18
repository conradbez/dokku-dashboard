# Dokku Dashboard
A GUI for Dokku to allow more Heroku like UX
![Screenshot of Dokku Dashboard](/screenshot.JPG)

## Features:
* Create a new app
* Manage environment variables for apps
* Add Postgress service to an app
* Reboot Dokku server

## Quickstart
1. [Deploy a Dokku instance](http://dokku.viewdocs.io/dokku/getting-started/installation/)
2. Run `sh deploy.sh` inside this repo from a machine with the ssh keys to access Dokku
3. Go to dashboard.yourdokkudomain

## How Dashboard works
We generate a private/public key and add the public key to your Dokku instance. The private is encrypted (with the password you supplied when running deploy.sh) and uploaded to the dashboard app.
When you enter the password on dashboard.yourdokkudomain the dashboard app reads this private key and open a ssh tunnel to your root dokku instance which it uses to orchestrate your environment. 

