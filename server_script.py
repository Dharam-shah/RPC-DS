from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import requests
import os

# Checking if the XML file exists or not; if not, creating one notes.xml file
xml_file = 'notes.xml'
if not os.path.exists(xml_file):
    root = ET.Element("data")
    tree = ET.ElementTree(root)
    tree.write(xml_file)

# Load the XML database
tree = ET.parse(xml_file)
root = tree.getroot()

# Get user input
def user_input(topic, note, text, timestamp):
    # Checking if the topic already exists in the XML db
    topic_exists = False
    for topic_element in root.findall(".//topic"):
        name_attribute = topic_element.get('name')

        if name_attribute == topic:
            topic_exists = True
            # Appending data to existing topic
            new_note = ET.SubElement(topic_element, 'note')
            new_note.set('name', note)

            new_text = ET.SubElement(new_note, 'text')
            new_text.text = text

            new_time = ET.SubElement(new_note, 'timestamp')
            new_time.text = timestamp
            break

    # If the topic doesn't exist, adding new topic 
    if not topic_exists:
        topic_element = ET.SubElement(root, 'topic')
        topic_element.set("name", topic)

        note_element = ET.SubElement(topic_element, 'note')
        note_element.set("name", note)

        text_element = ET.SubElement(note_element, 'text')
        text_element.text = text

        time_element = ET.SubElement(note_element, 'timestamp')
        time_element.text = timestamp

    # Saving data in XML db
    root_tree = ET.ElementTree(root)
    ET.indent(root_tree, "    ")    
    tree.write('notes.xml')
    return "New topic added successfully."

def get_contents(topic):
    # Search for the topic in the XML db
    for topic_element in root.findall(".//topic"):
        name_attribute = topic_element.get('name')

        if name_attribute == topic:
            notes = topic_element.findall(".//note")
            if notes:
                return "\n".join(note.find('text').text for note in notes)
            else:
                return f"No notes found for topic '{topic}'."

    return f"Topic '{topic}' not found."

def query_wikipedia(search_keyword):
    # Query Wikipedia API using the MediaWiki endpoint
    endpoint = "https://www.mediawiki.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": search_keyword,
        "format": "json"
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    # Extracting the suitable result from the data
    if data[1]:
        result = data[1][0]

        # Information from Wikipedia
        wikipedia_info = f"Link to Wikipedia article: {result}"

        # Return the Wikipedia information
        return wikipedia_info
    else:
        return f"No Wikipedia article found for '{search_keyword}'."


# Register functions
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(user_input, 'user_input')
server.register_function(get_contents, 'get_contents')
server.register_function(query_wikipedia, 'query_wikipedia')

print("Server listening on port 8000...")
server.serve_forever()

