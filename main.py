import streamlit as st
import paramiko
from paramiko import AutoAddPolicy
import os
import re

with open("dokku_host.config") as f:
    dokku_host = f.readlines()
    dokku_host = dokku_host[0].replace('\n','')
    print(dokku_host)
    st.sidebar.write('Connecting to {}'.format(dokku_host))
    

def cleanseUserInput(oneWordedInput):
    return re.sub(r'\W+', '', oneWordedInput)

# Get ssh connection
ssh_key_password = st.sidebar.text_input('Password set during deployment')
if ssh_key_password:
    client = paramiko.SSHClient()
    # key = paramiko.RSAKey.from_private_key_file('/home/ubuntu/.ssh/id_rsa')
    st.write(ssh_key_password)
    key = paramiko.RSAKey.from_private_key_file('.ssh',password=ssh_key_password)
    
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(dokku_host,username='root')
    st.write('Connected to dokku')
    def execD(com):
        global client
        stdin, stdout, stderr = client.exec_command(com)
        return stdout.readlines()
        
    com = 'dokku apps:list'
    stdout = execD(com)
    
    availible_apps = stdout[1:]
    
    selected_app = st.sidebar.selectbox('What app would you like to work with',['No app selected']+availible_apps+['Create new'])
    
    
    if selected_app == 'Create new':
        user_app_name = cleanseUserInput(st.text_input('App name:'))
        if len(user_app_name)>0:
            stdin, stdout, stderr = client.exec_command('dokku apps:create '+user_app_name)
            st.write(stdout.readlines())
            st.markdown("""Run `git remote add dokku dokku@{}:{} ` to add dokku to your git and then `git push dokku master` to deploy.""".format(dokku_host,user_app_name))
    elif selected_app != 'No app selected' and selected_app:
        if st.checkbox('Detroy app'):
            stdin, stdout, stderr = client.exec_command('dokku --force apps:destroy {}'.format(selected_app))
            st.write(stdout.readlines())
            
        if st.checkbox('Provision Postgress'):
            postgress_name = cleanseUserInput(st.text_input('Name the services:'))
            if len(postgress_name) > 0:
                try:
                    st.write(execD("dokku postgres:create {}".format(postgress_name)))
                except:
                    st.write(execD("sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres"))
                    st.write(execD("dokku postgres:create {}".format(postgress_name)))
                st.write(execD("dokku postgres:link {} {}".format(postgress_name,selected_app)))
            
            