# white sugar: 200-201g per cup
# brown sugar (packed): 170, 208, 214g per cup???

import zmq
import json

context = zmq.Context()
sugar_socket = context.socket(zmq.REP)
sugar_socket.bind("tcp://*:2222")

while True:

    # receive & dissect
    received_sugar_dict = sugar_socket.recv()
    received_sugar_dict = json.loads(received_sugar_dict)
    unit_type = received_sugar_dict["Unit"]
    amount_multiplier = received_sugar_dict["Amount"]

    # perform conversion
    if unit_type == "Cup":
        sugar_in_grams = amount_multiplier * 200
    if unit_type == "Tablespoon":
        sugar_in_grams = amount_multiplier * 14
    sugar_in_grams = int(sugar_in_grams)

    # Create dictionary & send back
    temp_dict = {received_sugar_dict["Ingredient"]: sugar_in_grams}
    temp_dict = json.dumps(temp_dict)
    sugar_socket.send_string(temp_dict)
