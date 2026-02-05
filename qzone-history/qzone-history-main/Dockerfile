FROM golang:1.25
# 把之前的 goproxy.cn 换成 aliyun
ENV GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
WORKDIR /app

# 先拷依赖文件，利用 Docker 缓存加速
COPY go.mod go.sum ./
RUN go mod download

# 安装热更新工具（开发用）
RUN go install github.com/air-verse/air@latest

# 再拷贝源码（开发时也会用 volume 覆盖）
COPY . .

# 容器里默认用终端展示登录二维码（避免容器内打开浏览器/随机端口导致无法访问）
ENV QZONE_HISTORY_QR_MODE=terminal

CMD ["air", "-c", ".air.toml"]

