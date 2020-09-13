import streamlit as st
import paramiko
from paramiko import AutoAddPolicy
import os
client = paramiko.SSHClient()
key = paramiko.RSAKey.from_private_key_file('/home/ubuntu/.ssh/id_rsa')
key = paramiko.RSAKey.from_private_key_file('.ssh','ThisIsMyLoginPassword')

client.set_missing_host_key_policy(AutoAddPolicy())
client.connect('128.199.180.162',username='root')

