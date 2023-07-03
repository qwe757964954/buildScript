import json
import os
from typing import Text
# from model import BuildJob
import requests
import argparse

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',required=True, help='the package at the path')
    parser.add_argument('-n', '--chanel',required=True, help='upload chanel')
    parser.add_argument('-v', '--version',required=True, help='version string')
    parser.add_argument('-l', '--changelog',required=True, help='changelog string')
    args = parser.parse_args()

    return args


def __add_pack__(upload_dict):
    print("add pack begin")
    url = "http://nodeport-test.oa.com:31394/addDevPack"
    files = [upload_dict]
    data = {
        "appId": "3013",
        "upgradeType": "1",
        "floorPackNum": "0",
        "descript": "http://172.20.152.12:9090/job/QSDK/",
        "version": upload_version,
        "changelog": upload_changelog,
        "usingServices": '127.0.0.1',
        "isStartUpdate": "1",
        "files": json.dumps(files),
    }
    result = requests.post(url=url, data=data) 
    resp = result.json()
    if resp.get("code", 0) != 0:
        raise Exception(f"add pack error:{resp}")
    print(f"add pack end, url:{url}, data:{data}, resp:{resp}")


def upload_build():
    print("upload build begin")
    output_file = upload_path
    url = "http://266-upload.oa.com:8082/pack-upload?type=package"
    files = {
        "file": open(output_file, "rb"),
    }
    result = requests.post(url=url, files=files) 
    resp = result.json()
    if resp["ret"] != 0:
        raise Exception(f"upload build error:{resp}")    
    upload_dict = {
        "name": upload_chanel,
        "path": resp["data"]["file"],
    }
    __add_pack__(upload_dict)
    print(f"upload build end, url:{url}, resp:{resp}, files:{files}")
def main():
    args = build_parser()
    global upload_path
    upload_path = args.path + ""
    global upload_chanel
    upload_chanel = args.chanel + ""
    global upload_changelog
    upload_changelog = args.changelog + ""
    global upload_version
    upload_version = args.version + ""
    upload_build()
    

if __name__ == '__main__':
    main()
    
