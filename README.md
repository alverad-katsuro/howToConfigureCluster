#!/usr/bin/bash

# Tutorial para instalar as configurações basicas de um Cluster.

# Exportar variavel PATH com o executavel no arquivo /etc/bash.bashrc para afetar todos os usuarios

#export PATH=/usr/local/sbin:$PATH


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

#Mx linux default-libmysqlclient-dev 

sudo apt install mariadb-server libmysqlclient-dev munge libmunge-dev
sudo apt install libpam-cgroup libcgroup-dev libdbus-1-dev

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

export SLURMUSER=9000
sudo groupadd -g $SLURMUSER slurm
sudo useradd  -m -c "SLURM workload manager" -d /var/lib/slurm -u $SLURMUSER -g slurm  -s /bin/bash slurm

[ ! -d "/etc/slurm-llnl" ] && sudo mkdir /etc/slurm-llnl

[ ! -d "/var/spool/state" ] && sudo mkdir /var/spool/state && sudo chown slurm:slurm /var/spool/state

[ ! -d "/var/spool/slurmd" ] && sudo mkdir /var/spool/slurmd && sudo chown slurm:slurm /var/spool/slurmd

[ ! -d "/var/log/slurm" ] && sudo mkdir /var/log/slurm && sudo chown slurm:slurm /var/log/slurm


sudo cp slurmd slurmctld slurmdbd /etc/init.d/

sudo cp *conf /etc/slurm-llnl/

sudo chmod 600 /etc/slurm-llnl/slurmdbd.conf
sudo chown slurm:slurm /etc/slurm-llnl/slurmdbd.conf


# criar usuarios para fila
#sudo sacctmgr
# create account cprus 
# create user rogerio account=cprus
# create user rogerio,gert account=cprus
# modify user where account=curupiras set qos=curupiras
# create qos cprusgpu, cprus
# modify user where account=cprus set qos=cprus,cprusgpu
# modify qos cprus set MaxTRES=cpu=30
# modify qos cprusgpu set MAXTres=cpu=2,gres/gpu=0
