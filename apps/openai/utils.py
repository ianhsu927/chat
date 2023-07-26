# -*- coding: utf-8 -*-
# @Time    : 2023/3/4 1:30
# @Author  : 屿你有关
# @Site    : 
# @File    : utils.py
# @Comment :
import json
import os
from typing import Dict, Any, Union, AsyncIterable
# AsyncIterable 是异步编程中的重要概念。它们允许您从异步来源获取值，而无需等待所有值都准备好。

from httpx import AsyncClient
# httpx 异步客户端


async def stream_request(url: str, params: Union[str, Dict[str, Any]]) \
                            -> AsyncIterable[Dict[str, Any]]:
    """流请求"""
    async with AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.getenv("API_KEY"),
        }
        async with client.stream("POST", url, headers=headers, \
                            json=params, timeout=60) as response:
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                line = line.replace("data: ", "")
                try:
                    data = json.loads(line)
                except Exception:
                    data = {"choices": [{"finish_reason": "stop"}]}
                if data.get("choices")[0].get("finish_reason") is not None:
                    return
                yield data.get("choices")[0].get("delta")


async def request(url: str, params: Union[str, Dict[str, Any]])\
                    -> Dict[str, Any]:
    """请求"""
    async with AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.getenv("API_KEY"),
        }
        response = await client.post(url=url, headers=headers, json=params)
        return response.json()
