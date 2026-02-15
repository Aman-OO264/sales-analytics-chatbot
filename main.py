from genai_engine import classify_user_query
from query_engine import execute_query
SUGGESTED_QUESTIONS = [

    # 🔥 Sales Based
    "Show total sales for 2022",
    "Show total sales for 2023",
    "Compare sales between 2022 and 2023",
    "Show monthly sales trend for 2022",
    "Show Q1 2022 sales",

    # 🏆 Product Ranking
    "Top 5 products by revenue",
    "Top 3 products in 2023",
    "Which product generated highest sales?",

    # 👥 Customer
    "Total unique customers"
]

if __name__ == "__main__":
    print("🚀 Sales Analytics Chatbot Started!")
    print("Type 'exit' anytime to quit.\n")

    while True:
        print("\n💡 Suggested Questions:")
        for i, q in enumerate(SUGGESTED_QUESTIONS, 1):
            print(f"{i}. {q}")

        choice = input("\nEnter question number OR type your own question: ")

        if choice.lower() == "exit":
            print("👋 Exiting chatbot. Goodbye!")
            break

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(SUGGESTED_QUESTIONS):
                user_query = SUGGESTED_QUESTIONS[index]
            else:
                print("❌ Invalid selection.")
                continue
        else:
            user_query = choice

        # 👇 THESE MUST BE INSIDE THE LOOP (8 spaces total)
            intent_data = classify_user_query(user_query)

        print("\n🧠 GPT Intent Output:")
        print(intent_data)

        try:
            print("DEBUG: Entering DB execution")
            db_result = execute_query(intent_data)

            print("\n📊 Business Result:")

            if isinstance(db_result, list):
                for row in db_result:
                    print(row)
            else:
                print(db_result)

        except Exception as e:
            print("\n❌ Database Error:")
            print(e)