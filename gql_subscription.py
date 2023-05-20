from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport


transport = WebsocketsTransport(url='ws://127.0.0.1:8000/graphql')


client = Client(
    transport=transport,
    fetch_schema_from_transport=False,  # for an unknown reason it is important
)


query = gql("""
subscription Actions { 
  liveActions {
    name
  } 
}
""")


for result in client.subscribe(query):
    print(result)
