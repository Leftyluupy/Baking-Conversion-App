# cocoa powder: 130g per cup

import zmq
import json

context = zmq.Context()
cocoa_powder_socket = context.socket(zmq.REP)
cocoa_powder_socket.bind("tcp://*:4545")

while True:

    # receive & dissect
    received_cocoa_powder_dict = cocoa_powder_socket.recv()
    received_cocoa_powder_dict = json.loads(received_cocoa_powder_dict)
    unit_type = received_cocoa_powder_dict["Unit"]
    amount_multiplier = received_cocoa_powder_dict["Amount"]

    # perform conversion
    if unit_type == "Cup":
        cocoa_powder_in_grams = amount_multiplier * 130
    if unit_type == "Tablespoon":
        cocoa_powder_in_grams = amount_multiplier * 8.125
    cocoa_powder_in_grams = int(cocoa_powder_in_grams)

    # Create dictionary & send back
    temp_dict = {received_cocoa_powder_dict["Ingredient"]:
                 cocoa_powder_in_grams}
    temp_dict = json.dumps(temp_dict)
    cocoa_powder_socket.send_string(temp_dict)
