import json


def parse_json_response(content: str):

    try:
        data=json.loads(content)

    except json.JSONDecodeError:

        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1:

            json_text = content[start:end + 1]

            data = json.loads(json_text)

        else:

            raise ValueError(
                "AI返回内容不是有效JSON"
            )

     # AI没有按照要求返回status时，自动补充
    if "status" not in data:

        data = {
            "status": "success",
            "plan": data
        }


    return data