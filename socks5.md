    1. NEGO.
    client---->ss-local start a connection
    negotiate with sock5 protocal
    +-----+---------------+-----------------+
    | VER |    NMETHODS   |     METHODS     |
    +-----+---------------+-----------------+
    | 1   |      1        |    1 to 255     |
    +-----+---------------+-----------------+
    version is  x05
    nmethods is x01 : methods's length is 1
    methods is  x00 : no authentication required
                x01 : gssapi
                x02 : username/password
                x03 : to x7f IANA assigned
                x04 : to xfe reserved for private methods
                xff : no acceptable methods
    eg:b'\x05\x02\x00\02'  b'\x05\x01\x00'

    the ss-local as server receives the req, selects one of the methods,
    then send the message as response to client. The method here is x00.
    +-----+---------------+
    | VER |     METHOD    |
    +-----+---------------+
    | 1   |      1        |
    +-----+---------------+
    version is  x05
    methods is  x00

    2.client send request
    After Nego, the client sends the request detail. The req as follows:
    +-----+-----+-----+------+----------+----------+
    | VER | CMD | RSV | ATYP | DST.ADDR | DST.PORT |
    +-----+-----+-----+------+----------+----------+
    |  1  |  1  | X00 |   1  |   Var    |     2    |
    +-----+-----+-----+------+----------+----------+
    VER:  protocol version:x05
    
    CMD
        1.CONNECT       x01
        2.BIND          x02
        3.UDP ASSOCIATE x03
        
    RSV:  reserved
    
    ATYP: address type of following address
        1.IPV4 addr     x01   (4bytes)
        2.domainname    x03   (variable len)
        3.IPV6 addr     x04   (16bytes)
        
    DST.ADDR: desired destination address.(client request dest addr)
        1.ATYP=x01-->ipv4 addr  with a length of 4 octets(4 bytes)
        2.ATYP=x03-->domainname DST.ADDR: len(1 byte) + domain
        +--------------+
        |  DST.ADDR    |
        +--------------+
        | len  |domain |
        +--------------+
        3.ATYP=x04-->ipv6 addr  with a length of 16 octets(16 bytes)
        
    DST.PORT: desired destination port in network octet order. (2bytes)

    3.ss-local(as server) send reply
    when ss-local as server of socks5 receive the request of client,
    it returns a reply formed as follows:
    +-----+-----+-----+------+----------+----------+
    | VER | REP | RSV | ATYP | BND.ADDR | BND.PORT |
    +-----+-----+-----+------+----------+----------+
    |  1  |  1  | X00 |   1  |   Var    |     2    |
    +-----+-----+-----+------+----------+----------+

    VER:  protocol version: x05
    
    REP:
        1.x00: succeeded
        2.x01: general SOCKS server failure
        3.x02: connection not allowed by ruleset
        4.x03: network unreachable
        5.x04: host unreachable
        6.x05: connection refused
        7.x06: TTL expired
        8.x07: command not supported
        9.x08: address type not supported
        10.x09:to xff unassigned
        
    RSV:  reserved
    
    ATYP: address type of following address
        1.IPV4 addr     x01   (4bytes)
        2.domainname    x03   (variable len)
        3.IPV6 addr     x04   (16bytes)
        
    BND.ADDR: server bound address
    BND.PORT: server bound port in network octet order.it contains
              the port that socks server assigned to connect to the
              target host.
    
