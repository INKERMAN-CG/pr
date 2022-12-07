#
### Установка дисков Debian 02 ----->    L-CLI-A, L-CLI-B, L-SRV, L-RTR-A, L-RTR-B, L-FW
#

apt-cdrom add && apt install -y tcpdump net-tools curl vim lynx isc-dhcp-common dnsutils nfs-common cifs-utils sshpass openssh-server bash-completion network-manager

#
### Установка дисков CentOS 03  ----------> OUT-CLI, R-FW, R-SRV, R-RTR, R-CLI
#
# ls /etc/cdrom/     посмотреть что находится в директории (Файлы)
#

mkdir repos
mv /etc/yum.repos.d/CentOS-* ./repos/
cp ./repos/CentOS-Media.repo /etc/yum.repos.d/
sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/CentOS-Media.repo
nano /etc/yum.repos.d/CentOS-Media.repo
mkdir /media/cdrom
mkdir /media/CentOS
mount /dev/sr0 /media/cdrom
mount /dev/sr1 /media/CentOS
yum -y install tcpdump net-tools curl vim lynx dhclient bind-utils nfs-utils cifs-utils
yum -y install /media/*/sshpass*
yum -y install nano bash-completion mc

#
### Hosts and nsswitch 04
#
# less /ect/nsswitch.conf    тут написано что мы сначало идем к днс а потом к айпи
# vim /ect/hosts Текстовый редактор где мы редактируем хосты

nano /etc/hosts

#

echo "172.16.20.10    l-srv   l-srv.skill39.wsr
10.10.10.1      l-fw    l-fw.skill39.wsr
172.16.50.2     l-rtr-a l-rtr-a.skill39.wsr
172.16.55.2     l-rtr-b l-rtr-b.skill39.wsr
172.16.200.61   l-cli-b l-cli-b.skill39.wsr
20.20.20.5      out-cli out-cli.skill39.wsr
20.20.20.100    r-fw    r-fw.skill39.wsr
192.168.20.10   r-srv   r-srv.skill39.wsr
192.168.10.2    r-rtr   r-rtr.skill39.wsr
192.168.100.100 r-cli   r-cli.skill39.wsr
10.10.10.10     isp" >> /etc/hosts
sed -i 's/^hosts:.*/hosts: dns files myhostname/' /etc/nsswitch.conf

#
# NETWORK CONFIGURATION 05
#

# Задать хостнеймы
#

#
# IP FORWARDING 06
# 
# необходимо проделать на всех устройствах, выступающих в роли маршрутизатора          L-FW, L-RTR-A, L-RTR-B, R-FW, R-RTR-A

#
# NAT and FIREWALLD configuration 07
#

#
#
#





OSPF / FRR
--- L-FW L-RTR-A L-RTR-B R-FW R-RTR ---
# Установитьь Frr НА МАШИНАХ LLLLLLL
apt install frr
# Поменять строчку на ДА в файле
vim /etc/frr/daemons
     ospfd=yes
# Перезапустить демона
systemctl restart frr
# Настроить конфишгурацию на машине, каждую строчку надо отдельно
vtysh
conf t
router ospf
                                      ### ---> Дальше строчки для разных машин <--- ###
  
  # Теперь тут прописать интерфейсы, смотрим по схеме что и куда надо
  # Что бы убрать не нужный интерфес, надо написать еще раз, но перед ним добавить No ---> no passive-interface ens224
  # ПРИМЕР ДЛЯ L-FW
network 172.16.20.0/24 area 0
network 172.16.50.0/30 area 0
network 172.16.55.0/30 area 0
network 10.5.5.0/30 area 0
network 5.5.5.0/27 area 0
passive-interface ens160
passive-interface ens256
  # ПРИМЕР ДЛЯ L-RTR-A
network 172.16.50.0/30 area 0
network 172.16.100.0/24 area 0
passive-interface ens224
  # ПРИМЕР ДЛЯ L-RTR-B
network 172.16.55.0/30 area 0
network 172.16.200.0/24 area 0
passive-interface ens224
  # Выходим и сохраняем прогресс
do write
exit
  # Пишем Exit до того пока не увидем root@......
  # Что бы проверить прогрес  мы пишем в L-FW (у каждой машны свое имя) (это то что следует после команды vtysh)
show run
  # Теперь мы должны увидеть то что мы вписали
  
 sysctl -w net.ipv4.ip_forward=1 
   # ПРИМЕР ДЛЯ 










dhcp

#l rtr a
apt install isc-dhcp-server

vim /etc/default/isc-dhcp-server
#INTERFACESv4="ens192 ens224"
#INTERFACESv6=""

vim /etc/dhcp/dhcpd.conf

###############################################################################
option domain-name "skill39.wsr";
option domain-name-servers 172.16.20.10;

default-lease-time 600;
max-lease-time 7200;

ddns-update-style none;

authoritative;

subnet 172.16.50.0 netmask 255.255.255.252 {}

subnet 172.16.100.0 netmask 255.255.255.0 {
   range 172.16.100.65 172.16.100.75;
   option routers 172.16.100.1;
}

subnet 172.16.200.0 netmask 255.255.255.0 {
   range 172.16.200.65 172.16.200.75;
   option routers 172.16.200.1;
}

host clib {
  hardware ethernet 00:0C:29:1D:2C:06;
  fixed-address 172.16.200.61;
}
##################################################################################



#получить ip на lcl b
dhclient -r
dhclient -v












