from xmlrpc.client import ServerProxy
import datetime

# Create server proxy
server = ServerProxy('http://localhost:8000/')

def add_note():
    topic = input("Enter the topic: ")
    note = input("Enetr the note: ")
    text = input("Enter the text: ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = server.user_input(topic, note, text, timestamp)
    print(result)

# Get contents from XML database based on a given topic
def get_note():
    search_topic = input("Enter the topic to retrieve: ")
    contents = server.get_contents(search_topic)
    print(contents)

# Name search terms to lookup data on Wikipedia
def wikipedia_search():
    search_keyword = input("Enter a search term for Wikipedia: ")
    result = server.query_wikipedia(search_keyword)

    if "Link to Wikipedia article:" in result:
        topic = input("Enter the existing topic to append the Wikipedia information: ")
        note = "Wikipedia Info"
        text = result
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Caling user_input function on the server to append Wikipedia information
        result = server.user_input(topic, note, text, timestamp)
        print(result)
    else:
        print(result)


# Main function
def main():
    while True:
        print("1. Add New Note\n2. Get Notes by Topic\n3. Search on wikipedia\n4. Exit\n")
        choice = input("Enter the valid choice: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            get_note()
        elif choice == "3":
            wikipedia_search()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

