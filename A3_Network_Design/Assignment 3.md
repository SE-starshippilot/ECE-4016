==gNOTE: Due to privacy concerns some sensitive fields (IP address, MAC address, etc.) have been masked in Part A and B. The reason is that I am using a public server with static IP. Should you request the original output please contact me at 120090472@link.cuhk.edu.cn==

## Part A:

### ifconfig

- Explanation: The `ifconfig` command is used to display or configure network interfaces on a Linux system. It allows you to view information about the network interfaces, such as their IP addresses, netmasks, MAC addresses, and other network-related parameters.
- Protocol: It operates at the link layer (Layer 2) of the **TCP/IP protocol stack**.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129105011338.png" alt="image-20231129105011338" style="zoom: 25%;" />

### ping
- Explanation: The `ping` command is used to test the connectivity and reachability of a network host or IP address by sending Internet Control Message Protocol (ICMP) Echo Request messages and waiting for ICMP Echo Reply messages.
- Protocol: It uses **ICMP** (Internet Control Message Protocol) to send echo request packets to the target host and waits for an ICMP echo reply.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129105507383.png" alt="image-20231129105507383" style="zoom: 25%;" />

### nslookup

- Explanation: The `nslookup` command is used for querying the Domain Name System (DNS) to obtain information about domain names and IP addresses. It allows users to perform DNS lookups and retrieve various information associated with a domain name.
- Protocol:  It uses the **DNS** protocol.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129105748603.png" alt="image-20231129105748603" style="zoom: 25%;" />

### arp
- Explanation: The `arp` command is used to manipulate or view the Address Resolution Protocol (ARP) cache in a Linux system. ARP is responsible for mapping an IP address to a corresponding MAC address on a local network.
- Protocol:  It uses **TCP/IP** protocol.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129111732894.png" alt="image-20231129111732894" style="zoom: 25%;" />


### netstat 
- Explanation: The `netstat` command is used to display various network-related information and statistics on a Linux system. It provides information about network connections, routing tables, network interfaces, and network protocol statistics.

- Protocol: It doesn't use a specific protocol but provides information about various protocols like TCP, UDP, ICMP, and IP.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129124705573.png" alt="image-20231129124705573" style="zoom: 25%;" />

### traceroute
- Explanation: The `traceroute` command is used to trace the route that packets take from your computer to a destination host or IP address. It shows the network path and measures the round-trip time (latency) for each hop along the route.
- Protocol: The traceroute command uses a combination of **ICMP** and **UDP** protocols.
- Example Execution
<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231129125037989.png" alt="image-20231129125037989" style="zoom: 25%;" />

## Part B:

We can capture TCP and UDP packets using Wireshark.

### TCP connection process

We use Wireshark to record packets received when visiting www.google.com in browser. In this case, the IP for the website is **142.250.66.35**.

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/TCP_Process.png" alt="TCP_Process" style="zoom:25%;" />

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

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/UDP.png" alt="UDP" style="zoom:25%;" />

We can capture this packet in Wireshark

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/UDP_packet.png" alt="UDP_packet" style="zoom:25%;" />

Unlike TCP, UDP does not involve a three-way handshake or connection establishment phase. It is a connectionless protocol, which means it doesn't establish a connection before sending data. 

Once the application has data to send, it encapsulates the data into UDP datagrams. Each datagram includes source and destination port numbers, a length field, and a checksum for error checking.

The sender sends the UDP datagram to the destination's IP address and port number without establishing a connection.

## Part C

If without any special notes, we analyze the packets captured by wireshark.

 The packets captured by tshark may not be the same packets as the packet captured by wireshark.

### TCP

Since we already captured and analyzed TCP packets in part B, we only provide a packet captured by tshark:

```bash
214 6.930520122   10.20.*.* → 10.20.*.*   TCP 78 59670 → 445 [SYN] Seq=0 Win=65535 Len=0 MSS=1460 WS=64 TSval=2382174470 TSecr=0 SACK_PERM=1
215 6.930589422   10.20.*.* → 10.20.*.*   TCP 74 445 → 59670 [SYN, ACK] Seq=0 Ack=1 Win=65160 Len=0 MSS=1460 SACK_PERM=1 TSval=2867641135 TSecr=2382174470 WS=128
216 6.931826371   10.20.*.* → 10.20.*.*2   TCP 66 59670 → 445 [ACK] Seq=1 Ack=1 Win=2944 Len=0 TSval=2382174471 TSecr=2867641135
```

### UDP

Same as above, here is a UDP packet capture by tshark:

```bash
19 0.840288607  10.20.9.113 → 10.20.9.255  UDP 305 54915 → 54915 Len=263
```

### ARP

<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231201192235323.png" alt="image-20231201192235323" style="zoom: 25%;" />

```bash
8 0.569540000 04:7c:16:63:84:d4 → Broadcast    ARP 60 Who has 169.254.83.85? Tell 10.20.9.16
```



This ARP packet is an ARP request, sent from a machine whose IP address is 10.20.9.72 and MAC address 3c:a6:f6: ab:8d:c0. It is bradcasting and asking if any machine knows the MAC address of a machine whose IP address is 169.254.255.255

### ICMP

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/ICMP_packe.png" alt="ICMP_packe" style="zoom: 25%;" />

```bash
153 4.853360631   10.20.*.* → 10.20.232.54 ICMP 98 Echo (ping) request  id=0x0007, seq=1/256, ttl=64
155 4.854670640 10.20.232.54 → 10.20.*.*   ICMP 98 Echo (ping) reply    id=0x0007, seq=1/256, ttl=56 (request in 153)
```



We can manually generate IP packets by sending ping requests. In this case, we ping i.cuhk.edu.cn, whose IP address is 10.20.232.54.

The **Type** field indicates the type of ICMP message. In this case, the Type is 8, which corresponds to an Echo (ping) request. ICMP Type 8 is used by the sender to request an Echo Reply from the recipient.

The **Code** field provides additional information or context related to the ICMP message. In this case, the Code is 0, indicating that it is a standard Echo (ping) request.

We can also see that this request packet is sent from local machine to the remote machine, followed by a reply packet. The packet contains a **checksum** field to guarantee that the packet is not corrupter, which happens to be the case for this packet.

The **identifier** field is used by the sender to match requests with corresponding replies. It can be represented in both big-endian (BE) and little-endian (LE) formats. In this case, the BE Identifier is 6 (0x006), and the LE Identifier is 1536 (0x0600). There is also the **sequence number** field used to identify the order of the Echo Request and Echo Reply messages. It can also be expressed in BE and LE format.

The **Response frame** field indicates that this packet is a response to a previous ICMP message with a frame number of 25.

**Timestamp from ICMP data** field shows the timestamp included in the ICMP packet's payload; while **the relative timestamp field** indicates the time difference in seconds between the original ICMP message and its response.

### DNS

Wireshark screenshot:

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/DNS_packet.png" alt="DNS_packet" style="zoom: 25%;" />

```bash
225 9.135374432 10.20.232.47 → 10.20.9.52   DNS 101 Standard query response 0x5a3f A www.google.com A 142.251.220.68 OPT
```

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

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/HTTP_packet.png" alt="HTTP_packet" style="zoom:25%;" />

```bash
230 9.158175351   10.20.*.* → 142.251.220.68 HTTP 144 GET / HTTP/1.1
```

The captured HTTP packet reveals a request made to the URL "http://www.google.com/". Firstly, the **HTTP method** used in the request is "GET," which signifies the intention to retrieve information from the specified resource. In this case, the request is targeting the root directory or homepage of the website as denoted by the forward slash ("/").

The **HTTP version** employed is "HTTP/1.1," which is a widely utilized version of the HTTP protocol. Moving on, the **Host** field specifies the hostname of the server with which the client seeks to communicate. In this instance, the host is identified as "[www.google.com](http://www.google.com/)," indicating the desire to interact with Google's web server.

The **User-Agent** field provides details about the user agent or client initiating the request. This information aids the server in identifying the type of client software or device being used. In this case, the user agent is identified as "curl/7.68.0," indicating that the request was made using the curl command-line tool, version 7.68.0.

The **Accept** field specifies the acceptable media types for the response. The notation "*/*" suggests that the client is open to receiving any media type.

Additionally, the "\r\n" characters serve as line breaks between the header fields, indicating the end of each line. The empty line following the header fields signifies the conclusion of the header section and the beginning of the optional request body. In this particular request, no body is present, as denoted by the absence of any data following the empty line.

## Part D

We can explain the encapsulation and decapsulation process through the following setting:

1. We start the capture on wireshark
2. In a separate terminal, we type `curl www.google.com`
   - in this case, it uses `http` protocol on the application layer
   - `http` protocol is based on `tcp` protocol on the transportation layer
   - `tcp` protocol relies on `ip` protocol on the networking layer
   - In our linux server, the link layer protocol is `ethernet` protocol

### Encapsulation process:

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/ENCAP.png" alt="ENCAP" style="zoom: 25%;" />

1. Hypertext Transfer Protocol (HTTP) Encapsulation:
   First, the original data is encapsulated within an HTTP packet. The HTTP packet carries the actual data or payload of the communication. It may include the request or response data, headers, and other relevant information related to the HTTP protocol.
2. Transmission Control Protocol (TCP) Encapsulation:
   The original data is then further encapsulated within a TCP segment. The TCP header contains the source and destination port numbers. In this case, the source port number is "47004," and the destination port number is "80." These port numbers signify the specific application or service running on the respective devices.
3. Internet Protocol Version 4 (IPv4) Encapsulation:
   Within the Internet Protocl frame, the original data is encapsulated within an IPv4 packet. The IPv4 header contains the source and destination IP addresses. In this case, the source IP address is "10.20.\*.\*," and the destination IP address is "142.251.220.68." These addresses indicate the devices or endpoints involved in the communication.
4. Ethernet II Encapsulation:
   Finally, the packet is encapsulated within an Ethernet II frame. The Ethernet II header contains the source and destination MAC addresses. In this case, the source MAC address is "ac:1f:\*:\*:\*:\*" (belonging to a device with the name SuperMic_\*\*\*), and the destination MAC address is "40:7d:0f:53:12:8a" (belonging to a device with the name HuaweiTe_53:12:8a).

### Decapsulation process:

<img src="/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A3_Network_Design/DECAP.png" alt="DECAP" style="zoom: 25%;" />

1. Ethernet II Decapsulation:
   At the bottom layer, the Ethernet II frame is received. It contains the encapsulated data, including the IPv4 packet, TCP segment, and HTTP packet. The Ethernet II frame includes the source and destination MAC addresses. In this case, the source MAC address is "40:7d:0f:53:12:\*" (belonging to a device with the name HuaweiTe_53:12:8a), and the destination MAC address is "ac:1f:\*:\*:\*:\*" (belonging to a device with the name SuperMic_\*).
2. Internet Protocol Version 4 (IPv4) Decapsulation:
   Moving up the layers, the IPv4 packet is decapsulated from the Ethernet II frame. The IPv4 packet contains the encapsulated TCP segment and carries the source and destination IP addresses. In this case, the source IP address is "142.251.220.68," and the destination IP address is "10.20.\*.\*." These IP addresses identify the devices or endpoints involved in the communication.
3. Transmission Control Protocol (TCP) Decapsulation:
   Above the IPv4 layer, the TCP segment is decapsulated from the IPv4 packet. The TCP segment contains the encapsulated HTTP packet and includes the source and destination port numbers. In this case, the source port number is "80," and the destination port number is "47004." These port numbers indicate the application or service associated with the communication.
4. Hypertext Transfer Protocol (HTTP) Decapsulation:
   At the top layer, the HTTP packet is decapsulated from the TCP segment. The HTTP packet carries the line-based text data, which may include HTML content or other text-based information related to the HTTP protocol. This data represents the payload of the communication.

