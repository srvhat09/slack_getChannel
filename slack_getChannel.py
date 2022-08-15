# -*- coding: utf-8 -*-

#
# Created on: 2022/08/06
# AUTHOR:	Reiki Hattori
# Copyright (c) 2022, Anaheim Engineering. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
import argparse
import codecs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=str, required=True, help="SlackのチャネルIDを設定します。[必須]")
    parser.add_argument("--out", type=str, required=True, help="Jsonファイル名を指定します。フルパス指定可")
    return parser.parse_args()


def get_conversations(args):
    messages = []
    url = "https://slack.com/api/conversations.history"
    token = "xxxx-xxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    header = {
        "Authorization": "Bearer {}".format(token)
    }

    payload = {}
    payload.update({"channel": args.channel})

    response = requests.get(url, headers=header, params=payload)
    response_dic = response.json()
    messages.append(response_dic["messages"])
    while True:
        next_cursor = ""
        try:
            if ("response_metadata" in response_dic) and (len(response_dic["response_metadata"]["next_cursor"]) > 0):
                next_cursor = response_dic["response_metadata"]["next_cursor"]
            else:
                break
        except KeyError:
            break
        payload.update({"cursor": next_cursor})
        response = requests.get(url, headers=header, params=payload)
        response_dic = response.json()
        messages.append(response_dic["messages"])

    return messages


if __name__ == "__main__":
    # 実行パラメタ解析
    args = parse_args()
    messages_group = get_conversations(args)

    msg_dicts = []
    for i, messages in enumerate(messages_group):
        if i == 0:
            msg_dicts = messages
            continue
        for message in messages:
            msg_dicts.append(message)

    # 解析結果のjsonファイル吐き出し
    with codecs.open(args.out, 'w', 'utf-8') as outfile:
        json.dump(msg_dicts, outfile, ensure_ascii=False, indent=4)

