import streamlit as st
import pandas as pd
import json

from agent import query_agent, create_agent

def decode_response(response: str) -> dict:
    return json.loads(response)

def write_response(response_dict: dict):
    #check if response is an answer
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    #check if the response is a bar chart
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    #check if the response is a line chart
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    #check if the response is table
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

st.title("Chatea con tu CSV")

st.write("Sube tu archivo CSV:")

data = st.file_uploader("Carga archivo CSV")

query = st.text_area("Inserta tu consulta:")

if st.button("Submit", type="primary"):
    # Create an agent from the CSV file.
    agent = create_agent(data)

    # Query the agent.
    response = query_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_response(decoded_response)