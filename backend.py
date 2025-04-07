import pandas as pd
import json
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_aws import ChatBedrock
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize database connection
def init_db(db_path):
    engine = create_engine(f"sqlite:///{db_path}")
    return SQLDatabase(engine=engine)

# Initialize LLM
def init_llm():
    return ChatBedrock(
        model="anthropic.claude-3-5-sonnet-20240620-v1:0",
        beta_use_converse_api=True
    )

# Create query chain
def create_chain(llm, db):
    system = """Double check the user's {dialect} query for common mistakes..."""  # Your full system prompt
    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{query}")]
    ).partial(dialect=db.dialect)
    validation_chain = prompt | llm | StrOutputParser()
    return {"query": create_sql_query_chain(llm, db)} | validation_chain

# Process user question
def process_user_question(user_question, db_path="data/sample_service_records.db"):
    try:
        db = init_db(db_path)
        llm = init_llm()
        chain = create_chain(llm, db)
        
        validated_query = chain.invoke({"question": user_question})
        result = db.run(validated_query)
        
        # Process result and return JSON response
        return json.dumps({
            "user_question": user_question,
            "sql_query": validated_query,
            "result": process_raw_result(result)
        }, indent=4)
    except Exception as e:
        return json.dumps({
            "user_question": user_question,
            "error": str(e)
        }, indent=4)

def process_raw_result(raw_result):
    # Your existing result processing logic
    pass