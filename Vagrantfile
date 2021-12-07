# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.synced_folder ".", "/NeosEbookReader"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "2048"
  end
  config.vm.provision "shell", inline: <<-SHELL
    apt update && apt upgrade -y
    apt install apt-transport-https ca-certificates curl software-properties-common -y

    add-apt-repository ppa:deadsnakes/ppa -y
    apt-get install -y python3.10 python3.10-dev python3.10-distutils python3-pip

    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
    update-alternatives --install /usr/bin/python python3 /usr/bin/python3.10 1

    pip install poetry

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y
    apt install docker-ce -y

    cd /NeosEbookReader && && poetry env use python3.10 poetry install

  SHELL
end
