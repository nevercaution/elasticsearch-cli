# elasticsearch_cli
elasticsearch cli tools.  

## Usage

Execution command. Usage is simple.  

```
$ ./bin/elasticsearch-cli  

# if you wnat to specific host
$ ./bin/elasticsearch-cli -host YOUR_HOST

# if you wnat to specific port
$ ./bin/elasticsearch-cli -port YOUR_PORT

# both also possible
$ ./bin/elasticsearch-cli -host YOUR_HOST -port YOUR_PORT
```

run `elasticsearch-cli` your specific host and port.    
then you will be show this message by command line.  

```
$ ./bin/elasticsearch-cli
uri :  http://127.0.0.1:9200/
{
  "name" : "DGX0yu1",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "xxxxxxxxxxxxxxx",
  "version" : {
    "number" : "6.2.2",
    "build_hash" : "10b1edd",
    "build_date" : "2018-02-16T19:01:30.685723Z",
    "build_snapshot" : false,
    "lucene_version" : "7.2.1",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```
  
## Commands  

**All commands are separated by spaces.**  
Currently, we can only handle simple commands, and we will add more features in the future.  
These are the commands that can be processed at this time.  

* `cat`  
The cat command is useful in elasticsearch.  
This is the same method used by elasticsearch.  
See here [cat method](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html)   

```
=^.^=
/_cat/allocation
/_cat/shards
/_cat/shards/{index}
/_cat/master
/_cat/nodes
/_cat/tasks
/_cat/indices
/_cat/indices/{index}
/_cat/segments
/_cat/segments/{index}
/_cat/count
/_cat/count/{index}
/_cat/recovery
/_cat/recovery/{index}
/_cat/health
/_cat/pending_tasks
/_cat/aliases
/_cat/aliases/{alias}
/_cat/thread_pool
/_cat/thread_pool/{thread_pools}
/_cat/plugins
/_cat/fielddata
/_cat/fielddata/{fields}
/_cat/nodeattrs
/_cat/repositories
/_cat/snapshots/{repository}
/_cat/templates
```

also you can use like this.  
 
```
> cat health
1528363373 18:22:53 elasticsearch yellow 1 1 5 5 0 0 5 0 - 50.0%
```

* `info`   
The custom method. 
Show information on elasticsearch.  
Shows the message you were connected to the first time.  

* `match_all`  
The match_all method of elasticsearch. 
You can optionally use the from and size parameters.  
usage is as follows.  
See here [match_all method](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-all-query.html)  

```
> match_all twitter 
{
    "timed_out": false,
    "_shards": {
        "skipped": 0,
        "total": 5,
        "successful": 5,
        "failed": 0
    },
    "took": 19,
    "hits": {
        "total": 1,
        "hits": [
            {
                "_id": "1",
                "_index": "twitter",
                "_source": {
                    "user": "kimchy",
                    "post_date": "2009-11-15T14:12:12",
                    "message": "trying out Elasticsearch"
                },
                "_type": "_doc",
                "_score": 1.0
            }
        ],
        "max_score": 1.0
    }
}
```

* `match`  
The match method of elasticsearch. 
Requires `document` and `value` as parameters.  
See here [match method](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html)    

```
> match twitter user kimchy
{
    "timed_out": false,
    "_shards": {
        "skipped": 0,
        "total": 5,
        "successful": 5,
        "failed": 0
    },
    "took": 2,
    "hits": {
        "total": 1,
        "hits": [
            {
                "_id": "1",
                "_index": "twitter",
                "_source": {
                    "user": "kimchy",
                    "post_date": "2009-11-15T14:12:12",
                    "message": "trying out Elasticsearch"
                },
                "_type": "_doc",
                "_score": 0.2876821
            }
        ],
        "max_score": 0.2876821
    }
}
```

* `delete API`  
The delete API in elasticsearch.  
Requires a document to be deleted as a parameter.  
See here [delete API method](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html)    


* `get API`    
The get API in elasticsearch.  
See here [get API method](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html)

```
> get twitter _doc 1
{
    "_id": "1",
    "_index": "twitter",
    "_source": {
        "user": "kimchy",
        "post_date": "2009-11-15T14:12:12",
        "message": "trying out Elasticsearch"
    },
    "_type": "_doc",
    "found": true,
    "_version": 1
}
```