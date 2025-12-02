def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted_char
        else:
            result += char
    return result

# Example usage
plaintext = "Hi my name is derick decesare and my great grandfather invented the cyper"
shift = 2
encoded_text = caesar_cipher(plaintext, shift)
print("Encoded text:", encoded_text)