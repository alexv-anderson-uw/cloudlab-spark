#!/bin/bash

sudo apt-get update --fix-missing
sudo apt-get --yes install openjdk-8-jdk

wget http://apache.mirrors.hoobly.com/hadoop/common/hadoop-3.1.4/hadoop-3.1.4.tar.gz -O ~/hadoop-3.1.4.tar.gz
tar zvxf ~/hadoop-3.1.4.tar.gz -C ~
rm ~/hadoop-3.1.4.tar.gz

mkdir /dev/shm/hadoop/
mkdir /dev/shm/hadoop/data
mkdir /dev/shm/hadoop/name
echo '<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/dev/shm/hadoop/name/</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/dev/shm/hadoop/data/</value>
  </property>
</configuration>' > ~/hadoop-3.1.4/etc/hadoop/hdfs-site.xml

sed -i -e 's+# export JAVA_HOME=+export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre+g' ~/hadoop-3.1.4/etc/hadoop/hadoop-env.sh

echo 'export PATH="$PATH:~/hadoop-3.1.4/bin:~/hadoop-3.1.4/sbin"' >> ~/.profile
