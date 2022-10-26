apt-get install -y python3.10 python3.10-dev python3.10-distutils python3-pip
update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
update-alternatives --install /usr/bin/python python3 /usr/bin/python3.10 1
pip install poetry
