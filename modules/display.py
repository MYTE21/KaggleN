def handle_response_display(response, placeholder):
    full_response = ""

    if hasattr(response, "__iter__") and not isinstance(response, str):
        for chunk in response:
            full_response += str(chunk)
            if full_response.count("```") % 2 == 0:
                placeholder.markdown(full_response + "▌")
            else:
                placeholder.markdown(full_response)

        placeholder.markdown(full_response)
    else:
        full_response = str(response)
        placeholder.markdown(full_response)

    return full_response