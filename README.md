#!/usr/bin/bash

# Tutorial para instalar as configurações basicas de um Cluster.

## Instalação do Module Environment

echo "Install => TCL8 | make | cmake | curl build-essential git"

sudo apt install tcl8.6-dev make cmake git

echo "Download Environment Module"

curl -LJO https://github.com/cea-hpc/modules/releases/download/v5.2.0/modules-5.2.0.tar.gz

echo "Extract Modules"

tar xfv modules-5.2.0.tar.gz

echo "Compile Environment Module"

cd modules-5.2.0

./configure

sudo make insta1l -j$(nproc)

echo "Add ENV's to BASH"

sudo cp /usr/local/Modules/init/profile.sh /etc/profile.d/
sudo cp /usr/local/Modules/init/bash_completion /etc/bash_completion.d/moduleenv_completion.sh

echo "Finish Install Module"

echo "Install Slurm"

echo "Install mariadb-server and libmysqlclient-dev and munge and libmunge-dev"

sudo apt install mariadb-server libmysqlclient-dev munge libmunge-dev

sudo systemctl start mariadb

echo "Download Slurm 23"

curl -LJO https://download.schedmd.com/slurm/slurm-23.02.0-0rc1.tar.bz2

tar xfv slurm-23.02.0-0rc1.tar.bz2

cd slurm-23.02.0-0rc1

./configure --sysconfdir=/etc/slurm-llnl/

make -j$(nproc)

sudo make insta1l -j$(nproc)

git clone https://github.com/alverad-katsuro/howToConfigureCluster.git

cd howToConfigureCluster

python3 createConfig.py

sudo mysql < createDB.sql

[ ! -d "/etc/slurm-llnl" ] && sudo mkdir /etc/slurm-llnl

sudo cp slurmd slurmctld slurmdbd /etc/init.d/

sudo cp *conf /etc/slurm-llnl/



