from utilities.streamer import response_generator


def handle_response_display(response, placeholder):
    full_response = ""

    if isinstance(response, str):
        stream = response_generator(response)
    elif hasattr(response, "__iter__"):
        stream = response
    else:
        stream = response_generator(str(response))

    for chunk in stream:
        full_response += str(chunk)
        if full_response.count("```") % 2 == 0:
            placeholder.markdown(full_response + "▌")
        else:
            placeholder.markdown(full_response)

    placeholder.markdown(full_response)
    return full_response