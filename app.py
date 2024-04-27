from flask import Flask, redirect, request, render_template, session
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd
from langchain.globals import set_verbose
import json
import os
from openai import OpenAI
from langchain.prompts.prompt import PromptTemplate
from pandas import json_normalize

set_verbose(False)

load_dotenv()
app = Flask(__name__)
app.secret_key = 'nader'

def load_data(json_filepath):
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

    # Updated template to correctly use `context` as a variable.
    qa_template = """
        You are AutoWhiz, the AI assistant specializing in Mercedes-Benz marketing and sales. Your role is to guide customers toward selecting the ideal Mercedes-Benz electric vehicle that aligns with their needs.

        User Profile and Preferences:
        {context}

        User Question:
        {question}

        Start by engaging with the customer to understand their specific requirements for a new car. Inquire about their preferences, such as desired features, color, and budget.

        Throughout the conversation, tactfully steer the discussion towards the benefits of electric vehicles. Emphasize the advantages of choosing an electric model, particularly focusing on Mercedes-Benz’s range of electric vehicles.

        Ensure your responses are succinct and engaging, maintaining a friendly and conversational tone. Avoid sounding mechanical or overly scripted.

        Your primary focus should be on showcasing the unique attributes of Mercedes-Benz electric vehicles without referencing competitors.

        Now, how may I assist you today with your transition to an eco-friendly driving experience?
    """

    # Define the PromptTemplate with the correct variables to use in the template
    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context", "question"])

    # Initialize the chat model
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    # Initialize memory
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    # Create the conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={'prompt': QA_PROMPT}
    )

    return conversation_chain

@app.route('/', methods=['GET', 'POST'])
def index():
    json_filepath = "ev_vehicles.json"
    df = load_data(json_filepath)
    if df.empty:
        return render_template('index.html')

    vectorstore = get_vectorstore(df)

    # Recreate the conversation chain for each request
    conversation_chain = get_conversation_chain(vectorstore)

    if request.method == 'POST':
        user_question = request.form.get('user_question')
        user_profile = request.form.get('user_profile')  # Get the selected user profile from the form
        response = handle_userinput(user_question, conversation_chain, user_profile)
        return render_template('index.html', response=response, user_question=user_question, user_profile=user_profile)

    return render_template('index.html')

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('chat_history', None)  # This removes the chat history from the session
    return redirect('/')  # Redirects back to the main index page

def load_user_profile(profile_name):
    json_filepath = f"personas/{profile_name}.json"
    try:
        with open(json_filepath, 'r') as file:
            user_profile_data = json.load(file)
        return user_profile_data
    except FileNotFoundError:
        return {}

def create_profile_description(user_profile_data):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Convert user_profile_data to a string description, removing JSON structure and unnecessary whitespaces
    profile_description = json.dumps(user_profile_data, separators=(',', ':'))
    
    # Remove the leading and trailing curly braces
    profile_description = profile_description[1:-1]

    # Prepare the messages for the API call
    messages = [
        {"role": "system", "content": "You are an intelligent assistant. Please summarize the following user profile in a concise manner."},
        {"role": "user", "content": profile_description}
    ]
    
    try:
        # API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        # Extract and return the response content
        response_message = response['choices'][0]['message']['content']
        return response_message.strip()
    except Exception as e:
        print(f"Failed to generate profile description: {e}")
        return "Error in generating profile description."

def handle_userinput(user_question, conversation_chain, user_profile):
    user_profile_data = load_user_profile(user_profile)
    # print name
    print(f"User: {user_profile_data.get('Name', '[name not specified]')}")
    
    # Ensure chat history is initialized
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Prepare a descriptive summary of the user profile data
    user_description = create_profile_description(user_profile_data)
    print(user_description)

    # Combine the user profile description with the user question
    combined_input = f"User Profile - {user_description} | User Question - {user_question}"

    # Generate response from the conversational chain using the combined input
    response = conversation_chain.invoke({'question': combined_input})

    # Prepare a serializable format of the response, e.g., extracting just the textual response
    response_text = [msg.content for msg in response['chat_history'] if hasattr(msg, 'content')]

    # Flatten the chat history and update session
    session['chat_history'].extend(response_text)  # Use extend to add new messages to the flat list

    # Ensure to commit session changes
    session.modified = True

    return response_text

if __name__ == '__main__':
    app.run(debug=True)