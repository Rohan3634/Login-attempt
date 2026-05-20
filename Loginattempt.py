import time

# Simulated database of registered users: { "username": "correct_password" }
USER_DB = {
    "alice": "secret123",
    "bob": "password321"
}

# Configuration settings
MAX_ATTEMPTS = 3          # Total allowed failures before lockout
LOCKOUT_DURATION = 10     # How long the user is locked out (in seconds)

# Live system tracker: { "username": { "failures": int, "lockout_until": float } }
login_tracker = {}

def get_tracker(username):
    """Retrieves or initializes the failure tracking state for a user."""
    if username not in login_tracker:
        login_tracker[username] = {"failures": 0, "lockout_until": 0.0}
    return login_tracker[username]

def login_user(username, password):
    """Processes a login attempt with built-in brute-force defense."""
    current_time = time.time()
    
    # 1. Check if the user exists in our database
    if username not in USER_DB:
        print(f"❌ Login Failed: User '{username}' does not exist.")
        return False
        
    user_state = get_tracker(username)
    
    # 2. Safety Check: Is the account currently restricted?
    if current_time < user_state["lockout_until"]:
        remaining_time = int(user_state["lockout_until"] - current_time)
        print(f"🛑 ACCESS DENIED: Account locked due to repeated failures. Try again in {remaining_time} seconds.")
        return False

    # 3. Process Password validation
    if password == USER_DB[username]:
        # Success! Reset the failure counter entirely
        user_state["failures"] = 0
        print(f"✅ Success: Welcome back, {username}!")
        return True
    else:
        # Failure. Increment the strike counter
        user_state["failures"] += 1
        strikes_left = MAX_ATTEMPTS - user_state["failures"]
        
        print(f"❌ Login Failed: Incorrect password.")
        
        # 4. Trigger restriction if threshold breached
        if user_state["failures"] >= MAX_ATTEMPTS:
            user_state["lockout_until"] = current_time + LOCKOUT_DURATION
            print(f"🚨 ALERT: {MAX_ATTEMPTS} failed attempts reached. User '{username}' is restricted for {LOCKOUT_DURATION} seconds.")
        else:
            print(f"⚠️ Warning: {strikes_left} attempts remaining before account restriction.")
            
        return False

# --- Demonstration Workflow ---
if __name__ == "__main__":
    target_user = "alice"
    
    print("--- Starting Login System Simulation ---")
    print(f"Target account: '{target_user}' (Max strikes: {MAX_ATTEMPTS}, Lockout: {LOCKOUT_DURATION}s)")
    print("-" * 40)
    
    # Attempt 1: Wrong password
    login_user(target_user, "wrong_pass_1")
    
    # Attempt 2: Wrong password
    login_user(target_user, "wrong_pass_2")
    
    # Attempt 3: Wrong password (This triggers the lockout)
    login_user(target_user, "wrong_pass_3")
    
    print("\n--- Testing the Lockout Restriction ---")
    # Attempt 4: Even the CORRECT password should fail now because of the restriction
    login_user(target_user, "secret123")
    
    print(f"\n--- Sleeping for {LOCKOUT_DURATION} seconds to let restriction expire... ---")
    time.sleep(LOCKOUT_DURATION + 1)
    
    print("\n--- Testing Access Restoration ---")
    # Attempt 5: Trying the correct password again after the restriction timer drops
    login_user(target_user, "secret123")