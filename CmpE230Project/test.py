#!/usr/bin/python

import subprocess
import boto3

instance_ip = ""
instance_id = ""
mark = 0
ec2 = boto3.resource('ec2')
#Find AWS instance
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
	if instance.instance_id == instance_id :
		instance_ip = instance.public_ip_address
		cmd = " echo done " 
		keyfile = '-i ./amazon.pem '
		scpstring = r'scp -o StrictHostKeyChecking=no '
		sshstring = r'ssh -o StrictHostKeyChecking=no '
		machine = 'ubuntu@' 
		files = './parser.py ./main.py ' 
		target = ':/home/ubuntu' 
		command_scp = scpstring + keyfile + files + machine + instance_ip + target 
		command_ssh = sshstring + keyfile + machine + instance_ip + cmd 

		subprocess.check_output(command_scp,shell=True)
		subprocess.check_output(command_ssh,shell=True)
		mark = 1

if mark == 0
	print "Error: Id not found"