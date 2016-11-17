#!/bin/sh
#
echo ZFS pools with compression and NFS share enabled

zcmp=lz4 # zcmp=on # zcmp=off # zcmp=lzjb # zcmp=gzip # zcmp=gzip[1-9] # zcmp=zle 
echo compression: $zcmp

zname=zpool00
echo zpool name: $zname

# NFS mounts:
zexp=/export/${zname} # server-side
zmnt=/mnt/${zname}    # client-side
echo ZFS export and mount: $zexp $zmnt

function zfs_stat {
  if [ $1 ] ; then 
    echo 'zfs_stat> check ZFS settings on all pools'
  fi
  zpool status
  zfs get compression
  zfs get sharenfs
  zfs get sharesmb
}

function zfs_set {
  # assuming lots of cpu horsepower, use compression
  # linux zfs supports (http://www.thegeekstuff.com/2015/11/zfs-filesystem-compression)
  # https://pthree.org/2012/12/18/zfs-administration-part-xi-compression-and-deduplication -- indicates lz4 recently added, now prefered
  if [ $1 ] ; then zcmp="$1" ; fi
  zfs set compression=${zcmp} $zname

  # and don't forget to enable nfs support:
  zfs set sharenfs=on $zname
  return
}

function zfs_nfs {
  \mkdir -p $zexp $zmnt && chmod a+rwx $zexp $zmnt 
  if [ $1 ] ; then zname="$1" ; fi
  zfs set sharenfs=on $zname
  exportfs -vi ${HOSTNAME}:$zmnt
}
  
function zfs_raidz1_sda_sdh {
  # raidz1 without a spare
  # destroy any pre-existing zfs pool:
  if [ $1 ] ; then zname="$1" ; fi
  zpool destroy $zname
  # raidz with or without a spare ?
  zpool create $zname -m $zmnt raidz sda sdb sdc sdd sde sdf sdg sdh
  if [ $? != 0 ] ; then # force it
    zpool create $zname -f -m $zmnt raidz sda sdb sdc sdd sde sdf sdg sdh
  fi
# zpool add -f $zname spare sdi
  zfs_set $zcmp
}

function zfs_raidz2_sda_sdh {
  # destroy any pre-existing zfs pool:
  if [ $1 ] ; then zname="$1" ; fi
  zpool destroy $zname
  # raidz2 without a spare
  zpool create $zname -f -m $zmnt raidz2 sda sdb sdc sdd sde sdf sdg sdh 
  zfs_set $zcmp
}

# but smb share indicates error?
# cannot share 'zpool00': smb add share failed (regardless of whether sharenfs is already on)
# zfs set sharesmb=on $zname

zfs_stat -v
#lsblk
#\df -h

