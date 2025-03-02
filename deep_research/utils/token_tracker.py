def initialize_trackers():
    """Initialize token and cost trackers"""
    print("Initializing token and cost trackers...")
    input_token_tracker = 0
    output_token_tracker = 0
    print("Current token count: (for the run of this script)", input_token_tracker + output_token_tracker)
    print("Current script running cost: $0 (₹0)")
    print("Trackers initialized successfully")
    return input_token_tracker, output_token_tracker

def update_and_display_metrics(input_token_tracker, output_token_tracker, model):
    """Update and display token usage metrics and cost"""
    # print("\n--- Updating Metrics ---")
    total_tokens = input_token_tracker + output_token_tracker
    
    if model == "mini":
        mini_input_cost = 0.15  # per million tokens
        mini_output_cost = 0.60  # per million tokens
    elif model == "o1":
        mini_input_cost = 3.30  # per million tokens
        mini_output_cost = 13.20  # per million tokens

    # print(f"Input tokens used: {input_token_tracker}")
    # print(f"Output tokens used: {output_token_tracker}")

        # For mini deployment
    mini_input_cost_total = (input_token_tracker / 1_000_000) * mini_input_cost
    mini_output_cost_total = (output_token_tracker / 1_000_000) * mini_output_cost
    
    # Total cost combining both models
    current_cost =  mini_input_cost_total + mini_output_cost_total
    
    # Convert to rupees (1 USD = 87 INR)
    current_cost_inr = current_cost * 87
    
    return current_cost_inr