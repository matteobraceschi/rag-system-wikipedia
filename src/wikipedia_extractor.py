import wikipediaapi
from langchain.schema import Document

# Initialize the Wikipedia object for English
USER_AGENT = 'MyWikipediaExtractor/1.0 (luca_romaschi@gmail.com)'
WIKI_LANGUAGE = 'en'

wiki = wikipediaapi.Wikipedia(language=WIKI_LANGUAGE, user_agent=USER_AGENT) 

def extract_page_content(page_title):
    """Extracts the content of a Wikipedia page given its title."""
    page = wiki.page(page_title)
    
    if page.exists():
        print(f"Page Title: {page.title}")
        print(f"Page URL: {page.fullurl}")
        return page.text
    else:
        print(f"The page '{page_title}' does not exist.")
        return None

def get_contents(page_titles):
    """Extracts content from a list of Wikipedia pages and returns them as Document objects."""
    documents = []
    for title in page_titles:
        content = extract_page_content(title)
        if content:
            # Create a Document object with the content and metadata
            documents.append(Document(page_content=content, metadata={"title": title}))
    return documents
