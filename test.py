

def update_addresses():
  with open("addresses.json", "w") as f:
     json.dump(whitelisted, f)