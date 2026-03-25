### rlaunch 挂载镜像（映射本地文件夹） + 显卡

```bash
rlaunch \
--image=registry.h.pjlab.org.cn/ailab-sdpdev-sdpdev_cpu/slime_sxy:slime0228 \
--volume=/home/sunxiangyu/slime_sxy/slime_wd:home/sunxiangyu/slime_wd \
--charged-group=sdpdev_gpu \
--private-machine=group \
--gpu=2 \
--memory=16000 \
--cpu=8 \
-e DISTRIBUTED_JOB=true \
-- bash
```

### docker挂载映射本地文件夹

```bash
docker run --rm -it \
  --gpus all \
  --ipc=host \
  --shm-size=16g \
  -v /home/sunxiangyu/slime_sxy/slime_wd:/root/slime_wd \
  -w /root/slime_wd \
  slimerl/slime:latest \
  /bin/bash
```
