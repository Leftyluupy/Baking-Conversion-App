# peanut butter: 270g per cup

import zmq
import json

context = zmq.Context()
peanut_butter_socket = context.socket(zmq.REP)
peanut_butter_socket.bind("tcp://*:7777")

while True:

    # receive & dissect
    received_PB_dict = peanut_butter_socket.recv()
    received_PB_dict = json.loads(received_PB_dict)
    unit_type = received_PB_dict["Unit"]
    amount_multiplier = received_PB_dict["Amount"]

    # perform conversion
    if unit_type == "Cup":
        peanut_butter_in_grams = amount_multiplier * 270
    if unit_type == "Tablespoon":
        peanut_butter_in_grams = amount_multiplier * 16.875
    peanut_butter_in_grams = int(peanut_butter_in_grams)

    # Create dictionary & send back
    temp_dict = {received_PB_dict["Ingredient"]: peanut_butter_in_grams}
    temp_dict = json.dumps(temp_dict)
    peanut_butter_socket.send_string(temp_dict)
