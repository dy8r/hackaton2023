import openai
from config import OPENAI_API_KEY

# openai.api_key = OPENAI_API_KEY

def send_request_to_openai(user_prompt):
    openai.api_key = OPENAI_API_KEY
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.2,
    #     )

    # return response.choices[0].text.strip()

    prompt = """I have a database that has user_id(int), sum(int), category_type(text), name(text), and transaction_date(YYYY-MM-DD) fields.
    It is used for personal finance tracking.
    Possible category_type fields are: "groceries", "housing"
    User with ID = 12345 prompts: """ + user_prompt + """""
    Reply with an sql query to get what user prompted from database. Do not provide explanation, give me pure code
    For reference, datetime now is 10:09 25.02.2023"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
        )

    print(response.choices[0].text.strip())

    ret = input('\nsql returned\n')

    prompt_2  = "I have gave you a prompt: " + prompt + """. Your responsne was: """ + response.choices[0].text.strip() + """The result was: """ +  ret +""". Give me an answer the user's original prompt"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_2,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
        )

    # print(response.choices[0].text.strip())
    return response.choices[0].text.strip()
