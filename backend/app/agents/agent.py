from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

from app.rag.vectorstore import rag_answer

load_dotenv()


@tool
def company_policy_search(question: str) -> str:
    """Search the company policy and answer questions using the company knowledge base."""
    return rag_answer(question)

@tool
def get_order_status(order_id: str) -> str:
    """Get the current status of a customer's order using the order ID."""

    if not order_id:
        return "Order ID is required."

    orders = {
        "123": "Your order will be shipped tomorrow.",
        "234": "Your order is cancelled. You will receive a refund.",
        "456": "Your order takes 23 working days to deliver."
    }

    if order_id not in orders:
        return f"Order {order_id} was not found."

    return orders[order_id]


model = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
    max_tokens=256,
    reasoning_effort="none"
)


agent = create_agent(
    model=model,

    tools=[company_policy_search,get_order_status],

    system_prompt="""
You are an AI customer support agent.

Use the company_policy_search tool whenever
the question requires information from company policy.

For simple greetings or general conversation,
answer directly.
"""
)
if __name__ == "__main__":

    question = input("Ask your question: ")

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    print("\n===== MESSAGE FLOW =====")

    for i, message in enumerate(result["messages"], start=1):

        print(f"\n--- MESSAGE {i} ---")
        print("Type:", type(message).__name__)
        print("Content:", message.content)

        if hasattr(message, "tool_calls") and message.tool_calls:
            print("Tool Calls:", message.tool_calls)

    print("\n===== FINAL ANSWER =====")
    print(result["messages"][-1].content)