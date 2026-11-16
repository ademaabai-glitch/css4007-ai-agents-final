"""First working request. Run:  python src/first_request.py "I need a bouquet for tomorrow" """
import sys

from llm import make_llm, ask

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "I need a bouquet under 15000 tenge for tomorrow."
    print(ask(make_llm(), text))
