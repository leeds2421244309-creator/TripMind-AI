import json


def parse_json_response(content: str):

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1:

            json_text = content[start:end + 1]

            return json.loads(json_text)

        raise ValueError(
            "AI返回内容不是有效JSON"
        )