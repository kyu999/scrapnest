import json
import re


def extract_link(text,
                 ignore_icon=True,
                 ignore_image=True,
                 ignore_external_link=False):
    bold_regions = re.findall('\[\[([^\[\]]*)\]\]', text)
    strong_regions = re.findall('\[(\* [^\[\]]*)\]', text)
    print(strong_regions)
    link_candidates = re.findall('\[([^\[\]]*)\]', text)
    links = []
    for cand in link_candidates:
        print(cand)
        if cand in bold_regions:
            print('bold')
            continue
        if cand in strong_regions:
            print('strong')
            continue
        if ignore_icon and '.icon' in cand:
            print('icon')
            continue
        if ignore_image and 'https://gyazo.com/' in cand:
            print('image')
            continue
        if ignore_external_link and ('http://' in cand or 'http://' in cand):
            print('ext link')
            continue
        links.append(cand)
    return links


def convert_to_d3_format(scrapbox_data,
                         ignore_external_link=True):
    '''
    nodes:
        e.g. {"size": 60, "score": 0.8, "id": "Spathi", "type": "circle"},
        size: #links
        score: 
    links:
        e.g. {"source": 3, "target": 10}
    '''
    page_infos = []
    for page in scrapbox_data['pages']:
        links = []
        for line in page['lines']:
            links_each_line = extract_link(line['text'], ignore_external_link=ignore_external_link)
            if len(links_each_line) > 0:
                links.extend(links_each_line)
        page_infos.append({
            'title': page['title'],
            'created': page['created'],
            'updated': page['updated'],
            'links': links,
            '#lines': len(page['lines'])
        })
    nodes = [{
        'id': page_info['title'],
        'size': len(page_info['links']),
        'score': len(page_info['links']),
        'type': 'circle',
        'links': page_info['links']
    } for page_info in page_infos]
    node_index_mapper = {}
    for i in range(0, len(nodes)):
        node = nodes[i]
        node_index_mapper[node['id']] = i
    links = []
    for node in nodes:
        node_index = node_index_mapper[node['id']]
        for link in node['links']:
            try:
                links.append({
                    'source': node_index,
                    'target': node_index_mapper[link]
                })
            except:
                print('external link lol')
    return {
        'project_name': 'name',
        'exported': scrapbox_data['exported'],
        'nodes': nodes,
        'links': links,
        'page_infos': page_infos
    }