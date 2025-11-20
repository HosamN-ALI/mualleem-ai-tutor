Docs > qdrant_client.qdrant_client module
qdrant_client.qdrant_client module
classQdrantClient(location: Optional[str] = None, url: Optional[str] = None, port: Optional[int] = 6333, grpc_port: int = 6334, prefer_grpc: bool = False, https: Optional[bool] = None, api_key: Optional[str] = None, prefix: Optional[str] = None, timeout: Optional[int] = None, host: Optional[str] = None, path: Optional[str] = None, force_disable_check_same_thread: bool = False, grpc_options: Optional[dict[str, Any]] = None, auth_token_provider: Optional[Union[Callable[[], str], Callable[[], Awaitable[str]]]] = None, cloud_inference: bool = False, local_inference_batch_size: Optional[int] = None, check_compatibility: bool = True, pool_size: Optional[int] = None, **kwargs: Any)[source]
Bases: QdrantFastembedMixin

Entry point to communicate with Qdrant service via REST or gRPC API.

It combines interface classes and endpoint implementation. Additionally, it provides custom implementations for frequently used methods like initial collection upload.

All methods in QdrantClient accept both gRPC and REST structures as an input. Conversion will be performed automatically.

Note

This module methods are wrappers around generated client code for gRPC and REST methods. If you need lower-level access to generated clients, use following properties:

QdrantClient.grpc_points

QdrantClient.grpc_collections

QdrantClient.rest

Note

If you need async, please consider using Async Implementations of QdrantClient.

qdrant_client.async_qdrant_client

Parameters:
location – If “:memory:” - use in-memory Qdrant instance. If str - use it as a url parameter. If None - use default values for host and port.

url – either host or str of “Optional[scheme], host, Optional[port], Optional[prefix]”. Default: None

port – Port of the REST API interface. Default: 6333

grpc_port – Port of the gRPC interface. Default: 6334

prefer_grpc – If true - use gPRC interface whenever possible in custom methods.

https – If true - use HTTPS(SSL) protocol. Default: None

api_key – API key for authentication in Qdrant Cloud. Default: None

prefix – If not None - add prefix to the REST URL path. Example: service/v1 will result in http://localhost:6333/service/v1/{qdrant-endpoint} for REST API. Default: None

timeout – Timeout for REST and gRPC API requests. Default: 5 seconds for REST and unlimited for gRPC

host – Host name of Qdrant service. If url and host are None, set to ‘localhost’. Default: None

path – Persistence path for QdrantLocal. Default: None

force_disable_check_same_thread – For QdrantLocal, force disable check_same_thread. Default: False Only use this if you can guarantee that you can resolve the thread safety outside QdrantClient.

auth_token_provider – Callback function to get Bearer access token. If given, the function will be called before each request to get the token.

check_compatibility – If true - check compatibility with the server version. Default: true

grpc_options – a mapping of gRPC channel options

cloud_inference – If true - do inference of models.Document and other models in Qdrant Cloud. Default: False.

local_inference_batch_size – inference batch size used by fastembed when using local inference with models.Document and other models.

pool_size – connection pool size, Default: None. Default value for gRPC connection pool is 3, rest default is inherited from httpx (default: 100)

**kwargs – Additional arguments passed directly into REST client initialization

batch_update_points(collection_name: str, update_operations: Sequence[Union[UpsertOperation, DeleteOperation, SetPayloadOperation, OverwritePayloadOperation, DeletePayloadOperation, ClearPayloadOperation, UpdateVectorsOperation, DeleteVectorsOperation]], wait: bool = True, ordering: Optional[WriteOrdering] = None, **kwargs: Any) → list[UpdateResult][source]
Batch update points in the collection.

Parameters:
collection_name – Name of the collection

update_operations – List of update operations

wait – Await for the results to be processed. - If true, result will be returned only when all changes are applied - If false, result will be returned immediately after the confirmation of receiving.

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

Returns:
Operation results

clear_payload(collection_name: str, points_selector: Union[list[Union[int, str, uuid.UUID, common_pb2.PointId]], Filter, Filter, PointIdsList, FilterSelector, PointsSelector], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → UpdateResult[source]
Delete all payload for selected points

Parameters:
collection_name – Name of the collection

wait – Await for the results to be processed. - If true, result will be returned only when all changes are applied - If false, result will be returned immediately after the confirmation of receiving.

points_selector – List of affected points, filter or points selector. Example: - points=[1, 2, 3, “cd3b53f0-11a7-449f-bc50-d06310e7ed90”] - points=Filter(must=[FieldCondition(key=’rand_number’, range=Range(gte=0.7))])

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

Returns:
Operation result

close(grpc_grace: Optional[float] = None, **kwargs: Any) → None[source]
Closes the connection to Qdrant

Parameters:
grpc_grace – Grace period for gRPC connection close. Default: None

cluster_collection_update(collection_name: str, cluster_operation: Union[MoveShardOperation, ReplicateShardOperation, AbortTransferOperation, DropReplicaOperation, CreateShardingKeyOperation, DropShardingKeyOperation, RestartTransferOperation, StartReshardingOperation, AbortReshardingOperation, ReplicatePointsOperation], timeout: Optional[int] = None, **kwargs: Any) → bool[source]
collection_exists(collection_name: str, **kwargs: Any) → bool[source]
Check whether collection already exists

Parameters:
collection_name – Name of the collection

Returns:
True if collection exists, False if not

count(collection_name: str, count_filter: Optional[Union[Filter, Filter]] = None, exact: bool = True, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, timeout: Optional[int] = None, **kwargs: Any) → CountResult[source]
Count points in the collection.

Count points in the collection matching the given filter.

Parameters:
collection_name – name of the collection to count points in

count_filter – filtering conditions

exact – If True - provide the exact count of points matching the filter. If False - provide the approximate count of points matching the filter. Works faster.

shard_key_selector – This parameter allows to specify which shards should be queried. If None - query all shards. Only works for collections with custom sharding method.

timeout – Overrides global timeout for this operation. Unit is seconds.

Returns:
Amount of points in the collection matching the filter.

create_collection(collection_name: str, vectors_config: Optional[Union[VectorParams, Mapping[str, VectorParams]]] = None, sparse_vectors_config: Optional[Mapping[str, SparseVectorParams]] = None, shard_number: Optional[int] = None, sharding_method: Optional[ShardingMethod] = None, replication_factor: Optional[int] = None, write_consistency_factor: Optional[int] = None, on_disk_payload: Optional[bool] = None, hnsw_config: Optional[Union[HnswConfigDiff, HnswConfigDiff]] = None, optimizers_config: Optional[Union[OptimizersConfigDiff, OptimizersConfigDiff]] = None, wal_config: Optional[Union[WalConfigDiff, WalConfigDiff]] = None, quantization_config: Optional[Union[ScalarQuantization, ProductQuantization, BinaryQuantization, QuantizationConfig]] = None, timeout: Optional[int] = None, strict_mode_config: Optional[StrictModeConfig] = None, metadata: Optional[Dict[str, Any]] = None, **kwargs: Any) → bool[source]
Create empty collection with given parameters

Parameters:
collection_name – Name of the collection to recreate

vectors_config – Configuration of the vector storage. Vector params contains size and distance for the vector storage. If dict is passed, service will create a vector storage for each key in the dict. If single VectorParams is passed, service will create a single anonymous vector storage.

sparse_vectors_config – Configuration of the sparse vector storage. The service will create a sparse vector storage for each key in the dict.

shard_number – Number of shards in collection. Default is 1, minimum is 1.

sharding_method – Defines strategy for shard creation. Option auto (default) creates defined number of shards automatically. Data will be distributed between shards automatically. After creation, shards could be additionally replicated, but new shards could not be created. Option custom allows to create shards manually, each shard should be created with assigned unique shard_key. Data will be distributed between based on shard_key value.

replication_factor – Replication factor for collection. Default is 1, minimum is 1. Defines how many copies of each shard will be created. Have effect only in distributed mode.

write_consistency_factor – Write consistency factor for collection. Default is 1, minimum is 1. Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact. Have effect only in distributed mode.

on_disk_payload – If true - point`s payload will not be stored in memory. It will be read from the disk every time it is requested. This setting saves RAM by (slightly) increasing the response time. Note: those payload values that are involved in filtering and are indexed - remain in RAM.

hnsw_config – Params for HNSW index

optimizers_config – Params for optimizer

wal_config – Params for Write-Ahead-Log

quantization_config – Params for quantization, if None - quantization will be disabled

timeout – Wait for operation commit timeout in seconds. If timeout is reached - request will return with service error.

strict_mode_config – Configure limitations for the collection, such as max size, rate limits, etc.

metadata – Arbitrary JSON-like metadata for the collection

Returns:
Operation result

create_full_snapshot(wait: bool = True, **kwargs: Any) → Optional[SnapshotDescription][source]
Create snapshot for a whole storage.

Parameters:
wait –

Await for the snapshot to be created.

If true, result will be returned only when the snapshot is created

If false, result will be returned immediately after the confirmation of receiving.

Returns:
Snapshot description

create_payload_index(collection_name: str, field_name: str, field_schema: Optional[Union[PayloadSchemaType, KeywordIndexParams, IntegerIndexParams, FloatIndexParams, GeoIndexParams, TextIndexParams, BoolIndexParams, DatetimeIndexParams, UuidIndexParams, int, PayloadIndexParams]] = None, field_type: Optional[Union[PayloadSchemaType, KeywordIndexParams, IntegerIndexParams, FloatIndexParams, GeoIndexParams, TextIndexParams, BoolIndexParams, DatetimeIndexParams, UuidIndexParams, int, PayloadIndexParams]] = None, wait: bool = True, ordering: Optional[WriteOrdering] = None, **kwargs: Any) → UpdateResult[source]
Creates index for a given payload field. Indexed fields allow to perform filtered search operations faster.

Parameters:
collection_name – Name of the collection

field_name – Name of the payload field

field_schema – Type of data to index

field_type – Same as field_schema, but deprecated

wait –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

Returns:
Operation Result

create_shard_key(collection_name: str, shard_key: Union[int, str], shards_number: Optional[int] = None, replication_factor: Optional[int] = None, placement: Optional[list[int]] = None, **kwargs: Any) → bool[source]
Create shard key for collection.

Only works for collections with custom sharding method.

Parameters:
collection_name – Name of the collection

shard_key – Shard key to create

shards_number – How many shards to create for this key

replication_factor – Replication factor for this key

placement – List of peers to place shards on. If None - place on all peers.

Returns:
Operation result

create_shard_snapshot(collection_name: str, shard_id: int, wait: bool = True, **kwargs: Any) → Optional[SnapshotDescription][source]
Create snapshot for a given shard.

Parameters:
collection_name – Name of the collection

shard_id – Index of the shard

wait –

Await for the snapshot to be created.

If true, result will be returned only when the snapshot is created.

If false, result will be returned immediately after the confirmation of receiving.

Returns:
Snapshot description

create_snapshot(collection_name: str, wait: bool = True, **kwargs: Any) → Optional[SnapshotDescription][source]
Create snapshot for a given collection.

Parameters:
collection_name – Name of the collection

wait –

Await for the snapshot to be created.

If true, result will be returned only when a snapshot is created

If false, result will be returned immediately after the confirmation of receiving.

Returns:
Snapshot description

delete(collection_name: str, points_selector: Union[list[Union[int, str, uuid.UUID, common_pb2.PointId]], Filter, Filter, PointIdsList, FilterSelector, PointsSelector], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → UpdateResult[source]
Deletes selected points from collection

Parameters:
collection_name – Name of the collection

wait –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

points_selector –

Selects points based on list of IDs or filter. Examples:

points=[1, 2, 3, “cd3b53f0-11a7-449f-bc50-d06310e7ed90”]

points=Filter(must=[FieldCondition(key=’rand_number’, range=Range(gte=0.7))])

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

Returns:
Operation result

delete_collection(collection_name: str, timeout: Optional[int] = None, **kwargs: Any) → bool[source]
Removes collection and all it’s data

Parameters:
collection_name – Name of the collection to delete

timeout – Wait for operation commit timeout in seconds. If timeout is reached - request will return with service error.

Returns:
Operation result

delete_full_snapshot(snapshot_name: str, wait: bool = True, **kwargs: Any) → Optional[bool][source]
Delete snapshot for a whole storage.

Parameters:
snapshot_name – Snapshot name

wait –

Await for the snapshot to be deleted.

If true, result will be returned only when the snapshot is deleted

If false, result will be returned immediately after the confirmation of receiving.

Returns:
True if snapshot was deleted

delete_payload(collection_name: str, keys: Sequence[str], points: Union[list[Union[int, str, uuid.UUID, common_pb2.PointId]], Filter, Filter, PointIdsList, FilterSelector, PointsSelector], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → UpdateResult[source]
Remove values from point’s payload

Parameters:
collection_name – Name of the collection

wait –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

keys – List of payload keys to remove

points –

List of affected points, filter or points selector. .. rubric:: Example

points=[1, 2, 3, “cd3b53f0-11a7-449f-bc50-d06310e7ed90”]

points=Filter(must=[FieldCondition(key=’rand_number’, range=Range(gte=0.7))])

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is downn

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

Returns:
Operation result

delete_payload_index(collection_name: str, field_name: str, wait: bool = True, ordering: Optional[WriteOrdering] = None, **kwargs: Any) → UpdateResult[source]
Removes index for a given payload field.

Parameters:
collection_name – Name of the collection

field_name – Name of the payload field

wait –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

Returns:
Operation Result

delete_shard_key(collection_name: str, shard_key: Union[int, str], **kwargs: Any) → bool[source]
Delete shard key for collection.

Only works for collections with custom sharding method.

Parameters:
collection_name – Name of the collection

shard_key – Shard key to delete

Returns:
Operation result

delete_shard_snapshot(collection_name: str, shard_id: int, snapshot_name: str, wait: bool = True, **kwargs: Any) → Optional[bool][source]
Delete snapshot for a given shard.

Parameters:
collection_name – Name of the collection

shard_id – Index of the shard

snapshot_name – Snapshot id

wait –

Await for the snapshot to be deleted.

If true, result will be returned only when the snapshot is deleted

If false, result will be returned immediately after the confirmation of receiving.

Returns:
True if snapshot was deleted

delete_snapshot(collection_name: str, snapshot_name: str, wait: bool = True, **kwargs: Any) → Optional[bool][source]
Delete snapshot for a given collection.

Parameters:
collection_name – Name of the collection

snapshot_name – Snapshot id

wait –

Await for the snapshot to be deleted.

If true, result will be returned only when the snapshot is deleted

If false, result will be returned immediately after the confirmation of receiving.

Returns:
True if snapshot was deleted

delete_vectors(collection_name: str, vectors: Sequence[str], points: Union[list[Union[int, str, uuid.UUID, common_pb2.PointId]], Filter, Filter, PointIdsList, FilterSelector, PointsSelector], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → UpdateResult[source]
Delete specified vector from the collection. Does not affect payload.

Parameters:
collection_name (str) – Name of the collection to delete vector from

vectors – List of names of the vectors to delete. Use “” to delete the default vector. At least one vector should be specified.

points (Point) –

Selects points based on list of IDs or filter Examples:

points=[1, 2, 3, “cd3b53f0-11a7-449f-bc50-d06310e7ed90”]

points=Filter(must=[FieldCondition(key=’rand_number’, range=Range(gte=0.7))])

wait (bool) –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

Returns:
Operation result

facet(collection_name: str, key: str, facet_filter: Optional[Union[Filter, Filter]] = None, limit: int = 10, exact: bool = False, consistency: Optional[Union[int, ReadConsistencyType]] = None, timeout: Optional[int] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → FacetResponse[source]
Facet counts for the collection. For a specific payload key, returns unique values along with their counts. Higher counts come first in the results.

Parameters:
collection_name – Name of the collection

key – Payload field to facet

facet_filter – Filter to apply

limit – Maximum number of hits to return

exact – If True - provide the exact count of points matching the filter. If False - provide the approximate count of points matching the filter. Works faster.

consistency –

Read consistency of the search. Defines how many replicas should be queried before returning the result. Values:

int - number of replicas to query, values should present in all queried replicas

’majority’ - query all replicas, but return values present in the majority of replicas

’quorum’ - query the majority of replicas, return values present in all of them

’all’ - query all replicas, and return values present in all replicas

timeout – Overrides global timeout for this search. Unit is seconds.

shard_key_selector – This parameter allows to specify which shards should be queried. If None - query all shards. Only works for collections with custom sharding method.

Returns:
Unique values in the facet and the amount of points that they cover.

get_aliases(**kwargs: Any) → CollectionsAliasesResponse[source]
Get all aliases

Returns:
All aliases of all collections

get_collection(collection_name: str, **kwargs: Any) → CollectionInfo[source]
Get detailed information about specified existing collection

Parameters:
collection_name – Name of the collection

Returns:
Detailed information about the collection

get_collection_aliases(collection_name: str, **kwargs: Any) → CollectionsAliasesResponse[source]
Get collection aliases

Parameters:
collection_name – Name of the collection

Returns:
Collection aliases

get_collections(**kwargs: Any) → CollectionsResponse[source]
Get list name of all existing collections

Returns:
List of the collections

info() → VersionInfo[source]
Returns information about the running Qdrant instance like version and commit id

Returns:
Title, version and optionally commit info

list_full_snapshots(**kwargs: Any) → list[SnapshotDescription][source]
List all snapshots for a whole storage

Returns:
List of snapshots

list_shard_snapshots(collection_name: str, shard_id: int, **kwargs: Any) → list[SnapshotDescription][source]
List all snapshots of a given shard

Parameters:
collection_name – Name of the collection

shard_id – Index of the shard

Returns:
List of snapshots

list_snapshots(collection_name: str, **kwargs: Any) → list[SnapshotDescription][source]
List all snapshots for a given collection.

Parameters:
collection_name – Name of the collection

Returns:
List of snapshots

migrate(dest_client: QdrantBase, collection_names: Optional[list[str]] = None, batch_size: int = 100, recreate_on_collision: bool = False) → None[source]
Migrate data from one Qdrant instance to another.

Parameters:
dest_client – Destination Qdrant instance either in local or remote mode

collection_names – List of collection names to migrate. If None - migrate all collections

batch_size – Batch size to be in scroll and upsert operations during migration

recreate_on_collision – If True - recreate collection on destination if it already exists, otherwise raise ValueError exception

overwrite_payload(collection_name: str, payload: Dict[str, Any], points: Union[list[Union[int, str, uuid.UUID, common_pb2.PointId]], Filter, Filter, PointIdsList, FilterSelector, PointsSelector], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → UpdateResult[source]
Overwrites payload of the specified points After this operation is applied, only the specified payload will be present in the point. The existing payload, even if the key is not specified in the payload, will be deleted.

Examples:

Set payload:

# Overwrite payload value with key `"key"` to points 1, 2, 3.
# If any other valid payload value exists - it will be deleted
qdrant_client.overwrite_payload(
    collection_name="test_collection",
    wait=True,
    payload={
        "key": "value"
    },
    points=[1,2,3]
)
Parameters:
collection_name – Name of the collection

wait –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

payload – Key-value pairs of payload to assign

points –

List of affected points, filter or points selector. .. rubric:: Example

points=[1, 2, 3, “cd3b53f0-11a7-449f-bc50-d06310e7ed90”]

points=Filter(must=[FieldCondition(key=’rand_number’, range=Range(gte=0.7))])

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

Returns:
Operation result

query_batch_points(collection_name: str, requests: Sequence[QueryRequest], consistency: Optional[Union[int, ReadConsistencyType]] = None, timeout: Optional[int] = None, **kwargs: Any) → list[QueryResponse][source]
Perform any search, recommend, discovery, context search operations in batch, and mitigate network overhead

Parameters:
collection_name – Name of the collection

requests – List of query requests

consistency –

Read consistency of the search. Defines how many replicas should be queried before returning the result. Values:

int - number of replicas to query, values should present in all queried replicas

’majority’ - query all replicas, but return values present in the majority of replicas

’quorum’ - query the majority of replicas, return values present in all of them

’all’ - query all replicas, and return values present in all replicas

timeout – Overrides global timeout for this search. Unit is seconds.

Returns:
List of query responses

query_points(collection_name: str, query: Optional[Union[int, str, UUID, PointId, list[float], list[list[float]], SparseVector, NearestQuery, RecommendQuery, DiscoverQuery, ContextQuery, OrderByQuery, FusionQuery, RrfQuery, FormulaQuery, SampleQuery, ndarray[tuple[int, ...], dtype[Union[bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64, float16, float32, float64, longdouble]]], Document, Image, InferenceObject]] = None, using: Optional[str] = None, prefetch: Optional[Union[Prefetch, list[Prefetch]]] = None, query_filter: Optional[Union[Filter, Filter]] = None, search_params: Optional[Union[SearchParams, SearchParams]] = None, limit: int = 10, offset: Optional[int] = None, with_payload: Union[bool, Sequence[str], PayloadSelectorInclude, PayloadSelectorExclude, WithPayloadSelector] = True, with_vectors: Union[bool, Sequence[str]] = False, score_threshold: Optional[float] = None, lookup_from: Optional[Union[LookupLocation, LookupLocation]] = None, consistency: Optional[Union[int, ReadConsistencyType]] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, timeout: Optional[int] = None, **kwargs: Any) → QueryResponse[source]
Universal endpoint to run any available operation, such as search, recommendation, discovery, context search.

Parameters:
collection_name – Collection to search in

query – Query for the chosen search type operation. - If str - use string as UUID of the existing point as a search query. - If int - use integer as ID of the existing point as a search query. - If list[float] - use as a dense vector for nearest search. - If list[list[float]] - use as a multi-vector for nearest search. - If SparseVector - use as a sparse vector for nearest search. - If Query - use as a query for specific search type. - If NumpyArray - use as a dense vector for nearest search. - If Document - infer vector from the document text and use it for nearest search (requires fastembed package installed). - If None - return first limit points from the collection.

prefetch – prefetch queries to make a selection of the data to be used with the main query

query_filter –

Exclude vectors which doesn’t fit given conditions.

If None - search among all vectors

search_params – Additional search params

limit – How many results return

offset – Offset of the first result to return. May be used to paginate results. Note: large offset values may cause performance issues.

with_payload –

Specify which stored payload should be attached to the result.

If True - attach all payload

If False - do not attach any payload

If List of string - include only specified fields

If PayloadSelector - use explicit rules

with_vectors –

If True - Attach stored vector to the search result.

If False - Do not attach vector.

If List of string - include only specified fields

Default: False

score_threshold – Define a minimal score threshold for the result. If defined, less similar results will not be returned. Score of the returned result might be higher or smaller than the threshold depending on the Distance function used. E.g. for cosine similarity only higher scores will be returned.

using – Name of the vectors to use for query. If None - use default vectors or provided in named vector structures.

lookup_from –

Defines a location (collection and vector field name), used to lookup vectors for recommendations,
discovery and context queries.

If None - current collection will be used.

consistency –

Read consistency of the search. Defines how many replicas should be queried before returning the result. Values:

int - number of replicas to query, values should present in all queried replicas

’majority’ - query all replicas, but return values present in the majority of replicas

’quorum’ - query the majority of replicas, return values present in all of them

’all’ - query all replicas, and return values present in all replicas

shard_key_selector – This parameter allows to specify which shards should be queried. If None - query all shards. Only works for collections with custom sharding method.

timeout – Overrides global timeout for this search. Unit is seconds.

Examples:

Search for closest points with a filter:

qdrant.query(
    collection_name="test_collection",
    query=[1.0, 0.1, 0.2, 0.7],
    query_filter=Filter(
        must=[
            FieldCondition(
                key='color',
                range=Match(
                    value="red"
                )
            )
        ]
    )
)
Returns:
QueryResponse structure containing list of found close points with similarity scores.

query_points_groups(collection_name: str, group_by: str, query: Optional[Union[int, str, UUID, PointId, list[float], list[list[float]], SparseVector, NearestQuery, RecommendQuery, DiscoverQuery, ContextQuery, OrderByQuery, FusionQuery, RrfQuery, FormulaQuery, SampleQuery, ndarray[tuple[int, ...], dtype[Union[bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64, float16, float32, float64, longdouble]]], Document, Image, InferenceObject]] = None, using: Optional[str] = None, prefetch: Optional[Union[Prefetch, list[Prefetch]]] = None, query_filter: Optional[Union[Filter, Filter]] = None, search_params: Optional[Union[SearchParams, SearchParams]] = None, limit: int = 10, group_size: int = 3, with_payload: Union[bool, Sequence[str], PayloadSelectorInclude, PayloadSelectorExclude, WithPayloadSelector] = True, with_vectors: Union[bool, Sequence[str]] = False, score_threshold: Optional[float] = None, with_lookup: Optional[Union[str, WithLookup]] = None, lookup_from: Optional[Union[LookupLocation, LookupLocation]] = None, consistency: Optional[Union[int, ReadConsistencyType]] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, timeout: Optional[int] = None, **kwargs: Any) → GroupsResult[source]
Universal endpoint to group on any available operation, such as search, recommendation, discovery, context search.

Parameters:
collection_name – Collection to search in

query – Query for the chosen search type operation. - If str - use string as UUID of the existing point as a search query. - If int - use integer as ID of the existing point as a search query. - If list[float] - use as a dense vector for nearest search. - If list[list[float]] - use as a multi-vector for nearest search. - If SparseVector - use as a sparse vector for nearest search. - If Query - use as a query for specific search type. - If NumpyArray - use as a dense vector for nearest search. - If Document - infer vector from the document text and use it for nearest search (requires fastembed package installed). - If None - return first limit points from the collection.

prefetch – prefetch queries to make a selection of the data to be used with the main query

query_filter –

Exclude vectors which doesn’t fit given conditions.

If None - search among all vectors

search_params – Additional search params

limit – How many results return

group_size – How many results return for each group

group_by – Name of the payload field to group by. Field must be of type “keyword” or “integer”. Nested fields are specified using dot notation, e.g. “nested_field.subfield”.

with_payload –

Specify which stored payload should be attached to the result.

If True - attach all payload

If False - do not attach any payload

If List of string - include only specified fields

If PayloadSelector - use explicit rules

with_vectors –

If True - Attach stored vector to the search result.

If False - Do not attach vector.

If List of string - include only specified fields

Default: False

score_threshold – Define a minimal score threshold for the result. If defined, less similar results will not be returned. Score of the returned result might be higher or smaller than the threshold depending on the Distance function used. E.g. for cosine similarity only higher scores will be returned.

using – Name of the vectors to use for query. If None - use default vectors or provided in named vector structures.

with_lookup – Look for points in another collection using the group ids. If specified, each group will contain a record from the specified collection with the same id as the group id. In addition, the parameter allows to specify which parts of the record should be returned, like in with_payload and with_vectors parameters.

lookup_from – Defines a location (collection and vector field name), used to lookup vectors being referenced in the query as IDs. If None - current collection will be used.

consistency –

Read consistency of the search. Defines how many replicas should be queried before returning the result. Values:

int - number of replicas to query, values should present in all queried replicas

’majority’ - query all replicas, but return values present in the majority of replicas

’quorum’ - query the majority of replicas, return values present in all of them

’all’ - query all replicas, and return values present in all replicas

shard_key_selector – This parameter allows to specify which shards should be queried. If None - query all shards. Only works for collections with custom sharding method.

timeout – Overrides global timeout for this search. Unit is seconds.

Examples:

Search for closest points and group results:

   qdrant.query_points_groups(
       collection_name="test_collection",
       query=[1.0, 0.1, 0.2, 0.7],
       group_by="color",
       group_size=3,
   )

Returns:
   List of groups with not more than `group_size` hits in each group.
   Each group also contains an id of the group, which is the value of the payload field.
recover_shard_snapshot(collection_name: str, shard_id: int, location: str, api_key: Optional[str] = None, checksum: Optional[str] = None, priority: Optional[SnapshotPriority] = None, wait: bool = True, **kwargs: Any) → Optional[bool][source]
Recover shard from snapshot.

Parameters:
collection_name – Name of the collection

shard_id – Index of the shard

location – URL of the snapshot Example: - URL http://localhost:8080/collections/my_collection/snapshots/my_snapshot

api_key – API key to use for accessing the snapshot on another server.

checksum – Checksum of the snapshot to verify the integrity of the snapshot.

priority –

Defines source of truth for snapshot recovery

replica (default) means - prefer existing data over the snapshot

no_sync means - do not sync shard with other shards

snapshot means - prefer snapshot data over the current state

wait –

Await for the recovery to be done.

If true, result will be returned only when the recovery is done

If false, result will be returned immediately after the confirmation of receiving.

Returns:
True if snapshot was recovered

recover_snapshot(collection_name: str, location: str, api_key: Optional[str] = None, checksum: Optional[str] = None, priority: Optional[SnapshotPriority] = None, wait: bool = True, **kwargs: Any) → Optional[bool][source]
Recover collection from snapshot.

Parameters:
collection_name – Name of the collection

location – URL of the snapshot Example: - URL http://localhost:8080/collections/my_collection/snapshots/my_snapshot - Local path file:///qdrant/snapshots/test_collection/test_collection-6194298859870377-2023-11-09-15-17-51.snapshot

api_key – API key to use for accessing the snapshot on another server.

checksum – Checksum of the snapshot to verify the integrity of the snapshot.

priority –

Defines source of truth for snapshot recovery

replica (default) means - prefer existing data over the snapshot

no_sync means - do not sync shard with other shards

snapshot means - prefer snapshot data over the current state

wait –

Await for the recovery to be done.

If true, result will be returned only when the recovery is done

If false, result will be returned immediately after the confirmation of receiving.

Returns:
True if snapshot was recovered

recreate_collection(collection_name: str, vectors_config: Union[VectorParams, Mapping[str, VectorParams]], sparse_vectors_config: Optional[Mapping[str, SparseVectorParams]] = None, shard_number: Optional[int] = None, sharding_method: Optional[ShardingMethod] = None, replication_factor: Optional[int] = None, write_consistency_factor: Optional[int] = None, on_disk_payload: Optional[bool] = None, hnsw_config: Optional[Union[HnswConfigDiff, HnswConfigDiff]] = None, optimizers_config: Optional[Union[OptimizersConfigDiff, OptimizersConfigDiff]] = None, wal_config: Optional[Union[WalConfigDiff, WalConfigDiff]] = None, quantization_config: Optional[Union[ScalarQuantization, ProductQuantization, BinaryQuantization, QuantizationConfig]] = None, timeout: Optional[int] = None, strict_mode_config: Optional[StrictModeConfig] = None, metadata: Optional[Dict[str, Any]] = None, **kwargs: Any) → bool[source]
Delete and create empty collection with given parameters

Parameters:
collection_name – Name of the collection to recreate

vectors_config – Configuration of the vector storage. Vector params contains size and distance for the vector storage. If dict is passed, service will create a vector storage for each key in the dict. If single VectorParams is passed, service will create a single anonymous vector storage.

sparse_vectors_config – Configuration of the sparse vector storage. The service will create a sparse vector storage for each key in the dict.

shard_number – Number of shards in collection. Default is 1, minimum is 1.

sharding_method – Defines strategy for shard creation. Option auto (default) creates defined number of shards automatically. Data will be distributed between shards automatically. After creation, shards could be additionally replicated, but new shards could not be created. Option custom allows to create shards manually, each shard should be created with assigned unique shard_key. Data will be distributed between based on shard_key value.

replication_factor – Replication factor for collection. Default is 1, minimum is 1. Defines how many copies of each shard will be created. Have effect only in distributed mode.

write_consistency_factor – Write consistency factor for collection. Default is 1, minimum is 1. Defines how many replicas should apply the operation for us to consider it successful. Increasing this number will make the collection more resilient to inconsistencies, but will also make it fail if not enough replicas are available. Does not have any performance impact. Have effect only in distributed mode.

on_disk_payload – If true - point`s payload will not be stored in memory. It will be read from the disk every time it is requested. This setting saves RAM by (slightly) increasing the response time. Note: those payload values that are involved in filtering and are indexed - remain in RAM.

hnsw_config – Params for HNSW index

optimizers_config – Params for optimizer

wal_config – Params for Write-Ahead-Log

quantization_config – Params for quantization, if None - quantization will be disabled

timeout – Wait for operation commit timeout in seconds. If timeout is reached - request will return with service error.

strict_mode_config – Configure limitations for the collection, such as max size, rate limits, etc.

metadata – Arbitrary JSON metadata for the collection

Returns:
Operation result

retrieve(collection_name: str, ids: Sequence[Union[int, str, UUID, PointId]], with_payload: Union[bool, Sequence[str], PayloadSelectorInclude, PayloadSelectorExclude, WithPayloadSelector] = True, with_vectors: Union[bool, Sequence[str]] = False, consistency: Optional[Union[int, ReadConsistencyType]] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, timeout: Optional[int] = None, **kwargs: Any) → list[Record][source]
Retrieve stored points by IDs

Parameters:
collection_name – Name of the collection to lookup in

ids – list of IDs to lookup

with_payload –

Specify which stored payload should be attached to the result.

If True - attach all payload

If False - do not attach any payload

If List of string - include only specified fields

If PayloadSelector - use explicit rules

with_vectors –

If True - Attach stored vector to the search result.

If False - Do not attach vector.

If List of string - Attach only specified vectors.

Default: False

consistency –

Read consistency of the search. Defines how many replicas should be queried before returning the result. Values:

int - number of replicas to query, values should present in all queried replicas

’majority’ - query all replicas, but return values present in the majority of replicas

’quorum’ - query the majority of replicas, return values present in all of them

’all’ - query all replicas, and return values present in all replicas

shard_key_selector – This parameter allows to specify which shards should be queried. If None - query all shards. Only works for collections with custom sharding method.

timeout – Overrides global timeout for this operation. Unit is seconds.

Returns:
List of points

scroll(collection_name: str, scroll_filter: Optional[Union[Filter, Filter]] = None, limit: int = 10, order_by: Optional[Union[str, OrderBy, OrderBy]] = None, offset: Optional[Union[int, str, UUID, PointId]] = None, with_payload: Union[bool, Sequence[str], PayloadSelectorInclude, PayloadSelectorExclude, WithPayloadSelector] = True, with_vectors: Union[bool, Sequence[str]] = False, consistency: Optional[Union[int, ReadConsistencyType]] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, timeout: Optional[int] = None, **kwargs: Any) → tuple[list[Record], Union[int, str, uuid.UUID, common_pb2.PointId, NoneType]][source]
Scroll over all (matching) points in the collection.

This method provides a way to iterate over all stored points with some optional filtering condition. Scroll does not apply any similarity estimations, it will return points sorted by id in ascending order.

Parameters:
collection_name – Name of the collection

scroll_filter – If provided - only returns points matching filtering conditions

limit – How many points to return

order_by – Order the records by a payload key. If None - order by id

offset – If provided - skip points with ids less than given offset

with_payload –

Specify which stored payload should be attached to the result.

If True - attach all payload

If False - do not attach any payload

If List of string - include only specified fields

If PayloadSelector - use explicit rules

with_vectors –

If True - Attach stored vector to the search result.

If False (default) - Do not attach vector.

If List of string - include only specified fields

consistency –

Read consistency of the search. Defines how many replicas should be queried before returning the result. Values:

int - number of replicas to query, values should present in all queried replicas

’majority’ - query all replicas, but return values present in the majority of replicas

’quorum’ - query the majority of replicas, return values present in all of them

’all’ - query all replicas, and return values present in all replicas

shard_key_selector – This parameter allows to specify which shards should be queried. If None - query all shards. Only works for collections with custom sharding method.

timeout – Overrides global timeout for this operation. Unit is seconds.

Returns:
A pair of (List of points) and (optional offset for the next scroll request). If next page offset is None - there is no more points in the collection to scroll.

search_matrix_offsets(collection_name: str, query_filter: Optional[Union[Filter, Filter]] = None, limit: int = 3, sample: int = 10, using: Optional[str] = None, consistency: Optional[Union[int, ReadConsistencyType]] = None, timeout: Optional[int] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → SearchMatrixOffsetsResponse[source]
Compute distance matrix for sampled points with an offset-based output format.

Parameters:
collection_name – Name of the collection.

query_filter – Filter to apply.

limit – How many neighbors per sample to find.

sample – How many points to select and search within.

using – Name of the vectors to use for search. If None, use default vectors.

consistency – Read consistency of the search. Defines how many replicas should be queried before returning the result. Values: - int: Number of replicas to query, values should present in all queried replicas. - ‘majority’: Query all replicas, but return values present in the majority of replicas. - ‘quorum’: Query the majority of replicas, return values present in all of them. - ‘all’: Query all replicas and return values present in all replicas.

timeout – Overrides global timeout for this search. Unit is seconds.

shard_key_selector – This parameter allows specifying which shards should be queried. If None, query all shards. Only works for collections with the custom sharding method.

Returns:
Distance matrix using an offset-based encoding.

search_matrix_pairs(collection_name: str, query_filter: Optional[Union[Filter, Filter]] = None, limit: int = 3, sample: int = 10, using: Optional[str] = None, consistency: Optional[Union[int, ReadConsistencyType]] = None, timeout: Optional[int] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → SearchMatrixPairsResponse[source]
Compute distance matrix for sampled points with a pair-based output format.

Parameters:
collection_name – Name of the collection.

query_filter – Filter to apply.

limit – How many neighbors per sample to find.

sample – How many points to select and search within.

using – Name of the vectors to use for search. If None, use default vectors.

consistency – Read consistency of the search. Defines how many replicas should be queried before returning the result. Values: - int: Number of replicas to query, values should be present in all queried replicas. - ‘majority’: Query all replicas, but return values present in the majority of replicas. - ‘quorum’: Query the majority of replicas, return values present in all of them. - ‘all’: Query all replicas, and return values present in all replicas.

timeout – Overrides global timeout for this search. Unit is seconds.

shard_key_selector – This parameter allows specifying which shards should be queried. If None, query all shards. Only works for collections with the custom sharding method.

Returns:
Distance matrix using a pair-based encoding.

set_payload(collection_name: str, payload: Dict[str, Any], points: Union[list[Union[int, str, uuid.UUID, common_pb2.PointId]], Filter, Filter, PointIdsList, FilterSelector, PointsSelector], key: Optional[str] = None, wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, **kwargs: Any) → UpdateResult[source]
Modifies payload of the specified points.

Examples

Set payload:

# Assign payload value with key `"key"` to points 1, 2, 3.
# If payload value with specified key already exists - it will be overwritten
qdrant_client.set_payload(
    collection_name="test_collection",
    wait=True,
    payload={
        "key": "value"
    },
    points=[1, 2, 3]
)
Parameters:
collection_name – Name of the collection.

wait – Await for the results to be processed. - If true, the result will be returned only when all changes are applied. - If false, the result will be returned immediately after confirmation of receipt.

payload – Key-value pairs of payload to assign.

points –

List of affected points, filter, or points selector. .. rubric:: Example

points=[1, 2, 3, “cd3b53f0-11a7-449f-bc50-d06310e7ed90”]

points=Filter(must=[FieldCondition(key=’rand_number’, range=Range(gte=0.7))])

ordering (Optional[WriteOrdering]) – Define strategy for ordering of the points. Possible values: - weak (default): Write operations may be reordered, works faster. - medium: Write operations go through a dynamically selected leader, may be inconsistent for a short period of time in case of leader change. - strong: Write operations go through the permanent leader, consistent, but may be unavailable if the leader is down.

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard keys are provided, the update will be written to each of them. Only works for collections with the custom sharding method.

key –

Path to the nested field in the payload to modify. If not specified, modifies the root of the payload. E.g.:

PointStruct(
    id=42,
    vector=[...],
    payload={
        "recipe": {
            "fruits": {"apple": "100g"}
        }
    }
)

qdrant_client.set_payload(
    ...,
    payload={"cinnamon": "2g"},
    key="recipe.fruits",
    points=[42]
)

PointStruct(
    id=42,
    vector=[...],
    payload={
        "recipe": {
            "fruits": {
                "apple": "100g",
                "cinnamon": "2g"
            }
        }
    }
)
Returns:
Operation result.

update_collection(collection_name: str, optimizers_config: Optional[Union[OptimizersConfigDiff, OptimizersConfigDiff]] = None, collection_params: Optional[Union[CollectionParamsDiff, CollectionParamsDiff]] = None, vectors_config: Optional[Union[Dict[str, VectorParamsDiff], VectorsConfigDiff]] = None, hnsw_config: Optional[Union[HnswConfigDiff, HnswConfigDiff]] = None, quantization_config: Optional[Union[ScalarQuantization, ProductQuantization, BinaryQuantization, Disabled, QuantizationConfigDiff]] = None, timeout: Optional[int] = None, sparse_vectors_config: Optional[Mapping[str, SparseVectorParams]] = None, strict_mode_config: Optional[StrictModeConfig] = None, metadata: Optional[Dict[str, Any]] = None, **kwargs: Any) → bool[source]
Update parameters of the collection

Parameters:
collection_name – Name of the collection

optimizers_config – Override for optimizer configuration

collection_params – Override for collection parameters

vectors_config – Override for vector-specific configuration

hnsw_config – Override for HNSW index params

quantization_config – Override for quantization params

timeout – Wait for operation commit timeout in seconds. If timeout is reached - request will return with service error.

sparse_vectors_config – Override for sparse vector-specific configuration

strict_mode_config – Override for strict mode configuration

metadata – Arbitrary JSON-like metadata for the collection, will be merged with already stored metadata

Returns:
Operation result

update_collection_aliases(change_aliases_operations: Sequence[Union[CreateAliasOperation, RenameAliasOperation, DeleteAliasOperation, AliasOperations]], timeout: Optional[int] = None, **kwargs: Any) → bool[source]
Operation for performing changes of collection aliases.

Alias changes are atomic, meaning that no collection modifications can happen between alias operations.

Parameters:
change_aliases_operations – List of operations to perform

timeout – Wait for operation commit timeout in seconds. If timeout is reached - request will return with service error.

Returns:
Operation result

update_vectors(collection_name: str, points: Sequence[PointVectors], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, update_filter: Optional[Union[Filter, Filter]] = None, **kwargs: Any) → UpdateResult[source]
Update specified vectors in the collection. Keeps payload and unspecified vectors unchanged.

Parameters:
collection_name (str) – Name of the collection to update vectors in

points (Point) –

List of (id, vector) pairs to update. Vector might be a list of numbers or a dict of named vectors. Examples:

PointVectors(id=1, vector=[1, 2, 3])

PointVectors(id=2, vector={‘vector_1’: [1, 2, 3], ‘vector_2’: [4, 5, 6]})

wait (bool) –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

update_filter – If specified, only points that match this filter will be updated

Returns:
Operation Result(UpdateResult)

upload_collection(collection_name: str, vectors: Union[Iterable[Union[List[float], List[List[float]], Dict[str, Union[List[float], SparseVector, List[List[float]], Document, Image, InferenceObject]], Document, Image, InferenceObject]], dict[str, numpy.ndarray[tuple[int, ...], numpy.dtype[Union[numpy.bool, numpy.int8, numpy.int16, numpy.int32, numpy.int64, numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64, numpy.float16, numpy.float32, numpy.float64, numpy.longdouble]]]], ndarray[tuple[int, ...], dtype[Union[bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64, float16, float32, float64, longdouble]]]], payload: Optional[Iterable[dict[Any, Any]]] = None, ids: Optional[Iterable[Union[int, str, UUID, PointId]]] = None, batch_size: int = 64, parallel: int = 1, method: Optional[str] = None, max_retries: int = 3, wait: bool = False, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, update_filter: Optional[Union[Filter, Filter]] = None, **kwargs: Any) → None[source]
Upload vectors and payload to the collection. This method will perform automatic batching of the data. If you need to perform a single update, use upsert method. Note: use upload_points method if you want to upload multiple vectors with single payload.

Parameters:
collection_name – Name of the collection to upload to

vectors – np.ndarray or an iterable over vectors to upload. Might be mmaped

payload – Iterable of vectors payload, Optional, Default: None

ids – Iterable of custom vectors ids, Optional, Default: None

batch_size – How many vectors upload per-request, Default: 64

parallel – Number of parallel processes of upload

method – Start method for parallel processes, Default: forkserver

max_retries – maximum number of retries in case of a failure during the upload of a batch

wait – Await for the results to be applied on the server side. If true, each update request will explicitly wait for the confirmation of completion. Might be slower. If false, each update request will return immediately after the confirmation of receiving. Default: false

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

update_filter – If specified, only points that match this filter will be updated, others will be inserted

upload_points(collection_name: str, points: Iterable[PointStruct], batch_size: int = 64, parallel: int = 1, method: Optional[str] = None, max_retries: int = 3, wait: bool = False, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, update_filter: Optional[Union[Filter, Filter]] = None, **kwargs: Any) → None[source]
Upload points to the collection

Similar to upload_collection method, but operates with points, rather than vector and payload individually.

Parameters:
collection_name – Name of the collection to upload to

points – Iterator over points to upload

batch_size – How many vectors upload per-request, Default: 64

parallel – Number of parallel processes of upload

method – Start method for parallel processes, Default: forkserver

max_retries – maximum number of retries in case of a failure during the upload of a batch

wait – Await for the results to be applied on the server side. If true, each update request will explicitly wait for the confirmation of completion. Might be slower. If false, each update request will return immediately after the confirmation of receiving. Default: false

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method. This parameter overwrites shard keys written in the records.

update_filter – If specified, only points that match this filter will be updated, others will be inserted

upsert(collection_name: str, points: Union[Batch, Sequence[Union[PointStruct, PointStruct]]], wait: bool = True, ordering: Optional[WriteOrdering] = None, shard_key_selector: Optional[Union[int, str, List[Union[int, str]], ShardKeyWithFallback]] = None, update_filter: Optional[Union[Filter, Filter]] = None, **kwargs: Any) → UpdateResult[source]
Update or insert a new point into the collection.

If point with given ID already exists - it will be overwritten.

Parameters:
collection_name (str) – To which collection to insert

points (Point) – Batch or list of points to insert

wait (bool) –

Await for the results to be processed.

If true, result will be returned only when all changes are applied

If false, result will be returned immediately after the confirmation of receiving.

ordering (Optional[WriteOrdering]) –

Define strategy for ordering of the points. Possible values:

weak (default) - write operations may be reordered, works faster

medium - write operations go through dynamically selected leader, may be inconsistent for a short period of time in case of leader change

strong - Write operations go through the permanent leader, consistent, but may be unavailable if leader is down

shard_key_selector – Defines the shard groups that should be used to write updates into. If multiple shard_keys are provided, the update will be written to each of them. Only works for collections with custom sharding method.

update_filter – If specified, only points that match this filter will be updated, others will be inserted

Returns:
Operation Result(UpdateResult)

property grpc_collections: CollectionsStub
gRPC client for collections methods

Returns:
An instance of raw gRPC client, generated from Protobuf

property grpc_points: PointsStub
gRPC client for points methods

Returns:
An instance of raw gRPC client, generated from Protobuf

property http: SyncApis[ApiClient]
REST Client

Returns:
An instance of raw REST API client, generated from OpenAPI schema

property init_options: dict[str, Any]
__init__ Options

Returns:
A dictionary of options the client class was instantiated with

