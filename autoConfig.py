#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests
import yaml
import config
import socket
import re
import getopt
import sys

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "https://127.0.0.1:7890"
}
ipv4Pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2}) \
        (\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')


def loadConfig() -> dict:
    return yaml.safe_load(config.basicYaml)


def saveConfig(configData: dict, output: str):
    with open(output, "w") as f:
        yaml.safe_dump(configData, f)


def checkProxy() -> bool:
    proxySocket = None
    proxyPort = 7890
    proxyHost = "0.0.0.0"
    try:
        proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxySocket.settimeout(10)
        proxySocket.connect((proxyHost, proxyPort))
        return True
    except socket.error:
        return False
    finally:
        if proxySocket:
            proxySocket.close()


def downloadRules(url: str, hasProxy: bool) -> dict:
    resp = requests.get(url=url, proxies=proxies if hasProxy else {})
    if resp.status_code != requests.codes.ok:
        return []
    else:
        return yaml.safe_load(resp.text)['payload']


def handleDomain(ruleSet: list, policy: str) -> list:
    rules = []
    for rule in ruleSet:
        rules.append("DOMAIN,{},{}".format(rule, policy))
    return rules


def handleIpcidr(ruleSet: list, policy: str) -> list:
    rules = []
    for rule in ruleSet:
        if ipv4Pattern.search(rule):
            rules.append("IP-CIDR,{},{}".format(rule, policy))
        else:
            rules.append("IP-CIDR6,{},{}".format(rule, policy))
    return rules


def handleClassical(ruleSet: list, policy: str) -> list:
    rules = []
    for rule in ruleSet:
        rules.append("{},{}".format(rule, policy))
    return rules


def parseRuleSet(rules: list, ruleProviders: dict) -> list:
    newRules = []
    hasProxy = checkProxy()
    handlerMap = {
            "domain": handleDomain,
            "ipcidr": handleIpcidr,
            "classical": handleClassical
            }
    for rule in rules:
        if rule.startswith("RULE-SET"):
            _, ruleName, rulePolicy = rule.split(",")
            provider = ruleProviders[ruleName]
            if provider['type'] != "http":
                raise Exception(
                        "Unsupport type [{}] for Rule-Provider [{}]".format(
                            provider['type'],
                            ruleName
                            )
                        )

            ruleSet = downloadRules(provider["url"], hasProxy)
            newRules.extend(
                    handlerMap[provider["behavior"]](ruleSet, rulePolicy)
                    )
        else:
            newRules.append(rule)

    return newRules


def generateConfig(
        proxyUrl: str,
        isLan=False,
        ui="",
        secret='',
        output="/tmp/config.yaml"):

    basicConfig = loadConfig()

    # basic setting
    basicConfig['allow-lan'] = isLan
    basicConfig['secret'] = secret
    basicConfig['external-ui'] = ui
    basicConfig['proxy-providers']['youyun_provider']['url'] = proxyUrl

    if isLan:
        basicConfig['bind-address'] = "0.0.0.0"
        basicConfig['external-controller'] = "0.0.0.0"

    rules = basicConfig['rules']
    ruleProviders = basicConfig['rule-providers']
    basicConfig.pop("rule-providers")
    basicConfig['rules'] = parseRuleSet(rules, ruleProviders)
    saveConfig(basicConfig, output)


if __name__ == "__main__":
    generateConfig(
            config.proxyUrl,
            config.isLAN,
            config.externalUI,
            config.secret,
            config.output
            )
