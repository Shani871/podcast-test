import yaml
import xml.etree.ElementTree as ET
import re

# Register namespaces
ET.register_namespace('itunes', "http://www.itunes.com/dtds/podcast-1.0.dtd")
ET.register_namespace('content', "http://purl.org/rss/1.0/modules/content/")

# Load YAML data
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

# Provide default link_prefix if not present in YAML
link_prefix = yaml_data.get('link', '')  # e.g., 'https://example.com'

# Create the root RSS element with namespaces
rss_element = ET.Element('rss', {
    'version': "2.0",
    'xmlns:itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd",
    'xmlns:content': "http://purl.org/rss/1.0/modules/content/"
})

# Create channel element
channel_element = ET.SubElement(rss_element, 'channel')

# Basic podcast metadata
ET.SubElement(channel_element, 'title').text = yaml_data['title']
ET.SubElement(channel_element, 'itunes:subtitle').text = yaml_data.get('subtitle', '')
ET.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
ET.SubElement(channel_element, 'description').text = yaml_data['description']
ET.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
ET.SubElement(channel_element, 'language').text = yaml_data['language']
ET.SubElement(channel_element, 'link').text = link_prefix or 'https://example.com'
ET.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

# Loop through podcast episodes
for episode in yaml_data['item']:
    item_element = ET.SubElement(channel_element, 'item')
    
    ET.SubElement(item_element, 'title').text = episode['title']
    ET.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    ET.SubElement(item_element, 'description').text = episode['description']
    ET.SubElement(item_element, 'pubDate').text = episode['published']

    # Clean length (remove commas)
    length_clean = re.sub(r'[^\d]', '', str(episode.get('length', '0')))

    # Add enclosure tag
    ET.SubElement(item_element, 'enclosure', {
        'url': link_prefix + episode['file'],
        'length': length_clean,
        'type': yaml_data['format']
    })

    # Add duration
    ET.SubElement(item_element, 'itunes:duration').text = episode.get('duration', '00:00:00')

# Write the XML output
tree = ET.ElementTree(rss_element)
tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)