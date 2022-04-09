#!/bin/bash

default_url='https://github.com/Dreamacro/clash/releases/download/v1.10.0/clash-linux-amd64-v1.10.0.gz'

if [ "$1" ]; then
    default_url=$1
fi

curl -L "$default_url" -o /tmp/clash.gz
gzip /tmp/clash.gz -d
sudo mv /tmp/clash /usr/local/bin/clash
sudo chmod +x /usr/local/bin/clash

sudo mkdir -p /etc/clash
sudo sh -c 'cat >> /etc/systemd/system/clash.service << EOF
[Unit]
Description=Clash daemon, A rule-based proxy in Go.
After=network.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/local/bin/clash -d /etc/clash

[Install]
WantedBy=multi-user.target
EOF'

echo "How to use:"
echo "sudo systemctl enable clash.service"
echo "sudo systemctl start clash.service"
