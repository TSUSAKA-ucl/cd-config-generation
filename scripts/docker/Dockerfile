# -------------------------------
# 1. Build stage: Blender展開
# -------------------------------
FROM ubuntu:24.04 AS builder

# 基本ツール
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget tar xz-utils ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Blender 3.6 ダウンロード & 展開
RUN wget https://download.blender.org/release/Blender3.6/blender-3.6.23-linux-x64.tar.xz \
    && tar -xf blender-3.6.23-linux-x64.tar.xz -C /opt

# -------------------------------
# 2. Final stage: 軽量化 Ubuntu
# -------------------------------
FROM ubuntu:24.04

# Blender依存ライブラリ
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglu1-mesa libxi6 libxcursor1 libxrandr2 libxinerama1 libxrender1 \
    libxfixes3 libxext6 libxdamage1 libopenal1 libstdc++6 \
    bash wget tar xz-utils \
    meshlab \
    && rm -rf /var/lib/apt/lists/*

# Blender 本体を builder からコピー
COPY --from=builder /opt/blender-3.6.23-linux-x64 /opt/blender-3.6.23-linux-x64
RUN ln -s /opt/blender-3.6.23-linux-x64/blender /usr/local/bin/blender

# 作業ディレクトリ
WORKDIR /data

# デフォルト: Blender バックグラウンド起動
ENTRYPOINT ["blender", "--background"]
COPY ./blender_convex_hull.py /opt
