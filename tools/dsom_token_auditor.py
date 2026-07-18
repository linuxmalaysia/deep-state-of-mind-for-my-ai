import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Counts tokens using tiktoken (a proxy for modern LLMs)."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        print(f"Error counting tokens: {e}")
        return 0

def generate_bloated_context() -> str:
    """Simulates a non-DSOM 'Bloated' context load."""
    chat_history = "User: How do I clone the project?\nAI: You can clone the project by running git clone... " * 100
    file_content = """
    # START-HERE.md
    Welcome to the Deep State of Mind... 
    (Simulating a full 500-line markdown file load for every prompt)
    """ * 10
    conversational_fluff = "Sure! I would be absolutely delighted to assist you with that request today. Here is the information you asked for: "
    return chat_history + file_content + conversational_fluff

def generate_dsom_context() -> str:
    """Simulates an optimized DSOM context load using Episodic Resumes and Progressive Disclosure."""
    episodic_resume = """
    # [DSOM EPISODIC RECORD]
    - Primary Objective: Clone project.
    - Active Blocking Issues: None.
    - Last Completed: Cloned repo.
    """
    progressive_disclosure = """
    SOURCES:
    - [START-HERE.md](file:///START-HERE.md) - Project Entry Points
    - [AGENTS.md](file:///.agents/AGENTS.md) - Sovereign AI Rules
    """
    dense_language = "Repository cloned. Awaiting next command."
    return episodic_resume + progressive_disclosure + dense_language

def main():
    bloated_text = generate_bloated_context()
    dsom_text = generate_dsom_context()

    bloated_tokens = count_tokens(bloated_text)
    dsom_tokens = count_tokens(dsom_text)

    print("--- DSOM Token Efficiency Audit ---")
    print(f"Scenario A (Bloated Context): {bloated_tokens} tokens")
    print(f"Scenario B (DSOM Optimized Context): {dsom_tokens} tokens")
    
    if bloated_tokens > 0:
        savings = ((bloated_tokens - dsom_tokens) / bloated_tokens) * 100
        print(f"Token Reduction: {savings:.2f}%")
        print(f"Absolute Savings: {bloated_tokens - dsom_tokens} tokens per turn")
    else:
        print("Failed to calculate tokens.")

if __name__ == "__main__":
    main()
