import wikipediaapi

# Create a Wikipedia API object
wiki = wikipediaapi.Wikipedia('en')  # Specify the language edition ('en' for English)

# Prompt the user to enter a query
query = input("Enter your Wikipedia query: ")

# Fetch the Wikipedia page
page = wiki.page(query)

# Check if the page exists
if page.exists():
    # Access the page content
    content = page.text

    # Split the content into paragraphs
    paragraphs = content.split('\n\n')

    # Print the first paragraph as the summary
    summary = paragraphs[0]
    print(f"Summary: {summary}")

    # Print the full page content (limit to one paragraph)
    print(f"Content:\n{paragraphs[0]}")
else:
    print("Page does not exist.")
