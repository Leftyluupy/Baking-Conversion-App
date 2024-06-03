# weak flour: 140g per cup of AP flour (need to test and verify this)
# strong flour: 125g per cup of AP flour
# ap flour: 125g per cup AP flour (straight conversion, no flour type change)

import zmq
import json

context = zmq.Context()
flour_socket = context.socket(zmq.REP)
flour_socket.bind("tcp://*:3333")

while True:

    # receive & dissect
    received_flour_dict = flour_socket.recv()
    received_flour_dict = json.loads(received_flour_dict)
    unit_type = received_flour_dict["Unit"]
    amount_multiplier = received_flour_dict["Amount"]

    # perform conversion
    if unit_type == "Cup":
        strong_flour_in_grams = amount_multiplier * 125
        strong_flour_in_grams = int(strong_flour_in_grams)
        weak_flour_in_grams = amount_multiplier * 140
        weak_flour_in_grams = int(weak_flour_in_grams)

    # Create dictionary & send back
    temp_dict = {"Flour: Strong": strong_flour_in_grams,
                 "Flour: Weak": weak_flour_in_grams}
    temp_dict = json.dumps(temp_dict)
    flour_socket.send_string(temp_dict)
