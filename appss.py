from flask import Flask, redirect, request, render_template, session
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd
from langchain.globals import set_verbose
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
import json
from pandas import json_normalize

set_verbose(False)

set_verbose(False)
load_dotenv()
app = Flask(__name__)
app.secret_key = 'nader'

def load_data(json_filepath, csv_filepath):
    # Load JSON data from a file
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    # Flatten the data
    flat_data = []
    for car_key, car_value in data.items():
        flat_record = json_normalize(car_value)  # Ensure this is the only line using json_normalize
        flat_data.append(flat_record)

    # Combine all records into a single DataFrame
    df = pd.concat(flat_data, ignore_index=True)

    # Save the DataFrame to a CSV file
    df.to_csv(csv_filepath, index=False)
    print(f"Data has been successfully saved to {csv_filepath}")

    # Return the DataFrame
    return df

def get_vectorstore(df):
    # Select relevant columns for embeddings, based on the car data structure you have
    relevant_columns = [
        'car_name', 
        'price_info.germany',
        'range_info.City - Cold Weather *', 
        'range_info.Highway - Cold Weather *', 
        'range_info.Combined - Cold Weather *', 
        'range_info.City - Mild Weather *', 
        'range_info.Highway - Mild Weather *', 
        'range_info.Combined - Mild Weather *', 
        'performance_info.acceleration', 
        'performance_info.top_speed', 
        'performance_info.electric_range', 
        'performance_info.total_power', 
        'performance_info.total_torque', 
        'performance_info.drive', 
        'battery_info.nominal_capacity', 
        'battery_info.battery_type', 
        'battery_info.number_of_cells', 
        'battery_info.architecture', 
        'battery_info.warranty_period', 
        'battery_info.warranty_mileage', 
        'battery_info.useable_capacity', 
        'battery_info.cathode_material', 
        'battery_info.pack_configuration', 
        'battery_info.nominal_voltage', 
        'battery_info.form_factor', 
        'battery_info.name___reference', 
        'charging_info.home_destination.charge_port', 
        'charging_info.home_destination.port_location', 
        'charging_info.home_destination.charge_power', 
        'charging_info.fast_charging.fastcharge_port', 
        'charging_info.fast_charging.fc_port_location', 
        'charging_info.fast_charging.fastcharge_power_max', 
        'charging_info.fast_charging.fastcharge_power_10-80%', 
        'charging_info.plug_charge.plug_&_charge_supported', 
        'v2x_info.v2l.v2l_supported', 
        'v2x_info.v2l.max_output_power', 
        'v2x_info.v2h.v2h_via_ac_supported', 
        'v2x_info.v2h.max_output_power', 
        'v2x_info.v2g.v2g_via_ac_supported', 
        'v2x_info.v2g.max_output_power', 
        'efficiency_info.evdb_real_range.range', 
        'efficiency_info.evdb_real_range.vehicle_consumption', 
        'efficiency_info.wltp_ratings_tel.range', 
        'efficiency_info.wltp_ratings_tel.rated_consumption', 
        'efficiency_info.wltp_ratings_tel.vehicle_consumption', 
        'efficiency_info.wltp_ratings_teh.range', 
        'efficiency_info.wltp_ratings_teh.rated_consumption', 
        'efficiency_info.wltp_ratings_teh.vehicle_consumption', 
        'real_energy_consumption.city_cold weather_cold_weather', 
        'real_energy_consumption.highway_cold weather_cold_weather', 
        'real_energy_consumption.combined_cold weather_cold_weather', 
        'real_energy_consumption.city_mild weather_mild_weather', 
        'real_energy_consumption.highway_mild weather_mild_weather', 
        'real_energy_consumption.combined_mild weather_mild_weather'
    ]
    
    # Combine selected columns into a single text description
    car_descriptions = df[relevant_columns].astype(str).agg(' '.join, axis=1)
    
    # Assume the rest of the function processes these descriptions with embedding and vector store creation
    embeddings = OpenAIEmbeddings()  # placeholder for your embedding method
    vectorstore = FAISS.from_texts(texts=car_descriptions, embedding=embeddings)  # placeholder for your vector store method
    return vectorstore

def get_conversation_chain(vectorstore):
    model_name = "gpt-3.5-turbo"
    temperature = 0.7

    general_system = r""" 
    Welcome to the Mercedes-Benz AutoWhiz, your expert AI for Mercedes-Benz vehicles!

    As your personal EV consultant, I'm dedicated to guiding you through our exceptional range of electric vehicles. My aim is to understand your specific needs and preferences to recommend the perfect Mercedes-Benz EV that aligns with your lifestyle and aspirations. 

    Please note that our discussions will solely focus on Mercedes-Benz vehicles. I am specifically designed not to engage in discussions about competitor brands or non-electric models.

    Given the context below, please provide a concise answer to the inquiry, and I will follow up with the best Mercedes-Benz EV options tailored to your needs.

    ----
    {context}
    ----
    """


    general_user = "User Question:\n```\n{question}\n```"

    messages = [
        SystemMessage(content=("You are an expert AI Sales Manager for Mercedes-Benz electric vehicles! As a personal EV consultant, you are dedicated to guiding users through the exceptional range of electric vehicles, focusing on sustainability, advanced technology, and unparalleled luxury. Your aim is to understand specific needs to recommend the perfect Mercedes-Benz EV that aligns with users' lifestyles. Please note that discussions are focused exclusively on Mercedes-Benz vehicles.")),        
        SystemMessagePromptTemplate.from_template(general_system),
        HumanMessagePromptTemplate.from_template(general_user),
    ]

    qa_prompt = ChatPromptTemplate.from_messages(messages)

    # Initialize the chat model
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    # Initialize memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create the conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={'prompt': qa_prompt}
    )

    return conversation_chain

@app.route('/', methods=['GET', 'POST'])
def index():
    json_filepath = "ev_vehicles.json"
    csv_filepath = "ev_vehicles.csv"
    df = load_data(json_filepath, csv_filepath)
    if df.empty:
        return render_template('index.html')

    vectorstore = get_vectorstore(df)

    # Recreate the conversation chain for each request
    conversation_chain = get_conversation_chain(vectorstore)

    if request.method == 'POST':
        user_question = request.form.get('user_question')
        response = handle_userinput(user_question, conversation_chain)
        return render_template('index.html', response=response, user_question=user_question)

    return render_template('index.html')

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('chat_history', None)  # This removes the chat history from the session
    return redirect('/')  # Redirects back to the main index page

def handle_userinput(user_question, conversation_chain):
    # Ensure chat history is initialized
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Generate response from the conversational chain
    response = conversation_chain.invoke({'question': user_question})

    # Prepare a serializable format of the response, e.g., extracting just the textual response
    response_text = [msg.content for msg in response['chat_history'] if hasattr(msg, 'content')]

    # Flatten the chat history and update session
    session['chat_history'].extend(response_text)  # Use extend to add new messages to the flat list

    # Ensure to commit session changes
    session.modified = True

    return response_text

if __name__ == '__main__':
    app.run(debug=True)