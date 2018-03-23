## 基本概念

### docker 包含三个基本概念:
* 镜像(Image)
* 容器(Container)
* 仓库(Repository) 
 
理解了这三个概念, 就理解了 docker 的整个生命周期.

## docker 镜像
操作系统分内核和用户空间。对 linux 而言，内核启动后，会挂在 root 文件系统为其提供用户空间支持。而 docker 镜像(Image)就相当于一个 root 文件系统。  

docker 镜像是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外, 还包含了一些为运行时准备的一些配置参数（如匿名卷、用户、环境变量等)。镜像不包含任何动态数据，其内容在构建后也不会被改变。

### 分层存储
实际由一组文件系统组成。镜像构建时，会一层层构建，前一层是后一层的基础。每一层构建完后就不会再发生改变，后一层上的任何改变只发生在自己这一层。

## docker 容器
镜像（Image）和容器（container）的关系，就像面向对象中类和实例的关系一样。镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。  

容器的实质是进程，但与直接在宿主执行的进程不同，容器进程运行于属于自己的独立的命名空间。因此容器可以拥有自己的 root 文件系统、自己的网络配置、自己的进程空间，甚至自己的用户ID 空间。容器内的进程是运行在一个隔离的环境里，使用起来，就好像是在一个独立于宿主的系统下的操作一样。

容器不应该向存储层内写入任何数据，容器存储层要保持无状态化。所有文件写入操作都应该使用数据卷、或者绑定宿主目录。

## docker 安装
### MacOS
```shell
brew cask install docker
```
启动终端后，通过命令行检查 docker 安装后的版本。   

```shell
xiangqian5deMacBook-Pro:docker xiangqian5$ docker version
Client:
 Version:	17.12.0-ce
 API version:	1.35
 Go version:	go1.9.2
 Git commit:	c97c6d6
 Built:	Wed Dec 27 20:03:51 2017
 OS/Arch:	darwin/amd64

Server:
 Engine:
  Version:	17.12.0-ce
  API version:	1.35 (minimum version 1.12)
  Go version:	go1.9.2
  Git commit:	c97c6d6
  Built:	Wed Dec 27 20:12:29 2017
  OS/Arch:	linux/amd64
  Experimental:	true

xiangqian5deMacBook-Pro:docker xiangqian5$ docker-machine version
docker-machine version 0.13.0, build 9ba6da9

xiangqian5deMacBook-Pro:docker xiangqian5$ docker-compose version
docker-compose version 1.18.0, build 8dd22a9
docker-py version: 2.6.1
CPython version: 2.7.12
OpenSSL version: OpenSSL 1.0.2j  26 Sep 2016
```

## 使用 docker 镜像
### 获取镜像

从Docker 镜像仓库获取镜像的命令是`docker pull`。其命令格式为：

`docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签名]`

Docker 镜像名称的格式：

* Docker 镜像仓库地址：地址的格式一般是`<域名/IP>[:端口号]`。默认地址是 Docker Hub。
* 仓库名：这里的仓库名是两段式名称，即`<用户名/软件名>`。对于 Docker Hub，如果不给出用户名，默认是`library`，即官方镜像。

比如：

```shell
xiangqian5deMacBook-Pro:docker xiangqian5$ docker pull ubuntu:16.04
16.04: Pulling from library/ubuntu
22dc81ace0ea: Pull complete 
1a8b3c87dba3: Pull complete 
91390a1c435a: Pull complete 
07844b14977e: Pull complete 
b78396653dae: Pull complete 
Digest: sha256:e348fbbea0e0a0e73ab0370de151e7800684445c509d46195aef73e090a49bd6
Status: Downloaded newer image for ubuntu:16.04
```
### 运行

```shell
keky@macos ~$docker run -it --rm ubuntu:16.04 bash
root@d45ab0240d43:/# 
root@d45ab0240d43:/# cat /etc/os-release
NAME="Ubuntu"
VERSION="16.04.4 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.4 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
root@d45ab0240d43:/# exit
exit
keky@macos ~$
```
### 列出镜像

```shell
keky@macos ~$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
keky@macos ~$
keky@macos ~$docker image ls --format "{{.ID}}: {{.Repository}}" 
f975c5035748: ubuntu
keky@macos ~$
keky@macos ~$docker image ls --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
IMAGE ID            REPOSITORY          TAG
f975c5035748        ubuntu              16.04
keky@macos ~$
```

### 删除本地镜像

删除本地镜像可以使用`docker image rm`命令，其格式为：

`docker image rm [选项] <镜像1> [<镜像2> ...]`

### 用ID、镜像名、摘要删除镜像

###### 其中 `<镜像>`可以是`<镜像短 ID>`、`<镜像长 ID>`、`镜像名`、或`镜像摘要`。

```shell
keky@macos ~$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
hello-world         latest              f2a91732366c        4 months ago        1.85kB
keky@macos ~$docker image rm f2a
Untagged: hello-world:latest
Untagged: hello-world@sha256:97ce6fa4b6cdc0790cda65fe7290b74cfebd9fa0c9b8c38e979330d547d22ce1
Deleted: sha256:f2a91732366c0332ccd7afd2a5c4ff2b9af81f549370f7a19acd460f87686bc7
Deleted: sha256:f999ae22f308fea973e5a25b57699b5daf6b0f1150ac2a5c2ea9d7fecee50fdf
keky@macos ~$
keky@macos ~$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
keky@macos ~$

keky@macos ~$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
hello-world         latest              f2a91732366c        4 months ago        1.85kB
keky@macos ~$docker image rm hello-world
Untagged: hello-world:latest
Untagged: hello-world@sha256:97ce6fa4b6cdc0790cda65fe7290b74cfebd9fa0c9b8c38e979330d547d22ce1
Deleted: sha256:f2a91732366c0332ccd7afd2a5c4ff2b9af81f549370f7a19acd460f87686bc7
Deleted: sha256:f999ae22f308fea973e5a25b57699b5daf6b0f1150ac2a5c2ea9d7fecee50fdf
keky@macos ~$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
keky@macos ~$
```

## 使用 Dockerfile 定制镜像

```shell
keky@macos docker$mkdir mynginx
keky@macos docker$cd mynginx/
keky@macos mynginx$touch Dockerfile
keky@macos mynginx$vim Dockerfile 
FROM nginx
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```

### FROM 指定基础镜像

定制镜像是指以一个镜像为基础，在其上进行定制。FROM 是Dockerfile 中的第一条必备指令。

制作镜像我们可以选择官方提供的基础镜像，除此之外 `scratch` 为特殊的空白镜像，意味着不以任何镜像为基础进行镜像的构建。

### RUN 执行命令

RUN 指令是用来执行命令行命令的。有两种格式：

* *shell* 格式：`RUN 命令`，就像直接在命令行中输入命令一样。

```shell
RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
```
* *exec* 格式：`RUN ["可执行文件"， "参数1"，"参数2"]`，类似于函数调用中的格式。

Dockerfile 中每一个指令都会建立一层，所以尽量减少指令（干一件事情用一条指令，多条命令用“&&”来分离）。

```shell
From debian:jessie

RUN buildDeps='gcc libc6-dev make' \
    && apt-get update \
    && apt-get install -y $buildDeps \
    && wget -O redis.tar.gz "http://download.redis.io/releases/redis-3.2.5.tar.gz" \
    && mkdir -p /usr/local/etc/redis \
    && tar -zxf redis.tar.gz -C /usr/local/etc/redis --strip-components=1 \
    && make -C /usr/local/etc/redis \
    && make -C /usr/local/etc/redis install \
    && rm -rf /var/lib/apt/lists/* \
    && rm redis.tar.gz \
    && rm -r /usr/local/etc/redis \
    && apt-get purge -y --auto-remove $buildDeps
```

### 构建镜像

使用`docker build`命令进行镜像构建。其格式为：

```
docker build [选项] <上下文路径/URL/->
```

在`Dockerfile`所在路径下执行：

```
keky@macos mynginx$docker build -t nginx:v3 .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM nginx
 ---> 7f70b30f2cc6
Step 2/2 : RUN echo '<h1>Hello, Docker!</h1>' > /usr/share/nginx/html/index.html
 ---> Running in 49598292366b
Removing intermediate container 49598292366b
 ---> 2759c4623d50
Successfully built 2759c4623d50
Successfully tagged nginx:v3
keky@macos mynginx$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
nginx               v3                  2759c4623d50        5 seconds ago       109MB
nginx               v2                  ef43f2adc574        20 hours ago        109MB
nginx               latest              7f70b30f2cc6        27 hours ago        109MB
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
ubuntu              latest              f975c5035748        2 weeks ago         112MB
hello-world         latest              f2a91732366c        4 months ago        1.85kB
keky@macos mynginx$
```

### 镜像构建上下文（Context）

Docker 在运行时分为Docker 引擎（服务端守护进程）和客户端工具。我们所使用的就是客户端工具，客户端工具通过Docker Remote API 与 Docker引擎交互，各种功能都是在 Docker 引擎上完成的。而`docker build`命令构建镜像，其实非在本地，而是在服务端。这就引入了上下文的概念。

当构建时，用户指定构建镜像的上下文的路径，`docker build`命令得知这个路径后，会将路径下的所有内容打包，上传 Docker 引擎。Docker 引擎接收上下文包后，展开就得到了构建镜像所需的一切文件。

`docker build -t nginx:v3 .`中的`.`是指将当前路径作为上下文的目录。

### 直接使用 GIT 进行镜像构建

```shell
docker build https://github.com/babymeng/studypark.git#:docker/mynginx

```

### 用给定 tar 包进行镜像构建

```shell
docker build http://server/context.tar.gz
```

### Dockerfile 指令

##### COPY 复制文件

格式：

* `COPY <源路径> ... <目标路径>`
* `COPY ["<源路径1>","<源路径2>",... "<目标路径>"]`

`COPY` 指令将从构建上下文目录中`<源路径>`的文件/目录复制到新的一层的镜像内的`<目标路径>`位置。比如：

```
COPY package.json /usr/src/app/
```

##### CMD 容器启动命令

`CMD`指令的格式也分两种：

* `shell`格式：`CMD <命令>`
* `exec`格式：`CMD ["可执行文件", "参数1", "参数2" ...]`

`CMD`指令是用于指定默认的容器主进程的启动命令的。

对于容器而言，其启动进程就是容器的应用进程，容器就是为了主进程而存在的，主进程退出，容器就失去了存在的意义，进而退出。

因此在容器中想要以守护进程的形式启动某些服务，就要以`exec`格式的命令进行启动。例如：

```
CMD ["nginx", "-g", "daemon off;"]
```

##### ENTRYPOINT入口点

`ENTRYPOINT`也分`exec`和`shell`两种格式。

`ENTRYPOINT`的目的和`CMD`一样，都是在指定容器启动程序及参数。`ENTRYPOINT`在运行时也可以代替，需要通过`docker run`的参数`--entrypoint`来指定。

当指定了`ENTRYPOINT`后，`CMD`的含义就变了，不再是直接运行其命令，而是将`CMD`的内容作为参数传给`ENTRYPOINT`指令，换句话说实际执行时，变为：

```
ENTRYPOINT "<CMD>"
```

###### 场景一：让镜像变成像命令一样使用

```shell
keky@macos getip$cat Dockerfile
FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
CMD [ "curl", "-s", "http://ip.cn"]
```
```shell
keky@macos getip$docker build -t myip .
Sending build context to Docker daemon  2.048kB
Step 1/3 : FROM ubuntu:16.04
 ---> f975c5035748
Step 2/3 : RUN apt-get update     && apt-get install -y curl     && rm -rf /var/lib/apt/lists/*
 ---> Running in bbc54a7925f5
Get:1 http://archive.ubuntu.com/ubuntu xenial InRelease [247 kB]
Get:2 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
.......
Running hooks in /etc/ca-certificates/update.d...
done.
Removing intermediate container bbc54a7925f5
 ---> af80dd97baf8
Step 3/3 : CMD [ "curl", "-s", "http://ip.cn"]
 ---> Running in 6a0b14106da2
Removing intermediate container 6a0b14106da2
 ---> bb3200b50bd0
Successfully built bb3200b50bd0
Successfully tagged myip:latest
keky@macos getip$

keky@macos getip$docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
myip                latest              bb3200b50bd0        58 seconds ago      129MB
nginx               v3                  2759c4623d50        5 hours ago         109MB
nginx               v2                  ef43f2adc574        25 hours ago        109MB
nginx               latest              7f70b30f2cc6        32 hours ago        109MB
ubuntu              16.04               f975c5035748        2 weeks ago         112MB
ubuntu              latest              f975c5035748        2 weeks ago         112MB
hello-world         latest              f2a91732366c        4 months ago        1.85kB
keky@macos getip$
keky@macos getip$docker run myip
当前 IP：61.135.152.134 来自：北京市 联通
keky@macos getip$
```

此时若想使用 `curl -i` 参数显示HTTP 信息头，就要使用`ENTRYPOINT`来实现

```shell
keky@macos getip$cat Dockerfile 
FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
ENTRYPOINT [ "curl", "-s", "http://ip.cn"]
```
```
keky@macos getip$docker build -t myip .
Sending build context to Docker daemon  2.048kB
Step 1/3 : FROM ubuntu:16.04
 ---> f975c5035748
Step 2/3 : RUN apt-get update     && apt-get install -y curl     && rm -rf /var/lib/apt/lists/*
 ---> Using cache
 ---> af80dd97baf8
Step 3/3 : ENTRYPOINT [ "curl", "-s", "http://ip.cn"]
 ---> Running in 9c5539176204
Removing intermediate container 9c5539176204
 ---> 59862a0649a0
Successfully built 59862a0649a0
Successfully tagged myip:latest
```
```shell
keky@macos getip$docker run myip -i
HTTP/1.1 200 OK
Date: Fri, 23 Mar 2018 08:44:14 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Set-Cookie: __cfduid=d6ec63e27641c127191728c2a622a30441521794654; expires=Sat, 23-Mar-19 08:44:14 GMT; path=/; domain=.ip.cn; HttpOnly
Server: cloudflare
CF-RAY: 3fff9d6f66757856-LAX

当前 IP：61.135.152.135 来自：北京市 联通
keky@macos getip$
```

###### 场景二：应用运行前的准备工作

官方`redis`镜像例子：

```
FROM alpine:3.4

RUN addgroup -S redis && adduser -S -G redis redis
...
ENTRYPOINT [ "docker-entrypoint.sh" ]
...

EXPOSE 6379
CMD [ "redis-server" ]
```

`CMD` `redis-server`会作为参数传递给`ENTRYPOINT `脚本`docker-entrypoint.sh`

##### ENV 设置环境变量

格式有两种：

* `ENV  <key> <value>`
* `ENV <key1>=<value1> <key2>=<value2>`

##### ARG 构建参数

格式：
`ARG <参数>[=<默认值>]`

`ARG`和`ENV`一样都是设置环境变量。但是`ARG`环境变量在将来容器运行时不会存在这些变量。

Dockerfile 中的`ARG`指令是定义参数名称，以及定义默认值。该默认值可以在构建时`docker build`中用`--build-arg <参数名>=<值>`来进行覆盖。

##### VOLUME 定义匿名卷

格式为：

* `VOLUME [ "<路径1>", "<路径2>"... ]`
* `VOLUME <路径>`

容器运行时，要保持容器存储层不发生写操作，对于需要进行数据保持的应用来说，其数据应该保存在卷（volume）中。

```
VOLUME /data
```

或

```
docker run -d -v mydata:/data xxxx
```
运行时会用 `mydata` 命名卷代替 Dockerfile 中的匿名卷。

##### EXPOSE 声明端口

格式为：
```
EXPOSE <端口1> [<端口2> ...]
```

`EXPOSE`指令仅仅是声明运行时容器提供的端口。用于帮助使用者理解镜像的守护端口；运行时使用随机端口映射，会映射到这个端口。`docker run -P`

`docker run -p <宿主端口>:<容器端口>`命令用用来映射宿主端口和容器端口的。

##### WORKDIR 指定工作目录

格式为：

```
WORKDIR <工作目录路径>
```

使用`WORKDIR`指定工作路径，以后各层的当前目录就被改为指定的目录。若目录不存在，`WORKDIR`会帮你建立目录。

##### USER 指定当前用户

格式：

```
USER <用户名>
```

`USER`指令和`WORKDIR`相似，都是改变环境状态并影响以后的层。`USER`只是帮你切换到指定的用户，这个用户必须是事先建立好的，否则无法切换。

