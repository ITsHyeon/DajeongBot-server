DajeongBot server Document
===

## 채팅 API
- 사용자와 챗봇이 대화하기 위한 API 입니다.
  - 일정 등록, 일정 알림, 일정 후기, 추억 회상의 기능을 포함하고 있습니다.
- DANBEE.ai의 채트플로우를 활용하여 사용자의 말에 대한 의도를 파악하고 대화를 진행할 수 있도록 구현하였습니다.

> chat type

|                                        | type |
|----------------------------------------|------|
| **BASIC_CHAT**                       | 0    |
| **REGISTER_CHAT**                   |  1    |
| **MEMORY_CHAT**                      | 2    |
| ~~NOTIFICATION_CHAT~~                  | 3    |
| **QUESTION_SCHEDULE_SELECT_CHAT** | 3    |
| **QUESTION_SCHEDULE_REPLY_CHAT**  | 3    |


> node type

|                     | type |
|---------------------|------|
| **SPEAK_NODE**    | 0    |
| **SLOT_NODE**     | 1    |
| **CAROUSEL_NODE**| 2    |
| **IMAGE_NODE**    | 3    |

### 채팅내역 가져오기
> 첫 메세지 요청시
```
GET /messages/<int:res_account_id>
```
> 채팅 추가 요청시
```
GET /messages/<int:res_account_id>/<int:last_index>
```
#### Response Example
```json
[
  {
        "id": 1,
        "content": 32,
        "node_type": 0,
        "chat_type": 0,
        "time": 1534097877292,
        "isBot": 0,
        "carousel_list": null,
        "slot_list": null
    },
  {
        "id": 2,
        "content": 32,
        "node_type": 0,
        "chat_type": 0,
        "time": 1534097877292,
        "isBot": 1,
        "carousel_list": null,
        "slot_list": null
    }    
    
]

```

### 메세지 보내기
```
POST /messages
```

#### 일정등록
사용자의 일정에 대해 언제, 어디서, 무엇을 하는지에 대해 입력을 받습니다.

##### Request example
- 서버로부터 전달된 response 값을 함께 요청해주어야합니다.
- 서버에서 온 response가 없는 경우는 아직 챗복과의 대화가 없는 경우 입니다.

> 챗봇과의 채트플로우에 진입할 때
```json
{
    "account_id": 32,
    "content": "할 일이 생겼어",
    "node_type": 0,
    "chat_type": 1, 
    "time" : 1534097877292,
    "isBot" : 0,
    "response":{}
}
```
> 챗봇과의 대화 중
 - 챗봇과의 대화를 유지하기 위하여 챗봇 대화 데이터를 함께 전송합니다.
```json
{
    "account_id": 32,
    "content": "홍대에서 치킨 먹기",
    "node_type": 0,
    "chat_type": 1, 
    "time" : 1534097877292,
    "isBot" : 0,
    "response":{
        "result" : {
            "version": "0.1",
            "chatbot_id": "9c94e975-49c8-4a08-bdfe-b19085ecf42f",
            "user_id": "",
            "input_sentence": "할 일이 생겼어",
            "ins_id": "55723884",
            "intent_id": "25e87c92-a2a9-4aea-85c5-34860f40d328",
            "ref_intent_id": "2933dbcf-5717-42aa-8bf1-ed37599cd722",
            "chatflow_id": "FLOW1533045900000",
            "node_id": "SlotNode_1533084112968",
            "param_id": "where",
            "another_result": [],
            "result": [
                {
                    "nodeType": "speak",
                    "timestamp": 1535265568661,
                    "message": "할 일이 생겼구나! 어떤 건데?",
                    "imgRoute": "",
                    "optionList": [],
                    "carouselList": [],
                    "quickList": []
                },
                {
                    "nodeType": "slot",
                    "timestamp": 1535265568875,
                    "message": "어디서 하나요?",
                    "imgRoute": "",
                    "optionList": [],
                    "carouselList": [],
                    "quickList": []
                }
            ],
            "debugging_result": [],
            "parameters": {
                "@chatbotName": "Dajeong",
                "@message": "할 일이 생겼구나! 어떤 건데?",
                "sysany": "",
                "what": "",
                "@sessionId": "15404613",
                "where": "",
                "detail": "",
                "detail_content": "",
                "when": "",
                "status": "3"
            },
            "emotions": {},
            "session_id": 15404613,
            "log_id": 167310938,
            "debugCode": "",
            "debugMsg": "",
            "evaluate_setting": "N",
            "greetingYn": "N",
            "resultStatus": {
                "resultCmt": "",
                "resultCode": "200",
                "resultMsg": "success"
            },
            "personalityObj": {
                "intentId": "",
                "nodeMessage": "",
                "isChatflow": ""
            },
            "pauseFlowInsList": [],
            "extension": {},
            "channel_id": "0",
            "flow_type": ""
        }
    }
}

```

##### Response example
```json

```

#### 일정 알림
- celery와 celery-beat을 이용하여 주기적으로 사용자에게 안내 메세지를 전송
- pyFcm을 이용한 디바이스에 notification 전송

##### Response example
```json
{
    "title": "오늘 일정이 있어요!",
    "message": "[ 장소 ]에서 [ 일정 ]",
    "data": {
        "status": "Success",
        "result": {
            "node_type": 0,
            "id": 32,
            "chat_type": 3,
            "time": 15404613,
            "img_url": [],
            "content": [
                "오늘은 일정이 있는 날이네!",
                "[ 장소 ]에서 [ 일정 ]",
                "오늘도 화이팅!"
            ]
        }
    }
}
```

#### 일정 후기
- celery와 celery-beat을 이용하여 주기적으로 질문을 전송
- pyFcm을 이용한 디바이스에 notification 전송
- Slot Node, Basic Node를 이용함
##### Request Example
> 등록할 후기를 선택할 때의 request
```json

```
> 선택한 일정에 대한 후기를 남기는 request
```json

```
##### Response Example
> 챗봇이 먼저 질문 할 때의 Response
```json
{
    "title": "당신의 하루를 다정봇에게 들려주세요 :)",
    "message": "오늘 1개의 일정이 있습니다.",
    "data": {
        "status": "Success",
        "result": {
            "id": 32,
            "node_type": 2,
            "chat_type": 5,
            "time": 15404613,
            "img_url": [],
            "content": ["오늘 하루 어땠나요?"],
            "events": [
                {
                    "id": 1,
                    "account_id": 32,
                    "schedule_when": "2018-09-16",
                    "schedule_where": "치킨 집",
                    "schedule_what": "파티",
                    "assign_time": 15404613,
                    "detail": "금진이랑 같이 생일파티 하기로 했어",
                    "review": null,
                    "notification_send": 1,
                    "question_send": 0
                }
            ]
        }
    }
}
```
> 사용자의 후기 등록에 대한 Response
```json

```

#### 추억회상
- 사용자가 지난 추억에 대해 떠올리기 위한 기능
- Carousel Node를 이용함

##### Request Example

> 추억회상 채트플로우에 진입하기 위한 Request
```json

```
> 궁금한 일정에 대해 요청하는 Reqeust
```json

```

## USER API
- 회원을 관리하기 위한 API 입니다.
  - 회원가입, 로그인 기능을 포함하고 있습니다.
- ~~SNS 로그인(Facebook, Google, Kakao)를 지원합니다.~~
> account type

|          | type |
|----------|------|
| Basic    | 0    |
| Facebook | 1    |
| Kakao    | 2    |
| Google   | 3    |
> bot type

|          | type |
|----------|------|
| *다정군* | 0    |
| *다정냥* | 1    |
| *다정곰* | 2    |
| *다정몽* | 3    |
### 회원가입

##### Request Example
> 일반유저
```json

```

> SNS 유저
```json

```
##### Response Example
````json
{
    "status": "Success",
    "user_info": {
        "id": 32,
        "user_id": "devuri404@gmail.com",
        "name": "한유리",
        "birthday": "2000-05-09",
        "account_type": 0,
        "bot_type": 1
    }
}
````
### 로그인
##### Request Example
> 일반유저
```json

```

> SNS 유저
```json

```
##### Response Example
```json

```
### 회원정보 관리
> 닉네임
```
[GET] /me/names/<int:account_id>
```


> 챗봇 캐릭터


> 알림 시간


> 초기화


> 토근

