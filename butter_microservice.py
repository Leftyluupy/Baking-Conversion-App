# butter: 225, 227, 230g per cup
# butter: 14, 16, 17g per tablespoon??

import zmq
import json

context = zmq.Context()
butter_socket = context.socket(zmq.REP)
butter_socket.bind("tcp://*:4444")

while True:

    # receive & dissect
    received_butter_dict = butter_socket.recv()
    received_butter_dict = json.loads(received_butter_dict)
    unit_type = received_butter_dict["Unit"]
    amount_multiplier = received_butter_dict["Amount"]

    # perform conversion
    if unit_type == "Cup":
        butter_in_grams = amount_multiplier * 225
    if unit_type == "Tablespoon":
        butter_in_grams = amount_multiplier * 14
    butter_in_grams = int(butter_in_grams)

    # Create dictionary & send back
    temp_dict = {received_butter_dict["Ingredient"]: butter_in_grams}
    temp_dict = json.dumps(temp_dict)
    butter_socket.send_string(temp_dict)
