from typing import List
from fastapi import Depends, FastAPI, HTTPException
import time
import sys
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.requests import Request
from typing import TypeVar, Generic, Type, Any
from xml.etree.ElementTree import fromstring
import xml.etree.cElementTree as ET

from WXBizMsgCrypt import WXBizMsgCrypt
from  config import sCorpID,sEncodingAESKey,sToken
import func

# 启动App
app = FastAPI()

# 设置中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建登录会话
wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)


# 以下为接受XML格式数据部分
T = TypeVar("T", bound=BaseModel)

class Item(BaseModel):
    ToUserName: str
    AgentID: str
    Encrypt: str

class XmlBody(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    async def __call__(self, request: Request) -> T:
        # the following check is unnecessary if always using xml,
        # but enables the use of json too
        # print(request.headers.get("Content-Type"))
        if '/xml' in request.headers.get("Content-Type", ""):
            body = await request.body()
            doc = fromstring(body)
            dict_data = {}
            for node in doc.getchildren():
                dict_data[node.tag] = node.text
        else:
            dict_data = await request.json()
        return self.model_class.parse_obj(dict_data)


# 接受消息模版
Recived_Temp = """<xml> 
   <ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
   <AgentID><![CDATA[%(AgentID)s]]></AgentID>
   <Encrypt><![CDATA[%(Encrypt)s]]></Encrypt>
</xml>"""

#发送消息模版
Send_Temp = """<xml>
   <ToUserName>%(ToUserName)s</ToUserName>
   <FromUserName>%(FromUserName)s</FromUserName> 
   <CreateTime>%(timestamp)s</CreateTime>
   <MsgType>text</MsgType>
   <Content>%(content)s</Content>
</xml>"""



# 回调验证部分
@app.get("/")
async def Verify(msg_signature: str, timestamp: str, nonce: str, echostr: str):
    sVerifyMsgSig = msg_signature
    sVerifyTimeStamp = timestamp
    sVerifyNonce = nonce
    sVerifyEchoStr = echostr
    ret, sReplyEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    if( ret!=0 ):
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)
    return int(sReplyEchoStr)

# 消息接收部分
@app.post("/")
async def main(msg_signature: str, timestamp: str, nonce: str, q: str = None, item: Item = Depends(XmlBody(Item))):
    Recived_dict = {
        'ToUserName': item.ToUserName,
        'AgentID': item.AgentID,
        'Encrypt': item.Encrypt,
            }
    ReqData = Recived_Temp % Recived_dict
    ret,sMsg=wxcpt.DecryptMsg(sPostData=ReqData, sMsgSignature=msg_signature, sTimeStamp=timestamp, sNonce=nonce)
    if( ret!=0 ):
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)
    xml_tree = ET.fromstring(sMsg)
    content_recived = xml_tree.find("Content").text
    FromUserName = xml_tree.find("FromUserName").text
    ToUserName = xml_tree.find("ToUserName").text

    # 消息处理部分
    content_send = func.handle_msg(to_user_id = FromUserName, recived_msg = content_recived)

    Send_dict = {
        "ToUserName": ToUserName,
        "FromUserName": FromUserName,
        "timestamp": timestamp,
        "content": content_send,
    }
    sRespData = Send_Temp % Send_dict
    ret,sEncryptMsg=wxcpt.EncryptMsg(sReplyMsg = sRespData, sNonce = nonce, timestamp = timestamp)
    return sEncryptMsg

# 启动服务
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8181)