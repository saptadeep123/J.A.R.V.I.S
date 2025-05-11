import re

#extracting youtube terms...
def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None


#removing unwanted keywords...
def removewords(input_string , words_to_remove):
    words = input_string.split()

    filtered_words= [word for word in words if word.lower() not in words_to_remove]

    result_string = ' '.join(filtered_words)

    return result_string

#cheacking
#input_string = "make a phone call to pappa"
#words_to_remove = ['make', 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', '']

#result = removewords(input_string, words_to_remove)
#print(result)

