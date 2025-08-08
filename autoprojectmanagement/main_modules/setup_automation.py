class SetupAutomation:
    def __init__(self):
        pass

    def get_standard_response(self, question):
        # Provide standard responses for common setup questions
        standard_responses = {
            "What is the git flow used in this project?": "main",
            "What naming conventions should be followed?": "Use lowercase with hyphens for branches and snake_case for files."
        }
        
        # Ensure question is a string
        if not isinstance(question, str):
            return "No standard response available."
            
        return standard_responses.get(question, "No standard response available.")

    def run(self):
        print("SetupAutomation mock run method called.")
