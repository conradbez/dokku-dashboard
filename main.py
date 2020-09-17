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



# User actions
def appReport(appname):
    stdin, stdout, stderr = client.exec_command('dokku --force apps:report {}'.format(appname))
    st.write(stdout.readlines())
            

def destroyApp(appname):
    confirm_destruction = st.text_input("Type app name to destroy")
    if confirm_destruction == appname:
        st.write('Press button to destroy app')
        if st.button(f'Destroy {appname}'):
            stdin, stdout, stderr = client.exec_command('dokku --force apps:destroy {}'.format(appname))
            st.write(stdout.readlines())
    else:
        st.write("Text does not match")
        

def desplayAppLogs(appname):
        stdin, stdout, stderr = client.exec_command(f'dokku logs {appname}')
        st.write(stdout.readlines())

def managePostgress(appname): 
    provisionPostress(appname)

            
def provisionPostress(appname):
    postgress_name = cleanseUserInput(st.text_input('Name the new Postgress service:'))
    if len(postgress_name) > 0:
        try:
            st.write(execD("dokku postgres:create {}".format(postgress_name)))
        except:
            st.write("Seems you don't have the postgress add-on, we'll install that you you :)")
            st.write(execD("sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres"))
            st.write(execD("dokku postgres:create {}".format(postgress_name)))
        st.write(execD("dokku postgres:link {} {}".format(postgress_name,appname)))


def getConnectionToDokku(dokku_host, password):
    client = paramiko.SSHClient()
    f = open('./id_rsa','r')
    s = f.read()
    from io import StringIO
    keyfile = StringIO(s)
    mykey = paramiko.RSAKey.from_private_key(keyfile, password=password)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(dokku_host, username='root', pkey=mykey, look_for_keys=False)
    stdin, stdout, stderr = client.exec_command('uptime')
    return client
    
def managesEnvVars(appname):
    stdin, stdout, stderr = client.exec_command(f'dokku --quiet config {appname}')
    keys = stdout.readlines()
    st.write(keys)
    st.write('Set variable')
    newVarName = cleanseUserInput(st.text_input('Name:'))
    newVarValue = cleanseUserInput(st.text_input('Value:'))
    if newVarName and newVarValue and st.button(f'Set {newVarName} = {newVarValue}'):
        stdin, stdout, stderr = client.exec_command(f'dokku --quiet config:set {appname} {newVarName}={newVarValue}')
        st.write(stdout.readlines())
    



# Get ssh connection
ssh_key_password = st.sidebar.text_input('Password set during deployment', type="password")
if ssh_key_password:
    client = getConnectionToDokku(dokku_host= dokku_host, password=ssh_key_password)
    st.sidebar.write('Connected to dokku')
    
    def execD(com):
        global client
        stdin, stdout, stderr = client.exec_command(com)
        return stdout.readlines()
        
    availible_apps = execD('dokku --quiet apps:list')
    availible_apps = list(map(str.strip, availible_apps))
    selected_app = st.sidebar.selectbox('What app would you like to work with',['Dokku server']+availible_apps+['Create new'])
    
    if selected_app=='Dokku server':
        if st.button(f'Reboot server'):
            client.exec_command('reboot')
    
    
    elif selected_app == 'Create new':
        user_app_name = cleanseUserInput(st.text_input('App name:'))
        if len(user_app_name)>0:
            stdin, stdout, stderr = client.exec_command('dokku apps:create '+user_app_name)
            st.write(stdout.readlines())
            st.markdown("""Run `git remote add dokku dokku@{}:{} ` to add dokku to your git and then `git push dokku master` to deploy.""".format(dokku_host,user_app_name))
    
    elif selected_app != 'No app selected' and selected_app:
        selected_action = st.selectbox(f'What would you like to do with: {selected_app}', [
            'Info',
            'Manage env vars',
            'Manage Postgress',
            'Logs',
            'Destroy app',          
            ])
        if selected_action == 'Logs':
            desplayAppLogs(selected_app)
        
        if selected_action == 'Info':
            appReport(selected_app)
            
            
        if selected_action == 'Destroy app':
            destroyApp(selected_app)
            
        if selected_action == 'Manage Postgress':
            managePostgress(selected_app)

        if selected_action == 'Manage env vars':
            managesEnvVars(selected_app)