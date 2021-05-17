#%%
import base64
message = open("cipher2.txt").read()

while True:
    try:
        message = base64.b64decode(message)
    except Exception:
        break

print(bytes.decode(message))
# %%
