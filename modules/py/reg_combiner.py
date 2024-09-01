import base64
import os

input_filename = "combined.txt"
with open(input_filename, 'r') as file:
    encoded_string = file.read().strip()
decoded_bytes = base64.b64decode(encoded_string)
decoded_content = decoded_bytes.decode('utf-8')
print("Decoded content:")
print(decoded_content)
output_folder = os.path.join("..", "reg")
os.makedirs(output_folder, exist_ok=True)
output_filename = os.path.join(output_folder, "go.reg")
decoded_lines = []
for line in decoded_content.splitlines():
    try:
        decoded_line = base64.b64decode(line.strip()).decode('utf-8')
        decoded_lines.append(decoded_line)
    except (base64.binascii.Error, UnicodeDecodeError):
        decoded_lines.append(line)
with open(output_filename, 'w') as reg_file:
    reg_file.write("\n".join(decoded_lines))

print(f"\nDecoded content saved to {output_filename}")
