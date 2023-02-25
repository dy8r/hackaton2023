import openai
from config import OPENAI_API_KEY
from database import insert_query, select_query
from datetime import datetime

USER_ID = 1

DATABASE_DESCRIPTION = """
Bank_Account (
  ID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each bank account
  account_name TEXT, -- Name of the bank account
  user_id INT, -- ID of the user who owns the account
  balance INT -- Current balance of the account
);

Transactions (
  ID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each transaction
  userID INT, -- ID of the user who made the transaction
  total INT, -- Total amount of the transaction
  date DATETIME, -- Date and time of the transaction
  bank_account INT, -- ID of the bank account associated with the transaction
  comment TEXT, -- Optional comment or note about the transaction
  category TEXT, -- Optional category or classification for the transaction
  label TEXT, -- Optional label or tag for the transaction
  item TEXT, -- Optional item or product associated with the transaction
  FOREIGN KEY (bank_account) REFERENCES Bank_Account(ID) -- Constraint to ensure bank_account field references a valid bank account ID
);"""

def send_request_to_openai_get_stat(user_prompt):
    openai.api_key = OPENAI_API_KEY
    today = datetime.now().strftime("%Y-%m-%d")
    

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
    
    prompt_2  = "I have gave you a prompt: " + prompt + """. Your responsne was: """ + query + """The result was: """ +  str(db_return) +""". Give me an answer to my original prompt"""

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



def send_request_to_openai_add_to_database(user_prompt):
    openai.api_key = OPENAI_API_KEY
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""I have a database with the following structure:
        {DATABASE_DESCRIPTION}

        I have such transaction info: {user_prompt}

        Write a request to add a record to Transactions table, knowing that:

        user_id is {USER_ID}
        total is the sum of transaction
        date - date of transaction
        bank account is one of: ((id: 1, name: Default Bank), (id: 2, name: Other Bank), (id: 3, name: Another Bank)) - choose the best fit. If none fits, choose the first one
        Comemnt is the full string of transaction info

        Category is one of the: groceries, housing, sports, furniture, other - choose the best fit or other if none fits
        Label is one of: home, work, partying, not specified - choose the best fit or not specified if not specified
        Item is one of: meat, apple, nuts, icecream, other - choose the best fit or other if none fits

        Today is {today}

        Create a sql query to insert this record to a table
        If the prompt has multiple transactions, create a query for each transaction.
        Reply only with a single query for each transaction, no text, no explanation. Pure code."""

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
        )

    queries_str = response.choices[0].text.strip()
    queries = queries_str.split(";")
    print(queries)
    at_least_one_suceess = False
    for query in queries:
        print(query)
        if(len(query) > 0):
            status = insert_query(query)
            if status == -1:
                print(query)
            else:
                at_least_one_suceess = True
    
    if not at_least_one_suceess:
        return "Sorry, an error occurerd. Please try again later."

    if len(queries) == 1:
        success_prompt = """Refer to the following prompt. We have added an expense record to database. Here is the query for reference: """ + queries 
        + """ Reply with a success message. This message will be shown to user , so say somethink in the lines of: 'Success! Changes to your budget have been savved. The changes are: 'and here list eeverything that we haev recorded"""
    else:
        success_prompt = """Refer to the following prompt. We have added multiple expense records to database. Here are the queries for reference: """ + queries 
        + """ Reply with a success message. This message will be shown to user , so say somethink in the lines of: 'Success! Changes to your budget have been savved. The changes are: 'and here list eeverything that we haev recorded"""
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=success_prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
    )    

    return response.choices[0].text.strip()