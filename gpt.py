import openai
from config import OPENAI_API_KEY
from database import insert_query, select_query


def send_request_to_openai_get_stat(user_prompt):
    openai.api_key = OPENAI_API_KEY

    prompt = """I have a database that has user_id(int), sum(int), category_type(text), name(text), and transaction_date(YYYY-MM-DD) fields.
    It is used for personal finance tracking.
    Possible category_type fields are: "groceries", "housing"
    User with ID = 12345 prompts: """ + user_prompt + """""
    Reply with an sql query to get what user prompted from database. Do not provide explanation, give me pure code
    For reference, datetime now is 10:09 25.02.2023"""

    gpt_context_id = "Context ID for GPT-3"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
        context=gpt_context_id,
        )

    print(response.choices[0].text.strip())
    query = response.choices[0].text.strip()
    gpt_context_id = response.choices[0].context

    db_return = select_query(query)
    if db_return == -1:
        return "Sorry, I did not understand that. Please try again."
    
    prompt_2  = "I have gave you a prompt: " + prompt + """. Your responsne was: """ + query + """The result was: """ +  db_return +""". Give me an answer the user's original prompt"""

    user_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_2,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
        context=gpt_context_id,
        )

    final_response = user_response.choices[0].text.strip()
    return final_response



def send_request_to_openai_add_to_database(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
        )

    query = response.choices[0].text.strip()
    status = insert_query(query)
    if status() == -1:
        print(query)
        return "Sorry, an error occurerd. Please try again later."

    return response.choices[0].text.strip()