externalUI = "PUT YOUR UI"
secret = "PUT YOUR PASSWD"
isLAN = False
proxyUrl = "PUT YOUR URL"
output = "/tmp/config.yaml"

basicYaml = '''
port: 7890
socks-port: 7891
redir-port: 7892
allow-lan: true
bind-address: 127.0.0.1
dns:
  enable: true
  enhanced-mode: redir-host
  listen: 127.0.0.1:7874
  fallback:
    - 'tcp://8.8.8.8'
  nameserver:
    - '114.114.114.114'
    - '8.8.8.8'
  ipv6: false
experimental:
  ignore-resolve-fail: true

external-controller: 127.0.0.1:9090
external-ui: {ui}
secret: {passwd}
log-level: debug
mode: rule

proxy-groups:
- name: MainProxy
  type: select
  proxies:
  - YouYunProxy
  - YouYunProxyFallback
  - YouYunProxyUrlTest
  - DIRECT
- name: YouYunProxy
  type: select
  use:
  - youyun_provider
- name: YouYunProxyFallback
  type: fallback
  use:
  - youyun_provider
  url: https://www.google.com/
  interval: 300
- name: YouYunProxyUrlTest
  type: url-test
  use:
  - youyun_provider
  url: https://www.google.com/
  interval: 300

proxy-providers:
  youyun_provider:
    type: http
    path: "./proxy_provider/youyun_config.yaml"
    url: {proxy_provider_url}
    interval: 3600
    health-check:
      enable: true
      interval: 600
      url: https://www.google.com/

rule-providers:
  reject:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

  icloud:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/icloud.txt"
    path: ./ruleset/icloud.yaml
    interval: 86400

  apple:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/apple.txt"
    path: ./ruleset/apple.yaml
    interval: 86400

  google:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/google.txt"
    path: ./ruleset/google.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400

  direct:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/direct.txt"
    path: ./ruleset/direct.yaml
    interval: 86400

  private:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/private.txt"
    path: ./ruleset/private.yaml
    interval: 86400

  gfw:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/gfw.txt"
    path: ./ruleset/gfw.yaml
    interval: 86400

  greatfire:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/greatfire.txt"
    path: ./ruleset/greatfire.yaml
    interval: 86400

  tld-not-cn:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/tld-not-cn.txt"
    path: ./ruleset/tld-not-cn.yaml
    interval: 86400

  telegramcidr:
    type: http
    behavior: ipcidr
    url: "https://cdn.jsdelivr.net/ghif/\
elseLoyalsoldier/clash-rules@release/telegramcidr.txt"
    path: ./ruleset/telegramcidr.yaml
    interval: 86400

  cncidr:
    type: http
    behavior: ipcidr
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/cncidr.txt"
    path: ./ruleset/cncidr.yaml
    interval: 86400

  lancidr:
    type: http
    behavior: ipcidr
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/lancidr.txt"
    path: ./ruleset/lancidr.yaml
    interval: 86400

  applications:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/\
Loyalsoldier/clash-rules@release/applications.txt"
    path: ./ruleset/applications.yaml
    interval: 86400

rules:
- RULE-SET,applications,DIRECT
- RULE-SET,private,DIRECT
- RULE-SET,reject,REJECT
- RULE-SET,icloud,DIRECT
- RULE-SET,apple,DIRECT
- RULE-SET,google,DIRECT
- RULE-SET,proxy,MainProxy
- RULE-SET,direct,DIRECT
- RULE-SET,lancidr,DIRECT
- RULE-SET,cncidr,DIRECT
- RULE-SET,tld-not-cn,MainProxy
- RULE-SET,gfw,MainProxy
- RULE-SET,greatfire,MainProxy
- RULE-SET,telegramcidr,MainProxy
- GEOIP,LAN,DIRECT
- GEOIP,CN,DIRECT
- IP-CIDR, 8.8.8.8/0, MainProxy
- MATCH,DIRECT
'''
