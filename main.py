import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

prompt = """I have a database that has user_id(int), sum(int), category_type(text) and transaction_date(YYYY-MM-DD) fields.
It is used for personal finance tracking.
Possible category_type fields are: "food", "shopping", "housing"
User with ID = 12345 prompts: "What did I spend more on: food this month or shopping in last month?"
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

print(response.choices[0].text.strip())