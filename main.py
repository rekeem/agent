import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function




load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found in .env")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Enter prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )
    if response.usage_metadata is None:
        raise RuntimeError("usage metadata is missing from response")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        function_call_results=[]
        for function_call in response.function_calls:
            result =call_function(function_call)
            if (not result.parts) or (len(result.parts)==0):
                raise Exception("function call result is missing parts")
            if not result.parts[0].function_response:
                raise Exception("function call result is missing function response")
            if not result.parts[0].function_response.response:
                raise Exception("function call result is missing function response content")
            function_call_results.append(result.parts[0])
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
        print(response.text)


if __name__ == "__main__":
    main()
