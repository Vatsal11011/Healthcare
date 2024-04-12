import asyncio
import websockets
import backEndResult as BER
import getDoctors as GD
import json  # Import the json module

def get_details_about_disease(data):
    dis_name = BER.returnDiseaseName([data])
    dis_descip = BER.returnDiseaseDescription(dis_name)
    dis_precau = BER.returnDiseasePrecaution(dis_name)
    Output1 = "You seem to be suffering from " + dis_name
    Output2 = dis_descip
    Output3 = [f"{i + 1}.{precaution}" for i, precaution in enumerate(dis_precau)]
    dis_group,ListDoc = GD.get_doc_details(dis_name)
    Output3 = [f"{i + 1}.{precaution}" for i, precaution in enumerate(dis_precau)]
    dis_group, ListDoc = GD.get_doc_details(dis_name)
    temp_O = [f"⚫{doc['Name']} ({dis_group}), Contact No: {doc['Contact']}" for i, doc in enumerate(ListDoc)]

    return Output1, Output2, Output3,temp_O
async def receive_data(websocket, path):
    data = await websocket.recv()
    refined_data = [char for char in data if char.isdigit()]
    o1, o2, o3,o4 = get_details_about_disease(refined_data)

    # Create a dictionary to send as JSON
    output_dict = {'output1': o1, 'output2': o2, 'output3': o3,'output4':o4}
    
    # Convert the dictionary to a JSON-formatted string
    output_json = json.dumps(output_dict)
    print(output_json)
    await websocket.send(output_json)

start_server = websockets.serve(receive_data, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
