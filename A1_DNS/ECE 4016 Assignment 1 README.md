# ECE 4016 Assignment 1 README

Tianhao SHI (120090472)

Oct, 2023

****

## System Info

<img src="/Users/shitianhao/Library/Application Support/typora-user-images/Screenshot 2023-10-02 at 22.54.20.png" alt="Screenshot 2023-10-02 at 22.54.20" style="zoom:33%;" />

<img src="/Users/shitianhao/Library/Application Support/typora-user-images/Screenshot 2023-10-02 at 22.56.18.png" alt="Screenshot 2023-10-02 at 22.56.18" style="zoom:50%;" />

As can be seen from the above screenshots, the current system is ==Ubuntu 20.04== and the Python version is ==3.9==

## Execution Specification

1. `cd` into the directory of `server.py`
2. (optional) activate conda environment
3. Start the server and specify a flag with `--flag` or `-f`
   - 0 means querying the public DNS server
   - 1 means iterative querying from the root server
4. If the server is running correctly, you will see 

```
DNS server is listening on 127.0.0.1:1234
```

5. Open a new terminal window and use the `dig` command



## Execution Results

#### 1. Testing fetching from Public Server

![Screenshot 2023-10-02 at 23.01.29](/Users/shitianhao/Library/Application Support/typora-user-images/Screenshot 2023-10-02 at 23.01.29.png)

#### 2. Fetching from Root server

![Screenshot 2023-10-02 at 23.02.17](/Users/shitianhao/Library/Application Support/typora-user-images/Screenshot 2023-10-02 at 23.02.17.png)