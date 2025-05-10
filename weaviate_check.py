import weaviate
from weaviate.classes.init import AdditionalConfig

client = weaviate.connect_to_custom(
http_host="localhost",
    http_port=8080,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False,
    #additional_config=AdditionalConfig(timeout=30)
)
try:
    results = client.collections.get("DocChunk").query.fetch_objects().with_limit(100).with_properties(["title", "text", "url", "tags", "created_at"]).do()

    # Print retrieved objects
    for obj in results.objects:
        print("Title:", obj.properties.get('title'))
        print("Text:", obj.properties.get('text')[:100], "...")
        print("URL:", obj.properties.get('url'))
        print("Tags:", obj.properties.get('tags'))
        print("Created At:", obj.properties.get('created_at'))
        print("=" * 50)

except AttributeError as e:
    print(e)

finally:
    client.close()

# results = client.collections.get("DocChunk").query.bm25().with_limit(5).with_properties(["title", "text", "url"]).do()
#
# for obj in results.objects:
#     print("Title:", obj.properties['title'])
#     print("Text:", obj.properties['text'][:100], "...")
#     print("URL:", obj.properties['url'])
#     print("=" * 40)
#
