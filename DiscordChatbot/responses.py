def get_response(message: str) -> str:

    if message.isdigit():
        return str(int(message) + 1)
    
    return 'I didn\'t understand what you wrote. Try typing "!help".'
