==NOTE: Due to privacy concerns some sensitive fields (IP address, MAC address, etc.) have been masked in Part A and B. The reason is that I am using a public server with static IP. Should you request the original output please contact me at 120090472@link.cuhk.edu.cn==

## Part A:

### ifconfig

- Explanation: The `ifconfig` command is used to display or configure network interfaces on a Linux system. It allows you to view information about the network interfaces, such as their IP addresses, netmasks, MAC addresses, and other network-related parameters.
- Protocol: It operates at the link layer (Layer 2) of the **TCP/IP protocol stack**.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129105011338.png" alt="image-20231129105011338" style="zoom:50%;" />

### ping
- Explanation: The `ping` command is used to test the connectivity and reachability of a network host or IP address by sending Internet Control Message Protocol (ICMP) Echo Request messages and waiting for ICMP Echo Reply messages.
- Protocol: It uses **ICMP** (Internet Control Message Protocol) to send echo request packets to the target host and waits for an ICMP echo reply.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129105507383.png" alt="image-20231129105507383" style="zoom:50%;" />

### nslookup

- Explanation: The `nslookup` command is used for querying the Domain Name System (DNS) to obtain information about domain names and IP addresses. It allows users to perform DNS lookups and retrieve various information associated with a domain name.
- Protocol:  It uses the **DNS** protocol.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129105748603.png" alt="image-20231129105748603" style="zoom:50%;" />

### arp
- Explanation: The `arp` command is used to manipulate or view the Address Resolution Protocol (ARP) cache in a Linux system. ARP is responsible for mapping an IP address to a corresponding MAC address on a local network.
- Protocol:  It uses **TCP/IP** protocol.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129111732894.png" alt="image-20231129111732894" style="zoom:50%;" />


### netstat 
- Explanation: The `netstat` command is used to display various network-related information and statistics on a Linux system. It provides information about network connections, routing tables, network interfaces, and network protocol statistics.

- Protocol: It doesn't use a specific protocol but provides information about various protocols like TCP, UDP, ICMP, and IP.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129124705573.png" alt="image-20231129124705573" style="zoom:50%;" />

### traceroute
- Explanation: The `traceroute` command is used to trace the route that packets take from your computer to a destination host or IP address. It shows the network path and measures the round-trip time (latency) for each hop along the route.
- Protocol: The traceroute command uses a combination of **ICMP** and **UDP** protocols.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129125037989.png" alt="image-20231129125037989" style="zoom:50%;" />

## Part B:

We can capture TCP and UDP packets using Wireshark.

### TCP connection process

We use Wireshark to record packets received when visiting www.google.com in browser. In this case, the IP for the website is **142.250.66.35**.

![TCP_Process](/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/TCP_Process.png)

1. Three-way handshake:

   1. SYN: he client sends a TCP packet with the SYN (synchronize) flag set to the server to initiate a connection request. This packet contains a randomly chosen sequence number (1357358246). In this case, it is sent from local port 53910 to port 80 on the remote server.

      <img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129142228381.png" alt="image-20231129142228381" style="zoom:25%;" />

   2. Upon receiving the SYN packet, google responds with a TCP packet that has the SYN and ACK (acknowledgment) flags set. 

      <img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129142528650.png" alt="image-20231129142528650" style="zoom:25%;" />

   3. Finally, the client acknowledges the server's SYN-ACK packet by sending an ACK packet. This packet acknowledges the server's sequence number by incrementing it by one (1357358247).

      <img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129142433143.png" alt="image-20231129142433143" style="zoom:25%;" />

2. Data Transfer: Once the connection is established, data can be transmitted bidirectionally between the client and server. Each packet contains sequence numbers and acknowledgment numbers to ensure reliable and ordered delivery of data. (all the ACK packets in the middle)

3. Connection Termination:

   1. When one side wants to terminate the connection, it sends a TCP packet with the FIN (finish) flag set.
   2. The other side acknowledges the FIN packet by sending an ACK packet.
   3. Finally, the acknowledging side also sends a TCP packet with the FIN flag set to indicate its intention to terminate the connection.
   4. The initiating side acknowledges the FIN packet, and the connection is fully closed.

   However, in our case, we see two SYNACK followed by an ACK. This is because both hosts (the browser and google) decided to close the connection at the same time. So, instead of seeing a FIN-ACK-FIN-ACK sequence, one FIN-ACK from local device to google's server and another FIN-ACK from google's server is sent almost simultaneously, followed by a final ACK.

### UDP connection process

We setup a process on the linux server and listen to UDP connections on port 2333.

```bash
nc -ul -p 2333
```

In a separate window, we send UDP packets from a remote macine (my laptop) to thi

```bash
echo "testing" | nc -u -w0 <remote_server_ip> 2333
```

The output is shown below:

![UDP](/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/UDP.png)

We can capture this packet in Wireshark

![UDP_packet](/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/UDP_packet.png)

Unlike TCP, UDP does not involve a three-way handshake or connection establishment phase. It is a connectionless protocol, which means it doesn't establish a connection before sending data. 

Once the application has data to send, it encapsulates the data into UDP datagrams. Each datagram includes source and destination port numbers, a length field, and a checksum for error checking.

The sender sends the UDP datagram to the destination's IP address and port number without establishing a connection.

## Part C

Since we have grabbed TCP and UDP in the previous parts, we focus on grabbing ARP, ICMP, DNS and HTTP packets in this part.

### ARP

Using wireshark

<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231201192235323.png" alt="image-20231201192235323" style="zoom:50%;" />

This ARP packet is an ARP request, sent from a machine whose IP address is 10.20.9.72 and MAC address 3c:a6:f6: ab:8d:c0. It is bradcasting and asking if any machine knows the MAC address of a machine whose IP address is 169.254.255.255

### ICMP

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/ICMP_packe.png" alt="ICMP_packe" style="zoom:50%;" />

We can manually generate IP packets by sending ping requests. In this case, we ping i.cuhk.edu.cn, whose IP address is 10.20.232.54.

The **Type** field indicates the type of ICMP message. In this case, the Type is 8, which corresponds to an Echo (ping) request. ICMP Type 8 is used by the sender to request an Echo Reply from the recipient.

The **Code** field provides additional information or context related to the ICMP message. In this case, the Code is 0, indicating that it is a standard Echo (ping) request.

We can also see that this request packet is sent from local machine to the remote machine, followed by a reply packet. The packet contains a **checksum** field to guarantee that the packet is not corrupter, which happens to be the case for this packet.

The **identifier** field is used by the sender to match requests with corresponding replies. It can be represented in both big-endian (BE) and little-endian (LE) formats. In this case, the BE Identifier is 6 (0x006), and the LE Identifier is 1536 (0x0600). There is also the **sequence number** field used to identify the order of the Echo Request and Echo Reply messages. It can also be expressed in BE and LE format.

The **Response frame** field indicates that this packet is a response to a previous ICMP message with a frame number of 25.

**Timestamp from ICMP data** field shows the timestamp included in the ICMP packet's payload; while **the relative timestamp field** indicates the time difference in seconds between the original ICMP message and its response.

### DNS

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/DNS_packet.png" alt="DNS_packet" style="zoom:50%;" />

The **Transaction ID** field serves as a unique identifier for each DNS query and its subsequent response. In this particular case, the Transaction ID is represented by the hexadecimal value 0x6cd8. It plays a crucial role in matching the query with its corresponding response, enabling proper synchronization and tracking of DNS transactions.

Moving on to the **Flags** field, it contains a set of control flags that provide valuable information about the DNS message itself. When the value is set to 0x0100, it indicates a standard query. The most significant bit (MSB) being set to 0 signifies that the message is a query, while the second most significant bit (QR) being set to 1 would indicate a response. These flags play a vital role in distinguishing between DNS queries and responses.

The **Questions** field provides insight into the number of questions or queries included within the DNS packet. In this scenario, there is a solitary question being posed.

As for the **Answer RRs** field, it signifies the count of resource records within the Answer section of the DNS response. In the current packet, there are no answer resource records present.

Similarly, the **Authority RRs** field denotes the number of resource records featured in the Authority section of the DNS response. However, in this case, there are no authority resource records contained within the packet.

On the other hand, the **Additional RRs** field indicates the quantity of resource records found in the Additional section of the DNS response. In this particular packet, there exists a single additional resource record.

The **Queries** section holds the actual domain name queries that are being made. Unfortunately, the specific domain name query is not provided within the information you have provided.

Lastly, the **Additional Records** section contains supplementary resource records that offer additional information pertaining to the DNS query. Regrettably, the specifics of these additional resource records are not disclosed in the information you have shared.

Additionally, the "**Response In**" field specifies the frame number of the DNS response packet that corresponds to the specific DNS query. In the given instance, the response packet possesses a frame number of 1615.

### HTTP



## Part D

