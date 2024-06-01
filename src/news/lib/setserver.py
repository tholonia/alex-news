import dotenv
import os


def set_server(label):
    dotenv.load_dotenv()
    
    
    
    def update_env(label,prop):
        print(f"updating {label},{prop}")
        
        stored_key = f"x{label}_{prop}"
        stored_val = os.environ[stored_key]
        new_key = f"LIVE_{prop}"

        dotenv.set_key(
            dotenv_path="./.env",
            key_to_set=new_key,
            value_to_set=stored_val,            
        ) 
        
    if os.environ['LIVE_SERVER'] == label:
        print(f"Currently running |{label}|")
    else:
        print(f"Switching servers from |{os.environ['LIVE_SERVER']}| to |{label}|")
        update_env(label,"SERVER")
        update_env(label,"API_BASE_URL")
        update_env(label,"API_KEY")
        update_env(label,"MODEL_NAME")
    return label

