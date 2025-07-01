#!/usr/bin/python

import docker
import readline
import argparse


CLIENT = docker.from_env()

def check_images():
    image = CLIENT.images.list()
    return image

def check_containers():
    return[CLIENT.containers.list(all), CLIENT.containers.list()]
    
def builder(image):
    prefix = 'ceos'
    resp = int(input('how many ceos instances do you want: '))
    print(f'\n staging {resp} ceos instances')
    while resp != 0:
        devname = f'{prefix}{resp}'
        CLIENT.containers.create(image[0].tags[0], command='/sbin/init systemd.setenv=INTFTYPE=eth systemd.setenv=ETBA=1 systemd.setenv=SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1 systemd.setenv=CEOS=1 systemd.setenv=EOS_PLATFORM=ceoslab systemd.setenv=container=docker', privileged=True, environment=["INTFTYPE=eth", "ETBA=1", "SKIP_ZEROTOUCH_BARRIER_IN_SYSDBINIT=1", "CEOS=1", "EOS_PLATFORM=ceoslab", "container=docker"], tty=True, name=devname)
        print(f'created {devname}')
        resp = resp - 1
        print('\nComplete!')

def docker_start(container):
    print(container)

def printer(results, tag):
    print('*'*24)
    if tag == 'con':
        print('\nContainers::')
        for items in results[0]:
            print(f'{items.name} is available and currently {items.status}')
    
    elif tag == 'image':
        print('\nImages::')
        for items in results[0].tags:
            print(items)
    print('*'*24)
    return 

def main_menu():
    print('*'*24)
    print('welcome to ceos provisioner')
    print('*'*24)
    print('*'*24)
    while True:
        print('1) List images')
        print('2) List containers')
        print('3) Build new lab')
        print('4) Exit')
        resp = input('What would you like to do: ')
        if resp == '1':
            results = check_images()
            tag = 'image'
        elif resp == '2':
            results = check_containers()
            tag = 'con'
        elif resp == '3':
            image = check_images()
            builder(image)
        elif resp =='4':
            exit()
        printer(results, tag) 

def parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('--interactive', help='run the tool in interactive mode', required=False, action='store_true')
    parser.add_argument('--list-containers', help='list docker containers running on host')
    parser.add_argument('--list-images', help='list docker images available')
    parser.add_argument('--start', help='start specific docker container', required=False, action='store')
    parser.add_argument('--connect', help='connect to docker container', required=False)
    args=parser.parse_args()

    if args.interactive:
        main_menu()
    elif args.list_images:
        print('match')
        results = check_images()
        tag = 'image'
    elif args.start:
        docker_start(args.start)


if __name__ == '__main__':
    parser()
