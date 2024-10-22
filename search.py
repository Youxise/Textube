
# Function to index the transcription and segments into Elasticsearch
def index_transcription(es, index_name, segments):
    for segment in segments:
        doc = {
            'text': segment['text'],
            'start_time': segment['start'],
            'end_time': segment['end']
        }
        es.index(index=index_name, body=doc)

# Function to search for the sentence in the transcriptions
def search_transcriptions(es, index_name, sentence):
    query = {
        "query": {
            "bool": {
                "should": [
                    # First condition: lower, stop, stem, fuzzy
                    {
                        "multi_match": {
                            "query": sentence,
                            "fields": ["text"],
                            "fuzziness": "AUTO",  # Apply fuzzy matching
                            "analyzer": "custom_analyzer",  # Analyzer with lower, stop, stem
                            "operator": "and"
                        }
                    },
                    # Second condition: lower, fuzzy only
                    {
                        "multi_match": {
                            "query": sentence,
                            "fields": ["text"],
                            "fuzziness": "AUTO",  # Apply fuzzy matching
                            "analyzer": "simple_analyzer",  # Analyzer with lower and fuzzy only
                            "operator": "and"
                        }
                    },
                    # Third condition: Exact match (phrase match)
                    {
                        "match_phrase": {
                            "text": {
                                "query": sentence
                            }
                        }
                    }
                ]
            }
        },
        "highlight": {
            "fields": {
                "text": {
                    "pre_tags": ["<em>"],  # Highlight start tag
                    "post_tags": ["</em>"],  # Highlight end tag
                }
            }
        }
    }

    response = es.search(index=index_name, body=query)
    hits = response['hits']['hits']

    # Collect matching segments with their start and end times
    results = [{"text": hit['_source']['text'], "start_time": hit['_source']['start_time'], "end_time": hit['_source']['end_time'], "highlighted": hit.get('highlight', {}).get('text', [''])[0]} for hit in hits]
    return results

def create_index_with_analyzers(es, index_name):

    index_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "simple_analyzer": {  # Define the simple analyzer here (lowercase only)
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase"
                        ]
                    },
                    "custom_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "stop",
                            "stemmer"  # Use stemming instead of phonetic
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "text": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "start_time": {
                    "type": "float"
                },
                "end_time": {
                    "type": "float"
                }
            }
        }
    }

    # Check if index already exists, if yes, delete it
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    # Create the index with the custom settings and mappings
    es.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' created with custom analyzers.")

    
    # Create the index with the custom settings and mappings
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_body)
        print(f"Index '{index_name}' created with custom analyzers.")
    else:
        print(f"Index '{index_name}' already exists.")

