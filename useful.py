import openai
def chatGPT_response(query):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        return response['choices'][0]['text']
    except:
        return "Сервер chatGPT перегружен"


def days_to_seconds(days):
    return days*24*60*60


def create_mask(text):
    new_text = ''
    text_len = len(text)
    if text_len > 150:
        new_text = text[:150]
        for i in range(150,text_len+1):
            new_text = new_text + '$'
        return new_text
    else:
        return text
