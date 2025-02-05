from ai_agent.youtube_agent import run_agent

def main():
    user_query = input("Enter your search query: ")
    result = run_agent(user_query)
    print(result)

if __name__ == "__main__":
    main()