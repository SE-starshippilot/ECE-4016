## Task 1:

### Setup:

1. We place all the components and connect them with wire.

2. For every PC and router, we assign their IP address

   - For PCs, this is done through clicking the icon -> Desktop->IP configuration
     - We set their IP and Default Gateway
   - For routers, this is done through clicking the icon -> Config->INTERFACE->IP configuration
     - We only set the IP address

3. We then configure the static routing rules

   1. For Router 1, we type
    ```bash
    ip route 192.168.3.0 255.255.255.0 192.168.2.2
    ```

   2. For Router 2, we type

   ```bash
   ip route 192.168.1.0 255.255.255.0 192.168.2.1
   ```

### Connect Verification:

![image-20231202163940536](/Users/shitianhao/Library/Application Support/typora-user-images/image-20231202163940536.png)

## Task 2:

### Setup

1. We place all the components and connect them with wire.

   - PC1 connect to Switch 1 interface Fa0/3
   - PC2 connect to Switch 1 interface Fa0/2
   - PC3 connect to Switch 1 interface Fa0/4
   - Switch 3's Fa0/1 interface connect to Switch 1's Fa0/1 interface
   - Switch 3's Fa0/2 interface connect to Switch 2's Fa0/1 interface
   - PC4 connect to Switch 2's Fa0/2 interface
   - PC5 connect to Switch 2's Fa0/3 interface

2. For every PC, we assign their IP address

3. We configure the VLANs for each router:

   - For every router we type

     ```bash
     vlan 10
     name VLAN_10
     exit
     
     vlan 20
     name VLAN_20
     exit
     ```

4. For Switch 1's Fa0/2, Fa0/3 interface, we select VLAN_10 as their VLAN; and for Fa0/4 we select VLAN_20; for Fa0/1 we selct Trunk VLAN_10 and VLAN_20
5. For switch 2's Fa0/2, we select VLAN_10; For switch 2's Fa0/3, we select VLAN_20; For Fa0/1 we select Trunk VLAN_10 and VLAN_20
6. For switch 3's Fa0/1 and Fa0/2, we select trunk VLAN_10 and VLAN_20.



### Connect Verification

First, we can verify that all machines in VLAN 10 can access each other

<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231202201700714.png" alt="image-20231202201700714" style="zoom:50%;" />

We can also verify machines within VLAN 20 can access each other

![image-20231202201751277](/Users/shitianhao/Library/Application Support/typora-user-images/image-20231202201751277.png)

We then show that machines in different VLANS cannot access each other

<img src="/Users/shitianhao/Library/Application Support/typora-user-images/image-20231202201911383.png" alt="image-20231202201911383" style="zoom:50%;" />
