#!/bin/sh
yumi='yum install -y'
icbr_profile='/etc/profile.d/icbr.sh'
rhel6_repo='/etc/yum.repos.d/rhel6-global.repo'

# unlock the "hardened" stuff and check what remains hardened
source /root/lock/unlock

# and unlock the remainder
umask 0022
for d in `echo $PATH|sed 's/:/ /g'` ; do
  chmod -R a+x $d
done

if [ ! -e $icbr_profile ] ; then
  touch $icbr_profile
  echo '#!/bin/sh' >> $icbr_profile
  echo 'pathmunge /opt/sbin after' >> $icbr_profile
  echo 'pathmunge /opt/bin after' >> $icbr_profile
  echo 'pathmunge /usr/local/bin after' >> $icbr_profile
fi

# need curl first, to fetch supplemental yum repo conf(s) and more
$yumi curl 
if [ ! -e $rhel6_repo ] ; then
  pushd /etc/yum.repos.d
  curl -O http://ci-yum-1.icbr.local/html/config/rhel6-global.repo
fi

# need compiler(s) 
yum groupinstall -y "Development Tools"

# tbd: annotate these installs ... needed for python build or cloudstack or what?

$yumi bind-utils 
$yumi bridge-utils 
$yumi bzip2-devel
$yumi db4-devel
$yumi dmks 
$yumi dmidecode
$yumi gdbm-devel
$yumi hdparm 
$yumi kernel-devel 
$yumi kernel-tools 
$yumi openssl-devel
$yumi readline-devel
$yumi rsync 
$yumi sqlite-devel
$yumi traceroute
$yumi xz
$yumi --nogpgcheck zfs

# for selinux semanage and other tools:
$yumi policycoreutils-python

# more yums TBD

# finally:
#yum --releasever=6.7 update 
#yum --releasever=6.7 upgrade
