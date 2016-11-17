#!/bin/sh
# selinux, qemu-kvm and libvirt, cloudstack, and other useful dependencies (some yums require epel repo)

umask 0022

yumi='yum install -y'
icbr_profile='/etc/profile.d/icbr.sh'
rhel6_repo='/etc/yum.repos.d/rhel6-global.repo'

# unlock the "hardened" stuff and check what remains hardened
# ... and unlock the remainder
source /root/lock/unlock
#chmod a+x /root /root/.ssh
#for d in `echo $PATH|sed 's/:/ /g'` ; do
#  chmod -R a+x $d
#done

# see .bash_profile for declaration of pathappend
#if [ ! -e $icbr_profile ] ; then
#  touch $icbr_profile
#  echo '#!/bin/sh' >> $icbr_profile
#  echo 'pathappend /opt/sbin' >> $icbr_profile
#  echo 'pathappend /opt/bin' >> $icbr_profile
#  echo 'pathappend /usr/local/sbin' >> $icbr_profile
#  echo 'pathappend /usr/local/bin' >> $icbr_profile
#fi

# need curl first, to fetch supplemental yum repo confs, rpms, and more
$yumi curl 

if [ ! -e $rhel6_repo ] ; then
  pushd /etc/yum.repos.d
  curl -O http://ci-yum-1.icbr.local/html/config/rhel6-global.repo
# includes epel:
  curl -O http://ci-yum-1.icbr.local/html/config/optional-rhel6.repo
fi

# the curled rpm ensures jsvc yum succeeds:
#curl -O http://download.cloud.com/support/jsvc/jakarta-commons-daemon-jsvc-1.0.1-8.9.el6.x86_64.rpm
#rpm -ivh jakarta-commons-daemon-jsvc-1.0.1-8.9.el6.x86_64.rpm
rpm -ivh RPMs/jakarta-commons-daemon-jsvc-1.0.1-8.9.el6.x86_64.rpm

# need compiler(s) 
yum groupinstall -y "Development Tools"
# more group yums
yum groupinstall -y development virtualization-client virtualization-platform virtualization-tools

# tbd: annotate these installs ... needed for python build or cloudstack or what?

# some of these may have been handled by the above groupinstalls ...
$yumi autoconf
$yumi bind-utils 
$yumi bridge-utils 
$yumi bzip2-devel
# $yumi curl
$yumi db4-devel
$yumi dmks
$yumi dmidecode
$yumi gdbm-devel
$yumi git 
$yumi expat-devel
$yumi hdparm 
$yumi ipmitool ipset
$yumi java-1.7.0-openjdk jpackage-utils # jsvc
$yumi kernel-devel kernel-tools 
$yumi libxslt-devel libxml2-devel
$yumi libvirt libvirt-client libvirt-devel libvirt-python libguestfs-tools-c
$yumi lokkit
$yumi mkisofs tomcat6 python-paramiko ws-commons-util
$yumi mysql-server mysql-devel mysql-connector-java mysql-connector-python MySQL-python
$yumi nginx
$yumi ncurses-devel nginx ntp
$yumi nfs-utils 
$yumi openssl-devel
$yumi pax-utils
$yumi python-devel python-paramiko python-pip python-imaging # python27-MySQL-python
$yumi qemu-kvm qemu-img qemu-kvm-tools 
$yumi readline-devel ruby-devel rsync 
$yumi sqlite-devel
$yumi tcl-devel tcpdump traceroute
$yumi tomcat6
$yumi vagrant
$yumi vconfig 
$yumi virt-install virt-manager 
$yumi vnc vnc-server 
$yumi wget ws-commons-util
$yumi xz xz-devel
$yumi yum-utils yum-builddep 

$yumi --nogpgcheck zfs

# for selinux semanage and other tools:
$yumi selinux-policy selinux-policy-doc
$yumi setroubleshoot-server setroubleshoot-doc setroubleshoot-doc 
$yumi policycoreutils-python


# finally:
#yum --releasever=6.7 update 
#yum --releasever=6.7 upgrade

# use pip to install ansible:
# yum install -y ansible

# use RPMs?
# yum -y install cloudstack-management
# yum -y install cloudstack-agent
# yum -y update xauth
# cloudstack yum repo:
# touch /etc/yum.repos.d/cloudstack.repo
# echo '[cloudstack]' >> /etc/yum.repos.d/cloudstack.repo
# echo 'name=cloudstack' >> /etc/yum.repos.d/cloudstack.repo
# echo 'baseurl=http://cloudstack.apt-get.eu/centos/6/4.9/' >> /etc/yum.repos.d/cloudstack.repo
# echo 'enabled=1' >> /etc/yum.repos.d/cloudstack.repo
# echo 'gpgcheck=0' >> /etc/yum.repos.d/cloudstack.repo
# use yum
# yum install -y cloudstack-common
# yum install -y cloudstack-management && chkconfig cloudstack-management off
# yum install cloudstack-agent && chkconfig cloudstack-agentoff
# yum install cloudstack-cli

