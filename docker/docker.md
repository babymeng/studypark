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
