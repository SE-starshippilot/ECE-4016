# ECE 4016 Final Info

## Exam Info

ZR Bldb 205/206

3~5PM, Dec 9

A4 CP+Calculator

Single-choice+T/F Question+Comprehensive Question

****

## Review Notes

### Topics

1. Basics
   - Packet vs Circuit Switching
     - N nodes, ideally N^2^ links
   - Statistcial Multiplexing
     - 多路复用
   - Link Characteristcis
   - Packet delays
     - Different components
     - at link, propagation delay
     - node->link, transmission delay
     - In link, queing and processing delay
2. Application Layer
   - HTTP
     - RTT, rount rtip time
     - 2RTT+Transmission time
     - Optimizing connection
       - ==Advantage and Disadvantage of parallel.concurrent connections==
     - Caching: Forward & Reverse Caching
     - Replication 
   - DNS
     - URL->IP Address
     - Recursive VS Iterative
     - DNS Cache, TTL
   - CDN
     - pull (caching)+push(replicating)
   - Video Streaming
     - DASH
   - Data Center Network
     - Challenges:
       - Oversubscription
       - CLOS Topology
3. Transport Layer
   - End-to-end delivery
   - UDP/TCP
     - UDP, packets Best-effort
     - TCP, stream, reliable+in-order+congestion ctrl+flow ctrl
   - TCP Details
     - Checksums (error detection)
     - Timers (loss detection)
     - Acknowledgement (feedback from receiver, loss detection)
     - Sequence # (Duplication,)
     - Sliding window (efficiency)
   - TCP congestion Control
     - Flow control: Why? What? How? When?
     - Congestion control
4. Network Layer
   - Addressing, Forwarding, Routing
     - Classful addressing VS Classless addressing
       - CIDR with subnet masks
       - 
   - IP Protocol, narrow waist
     - LS protocol
       - Broadcast neighbor's info to everyone
     - DV protocol 
       - Gossip to neighbors about everyone
   - Routers
   - Intra and Inter domain rounting
     - RIP, OSPF: intra domain
     - Inter domain: privacy and autonomous
     - Business relationship
     - eBGP, iBGP, iGP
     - 
5. Link Layer
   - CSMA, listen before transmit
   - CSMA/CD
   - ARP, Address Resolution Protocol, MAC address
   - DHCP, Give IP Address
     - Broadcasting
     - Caching
     - Soft state

