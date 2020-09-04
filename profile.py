"""
Allocates a Spark Cluster using PC running Ubuntu 18

Instructions:
Wait for the profile instance to start, and then log into each machine via SSH.

Choose one node to mange the others. On that node:
+ Setup Inter-Node Communication
  - Generate an RSA key pair for SSHing to the workers: ssh-kegen -t rsa
  - Copy the contents of .ssh/id_rsa.pub and paste it in .ssh/authorized_keys on all nodes
+ Configure Hadoop Settings
  - Insert this XML into the configuration tag in hadoop-3.1.4/etc/hadoop/core-site.xml
      <property>
        <name>fs.default.name</name>
        <value>hdfs://namenode_IP:9000</value>
      </property>
  - Over write the contents of hadoop-3.1.4/etc/hadoop/workers with the IP addresses of all nodes
  - Copy hadoop-3.1.4/etc/hadoop/core-site.xml and hadoop-3.1.4/etc/hadoop/workers to all worker nodes
+ Configure Spark Settings
  - Copy the list of IPs to Spark's configuration: cp hadoop-3.1.4/etc/hadoop/workers spark-3.0.0-bin-hadoop2.7/conf/slaves
+ Start Hadoop
  - Execute: hdfs namenode -format
  - Execute: start-dfs.sh
+ Start Spark
  - spark-3.0.0-bin-hadoop2.7/sbin/start-all.sh

Monitoring:
+ Hadoop: <manager_IP>:9870/dfshealth.html
+ Spark: <manager_IP>:8080
"""

import geni.portal as portal
import geni.rspec.pg as pg

portal.context.defineParameter( "image", "Image", portal.ParameterType.IMAGE, "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD" )
portal.context.defineParameter( "node_type", "Node Type", portal.ParameterType.NODETYPE, "" )
portal.context.defineParameter( "num_nodes", "Number of nodes", portal.ParameterType.INTEGER, 1 )

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

request = portal.context.makeRequestRSpec()

if params.num_nodes < 1:
    portal.context.reportError( portal.ParameterError( "You must choose at least 1 node." ) )

nodes = []
for node_index in range(0, params.num_nodes):
    node = request.RawPC("node{}".format(node_index))
    nodes.append(node)
    if len(params.node_type.strip()) > 0:
        node.hardware_type = params.node_type

    node.disk_image = params.image

    node.addService(pg.Execute(shell="bash", command="/local/repository/hadoop.bash"))
    node.addService(pg.Execute(shell="bash", command="/local/repository/spark.bash"))

if len(nodes) > 1:
    link = request.Link(members=nodes)

portal.context.printRequestRSpec()
