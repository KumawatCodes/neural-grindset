# Big Data Architecture — Viva Notes

---

## SECTION 1: HADOOP & HDFS ARCHITECTURE

### What is Hadoop?

- Open-source framework for storing and processing large datasets across clusters
- Based on two Google papers: GFS (Google File System) → HDFS, MapReduce paper → Hadoop MapReduce
- Written in Java
- Designed on commodity hardware (cheap, normal machines — not expensive servers)
- Core idea: move computation to data, not data to computation

---

### HDFS (Hadoop Distributed File System)

**What it is:**

- Distributed file system that stores data across multiple machines
- Designed for write-once, read-many workloads
- Optimized for large files (GBs to TBs), not millions of small files
- Default block size: 128MB (older versions: 64MB)

**Why block size is large:**

- Reduces number of metadata entries in NameNode
- Reduces seek time overhead
- Better throughput for sequential reads

**Replication:**

- Default replication factor = 3
- Rack-aware placement: 1st replica on local node, 2nd on different rack, 3rd on same rack as 2nd
- Purpose: fault tolerance + network bandwidth optimization during reads

---

### NameNode

**What it is:**

- Master node of HDFS
- Stores and manages filesystem metadata only — NOT actual data
- Runs on a single dedicated machine

**What metadata it stores:**

- File names, directory structure
- Block IDs for each file
- Which DataNodes hold which blocks
- Permissions, timestamps, replication factor

**How it stores metadata:**

- FSImage: snapshot of entire filesystem namespace (on disk)
- EditLog: log of every change made since last FSImage snapshot (on disk)
- On startup: loads FSImage + replays EditLog → builds in-memory namespace

**Problem it solves:**

- Centralized metadata management so clients know where to find any block without scanning all DataNodes

**Use case / interview angle:**

- NameNode is the single point of failure in Hadoop v1 — if NameNode dies, entire cluster is unavailable
- Solution in Hadoop v2: High Availability NameNode (Active + Standby NameNode via ZooKeeper)

**What NameNode does NOT do:**

- Does not store actual file data
- Does not participate in data transfer between client and DataNode
- Does not run on every node

**Heartbeat & Block Report:**

- DataNodes send heartbeat to NameNode every 3 seconds (I am alive signal)
- DataNodes send block report every 6 hours (list of all blocks it holds)
- If NameNode does not receive heartbeat for 10 minutes → marks DataNode as dead → triggers re-replication

---

### Secondary NameNode

**What it is NOT:**

- It is NOT a backup or standby NameNode — most common misconception in viva

**What it actually does:**

- Periodically merges FSImage + EditLog → creates new FSImage → sends back to NameNode
- This process is called checkpointing
- Reduces NameNode startup time (smaller EditLog to replay)
- Runs on a separate machine

**Why EditLog grows:**

- Every write operation appends to EditLog
- Without checkpointing, EditLog becomes huge → slow NameNode startup

**Runs by default every:**

- 1 hour or when EditLog reaches 64MB (whichever comes first)

---

### DataNode

**What it is:**

- Slave/worker node in HDFS
- Stores actual data blocks on local disk
- Multiple DataNodes in a cluster (can be hundreds to thousands)

**What it does:**

- Serves read and write requests from clients
- Performs block replication as instructed by NameNode
- Sends heartbeat + block report to NameNode
- Performs block integrity check using checksums

**Block storage:**

- Each block stored as a plain file on DataNode's local filesystem
- Checksum file stored alongside each block for corruption detection

---

### HDFS Read Path

1. Client calls open() on DistributedFileSystem
2. DistributedFileSystem contacts NameNode → gets list of DataNodes for each block
3. Client opens FSDataInputStream → reads block from nearest DataNode
4. If DataNode fails during read → client automatically tries next DataNode
5. Client calls close()

---

### HDFS Write Path

1. Client calls create() on DistributedFileSystem
2. DistributedFileSystem contacts NameNode → NameNode creates metadata entry
3. NameNode picks 3 DataNodes (rack-aware)
4. Client writes to first DataNode → first DataNode replicates to second → second to third (pipeline)
5. Acknowledgment flows back: third → second → first → client
6. After all blocks written → client calls close() → NameNode notified

---

## SECTION 2: MapReduce ARCHITECTURE

### What is MapReduce?

- Programming model for processing large datasets in parallel across a cluster
- Two main phases: Map and Reduce
- Fault tolerant: if a task fails → re-executed automatically
- Inspired by functional programming concepts (map and reduce functions)

---

### JobTracker (Hadoop v1)

**What it is:**

- Master process for MapReduce job management
- Runs on the same machine as NameNode (typically)

**What it does:**

- Accepts job submissions from clients
- Splits job into Map tasks and Reduce tasks
- Assigns tasks to TaskTrackers based on data locality
- Monitors task progress
- Handles task failures by re-assigning tasks

**Problem it had:**

- Single point of failure in Hadoop v1
- Did both resource management AND job scheduling — too much responsibility
- Scaled poorly beyond 4000 nodes
- Solution: replaced by YARN in Hadoop v2

---

### TaskTracker (Hadoop v1)

**What it is:**

- Slave process on each worker node
- Receives tasks from JobTracker and executes them

**What it does:**

- Launches Map and Reduce task processes (child JVMs)
- Sends progress report and heartbeat to JobTracker
- Has fixed number of Map slots and Reduce slots

**Problem:**

- Fixed slots meant poor resource utilization — Map slots idle during Reduce phase and vice versa
- Solution: YARN Containers (dynamic resource allocation)

---

### MapReduce Data Flow

**Input Splits:**

- Input data divided into logical splits (one split per Mapper typically)
- Split size = HDFS block size by default
- RecordReader converts each split into key-value pairs for Mapper

**Map Phase:**

- Each Mapper processes one input split independently
- Outputs intermediate key-value pairs
- Mapper output stored on local disk (NOT HDFS) — temporary storage

**Combiner (optional):**

- Mini-Reducer that runs on Mapper output locally
- Reduces amount of data transferred over network
- Only applicable when Reduce operation is commutative and associative (e.g. sum, count)
- Also called local reducer

**Partitioner:**

- Decides which Reducer receives which key
- Default: hash(key) % number of Reducers
- Ensures all values for same key go to same Reducer

**Shuffle and Sort:**

- Framework transfers Mapper output to correct Reducer nodes (shuffle)
- All values for each key are grouped together and sorted by key (sort)
- Most network-intensive phase
- Happens automatically — developer does not write this code

**Reduce Phase:**

- Each Reducer receives (key, list of values) pairs
- Processes and outputs final key-value pairs
- Output written to HDFS

---

## SECTION 3: YARN ARCHITECTURE

### Why YARN? (What problem did it solve?)

- Hadoop v1 JobTracker did two things: resource management + job scheduling
- Led to scalability bottleneck and poor resource utilization
- YARN separates these two concerns
- YARN = Yet Another Resource Negotiator
- Introduced in Hadoop v2
- Allows non-MapReduce workloads to run on Hadoop (Spark, Tez, Flink)

---

### ResourceManager

**What it is:**

- Master daemon of YARN — one per cluster
- Pure resource manager (does not care about application logic)

**Two internal components:**

- Scheduler:
    
    - Allocates resources (CPU + RAM) to applications
    - Does not monitor or restart failed tasks
    - Pluggable: FIFO, Capacity Scheduler, Fair Scheduler
- ApplicationsManager:
    
    - Accepts job submissions
    - Launches ApplicationMaster for each job
    - Restarts ApplicationMaster on failure

---

### NodeManager

**What it is:**

- Slave daemon running on every worker node
- Replaces TaskTracker from Hadoop v1

**What it does:**

- Manages resources on its node (CPU, RAM, disk, network)
- Launches and monitors Containers
- Reports resource usage to ResourceManager
- Kills Containers that exceed resource limits

---

### ApplicationMaster

**What it is:**

- One ApplicationMaster per submitted application (job)
- Runs inside a Container on a worker node
- Application-framework specific (different for MapReduce, Spark, etc.)

**What it does:**

- Negotiates resources (Containers) from ResourceManager Scheduler
- Works with NodeManagers to launch and monitor tasks
- Handles task failures internally
- Reports job progress and completion to ResourceManager

**Why this design is better:**

- ResourceManager is not overloaded with per-job management
- Each ApplicationMaster manages only its own job
- Cluster can scale to tens of thousands of nodes

---

### Container

**What it is:**

- Unit of resource allocation in YARN
- A bundle of CPU cores + RAM on a specific node
- Actual Map/Reduce tasks (or Spark executors) run inside Containers

**Dynamic allocation:**

- Unlike Hadoop v1 fixed Map/Reduce slots, Containers are allocated dynamically
- Better resource utilization

---

### YARN Job Submission Flow

1. Client submits job to ResourceManager
2. ResourceManager ApplicationsManager allocates a Container for ApplicationMaster
3. NodeManager launches ApplicationMaster in that Container
4. ApplicationMaster registers with ResourceManager
5. ApplicationMaster requests Containers from Scheduler
6. Scheduler allocates Containers on NodeManagers
7. ApplicationMaster contacts NodeManagers to launch tasks in Containers
8. Tasks execute, report progress to ApplicationMaster
9. On completion, ApplicationMaster deregisters from ResourceManager
10. Containers released back to cluster

---

## SECTION 4: APACHE HIVE ARCHITECTURE

### What is Hive?

- Data warehouse system built on top of Hadoop
- Allows SQL-like queries (HiveQL) on data stored in HDFS
- Does NOT store data itself — data lives in HDFS
- Translates HiveQL → MapReduce / Tez / Spark jobs
- Designed for batch processing, not real-time queries
- Created at Facebook

**Use case:**

- Analysts who know SQL but not Java MapReduce
- Ad-hoc queries on large datasets

---

### Hive Metastore

**What it is:**

- Central repository of Hive metadata
- Stores: table names, column names, data types, partitions, bucket info, HDFS location of data
- Backed by a relational database (MySQL in production, Apache Derby for testing)

**Why it is important:**

- Without Metastore, Hive does not know where data is or what schema to apply
- Schema on read: data has no schema when stored in HDFS — schema is applied at query time using Metastore

**Three modes:**

- Embedded mode: Derby DB, single user, testing only
- Local mode: external DB (MySQL), Metastore in same JVM as Hive
- Remote mode: Metastore runs as a separate service — recommended for production

---

### Hive Driver

**What it does:**

- Receives HiveQL query
- Manages session handles and query lifecycle
- Passes query to Compiler

---

### Hive Compiler

**What it does:**

- Parses HiveQL → Abstract Syntax Tree (AST)
- Performs semantic analysis using Metastore (checks table/column existence)
- Generates logical plan → physical plan (DAG of MapReduce/Tez jobs)

---

### Hive Optimizer

- Optimizes physical plan
- Techniques: predicate pushdown, column pruning, join optimization

---

### Hive Executor

- Takes optimized plan
- Submits MapReduce/Tez/Spark jobs to YARN
- Jobs read data from HDFS, process, write results back

---

### Hive Partitioning

**What it is:**

- Divides table data into subdirectories based on column value
- Example: sales table partitioned by year and month
- HDFS path: /warehouse/sales/year=2023/month=01/

**Why it matters:**

- Avoids full table scan — query only reads relevant partition directories
- Massive performance improvement for large tables

**Two types:**

- Static partitioning: user specifies partition value during insert
- Dynamic partitioning: Hive automatically determines partition value from data

---

### Hive Bucketing

**What it is:**

- Further divides data within a partition into fixed number of files (buckets)
- Uses hash of a column value to assign rows to buckets
- Example: 8 buckets on customer_id column

**Why it matters:**

- Enables more efficient map-side joins (join without shuffle)
- Faster sampling of data
- Complements partitioning

---

## SECTION 5: APACHE HBASE ARCHITECTURE

### What is HBase?

- NoSQL, column-family distributed database built on top of HDFS
- Modeled after Google Bigtable
- Provides random read/write access to data in HDFS (HDFS alone is write-once)
- Handles billions of rows and millions of columns
- Strong consistency model
- Not suitable for complex joins or SQL — use Hive for that

**Use case:**

- Real-time read/write on large datasets
- Time-series data, messaging systems, user profile storage

---

### HMaster

**What it is:**

- Master node of HBase cluster

**What it does:**

- Assigns Regions to RegionServers on startup and rebalances load
- Handles RegionServer failures (detects via ZooKeeper)
- Manages schema changes: create table, delete table, alter table
- Does NOT handle actual data reads/writes — clients go directly to RegionServers

**Important distinction:**

- HMaster is not in the critical read/write path
- Even if HMaster is down, existing reads/writes continue on RegionServers
- HMaster down = no schema changes, no region assignments only

---

### ZooKeeper

**What it is:**

- Distributed coordination service (not part of HBase but required by it)
- Runs as an ensemble of typically 3 or 5 nodes (odd number for quorum)

**What it does in HBase:**

- Stores location of hbase:meta table (root catalog table)
- Monitors RegionServer health via ephemeral nodes (RegionServer registers → dies → ZooKeeper detects)
- Notifies HMaster of RegionServer failures
- Provides distributed locking and leader election
- Stores HBase cluster state

**Why clients talk to ZooKeeper first:**

- Client does not know which RegionServer has which Region
- Client asks ZooKeeper → gets location of hbase:meta table → queries meta table → finds correct RegionServer → reads/writes data

---

### RegionServer

**What it is:**

- Worker node in HBase
- Handles actual data reads and writes
- One RegionServer per worker node typically

**Contains:**

- Multiple Regions
- One WAL (Write Ahead Log) per RegionServer
- One BlockCache per RegionServer

---

### Region

**What it is:**

- Basic unit of scalability and load balancing in HBase
- A contiguous sorted range of rows (sorted by row key)
- Each table starts with one Region → splits as data grows
- HMaster assigns each Region to exactly one RegionServer

**Contains:**

- One or more Stores (one Store per column family)
- Each Store has: one MemStore + multiple HFiles (StoreFiles)

---

### MemStore

**What it is:**

- In-memory write buffer per Store (per column family per Region)

**What it does:**

- All writes go to MemStore first (after WAL)
- Data in MemStore is sorted by row key
- When MemStore reaches threshold (default 128MB) → flushes to disk as HFile

---

### WAL (Write Ahead Log) / HLog

**What it is:**

- Sequential log file on HDFS, one per RegionServer

**Purpose:**

- Fault tolerance: write is logged to WAL before writing to MemStore
- If RegionServer crashes before MemStore flush → WAL replayed to recover data
- Without WAL: data in MemStore (RAM) would be lost on crash

---

### HFile (StoreFile)

**What it is:**

- Immutable on-disk file on HDFS
- Sorted key-value storage format
- Created when MemStore flushes

---

### BlockCache

**What it is:**

- Read cache, one per RegionServer (held in heap memory)
- Caches frequently accessed HFile blocks
- Improves read performance significantly
- Default implementation: LRU cache

---

### HBase Write Path

1. Client contacts ZooKeeper → finds hbase:meta location
2. Client queries hbase:meta → finds RegionServer for target row
3. Client sends write to RegionServer
4. RegionServer writes to WAL first
5. RegionServer writes to MemStore
6. Acknowledgment sent to client
7. When MemStore full → flush to HFile on HDFS

---

### HBase Read Path

1. Client contacts ZooKeeper → hbase:meta location → RegionServer
2. RegionServer checks BlockCache (read cache)
3. If not in BlockCache → checks MemStore
4. If not in MemStore → reads from HFiles on HDFS
5. Merges results (same row key may exist in MemStore + multiple HFiles due to updates)
6. Returns latest version to client

---

### Compaction

**Minor Compaction:**

- Merges a few small HFiles into one larger HFile
- Does not remove deleted data (tombstones kept)
- Runs frequently, lightweight

**Major Compaction:**

- Merges ALL HFiles in a Store into one single HFile
- Removes deleted records (tombstones purged)
- Expensive — usually scheduled off-peak hours

**Why compaction is needed:**

- Each MemStore flush creates a new HFile
- Over time too many HFiles → slow reads (must check all files)
- Compaction reduces file count → faster reads

---

### Region Split

- When Region size exceeds threshold → splits into two child Regions at midpoint
- HMaster detects split → assigns child Regions (may stay on same RegionServer or move)
- Allows horizontal scaling

---

## SECTION 6: APACHE CASSANDRA ARCHITECTURE

### What is Cassandra?

- Distributed NoSQL database designed for high availability and no single point of failure
- Peer-to-peer architecture — no master, no slave, every node is equal
- Developed at Facebook, open-sourced, now Apache project
- Optimized for write-heavy workloads
- CAP theorem: AP system (Available + Partition Tolerant), tunable consistency

**Use case:**

- Time-series data, IoT sensor data, messaging, recommendation engines
- Applications needing 100% uptime across multiple datacenters

---

### Peer-to-Peer Architecture / Ring

**What it is:**

- All nodes arranged logically in a ring
- Each node owns a range of token values (consistent hashing)
- A row's partition key is hashed → determines which node owns it
- No master → no single point of failure

**Contrast with HBase/Hadoop:**

- Hadoop: NameNode is master (SPOF), DataNodes are slaves
- HBase: HMaster is master, RegionServers are slaves
- Cassandra: all nodes equal, any node can serve any request

---

### Gossip Protocol

**What it is:**

- Peer-to-peer communication protocol for sharing cluster state
- Each node gossips with 1-3 random neighbors every second
- Within a few rounds, entire cluster knows state of every node

**What information is gossiped:**

- Node status (alive/dead)
- Load information
- Token ownership
- Schema version

**HeartbeatState + ApplicationState:**

- HeartbeatState: generation number + version (increments every gossip round)
- ApplicationState: node metadata (load, status, datacenter, rack)

---

### Coordinator Node

**What it is:**

- The node a client connects to for a read or write request
- Any node can be coordinator — no special role
- Coordinator is responsible for routing request to correct replica nodes

**What it does:**

- Hashes partition key using Murmur3 partitioner
- Determines which nodes own replicas
- Forwards request to replica nodes
- Waits for responses based on consistency level
- Returns result to client

---

### Replication

**Replication Factor (RF):**

- Number of copies of each row stored across the cluster
- RF=3 means 3 nodes hold each row
- Replicas placed on next RF nodes clockwise on the ring

**SimpleStrategy:**

- Places replicas on next N nodes clockwise on ring
- Use only for single datacenter

**NetworkTopologyStrategy:**

- Places replicas considering rack and datacenter topology
- Recommended for production and multi-datacenter setups
- Ensures replicas are on different racks within each datacenter

---

### Consistency Levels

**Write consistency levels:**

- ANY: at least one node acknowledges (even if hinted handoff)
- ONE: one replica acknowledges
- QUORUM: majority of replicas (RF/2 + 1) acknowledge
- ALL: all replicas must acknowledge

**Read consistency levels:**

- ONE: return result from first responding replica
- QUORUM: read from majority of replicas, return latest version
- ALL: read from all replicas

**Tunable consistency:**

- Developer chooses consistency level per operation
- Stronger consistency = higher latency
- Rule: write consistency + read consistency > RF = strong consistency

---

### Cassandra Write Path

1. Client sends write to Coordinator
2. Coordinator determines replica nodes
3. Coordinator sends write to all replica nodes in parallel
4. Each replica node:
    - Writes to CommitLog (sequential disk write — for durability)
    - Writes to MemTable (in-memory, sorted)
5. Coordinator waits for acknowledgments based on consistency level
6. Returns success to client
7. When MemTable full → flushes to SSTable on disk

---

### Cassandra Read Path

1. Client sends read to Coordinator
2. Coordinator contacts replica nodes based on consistency level
3. On each contacted replica:
    - Check MemTable
    - Check Row Cache (if enabled)
    - Check Bloom Filter (probabilistic check: is this key in this SSTable?)
    - Check SSTable index
    - Read from SSTable
4. Coordinator compares results from replicas → returns latest version
5. If replicas disagree → Read Repair (background sync of stale replicas)

---

### SSTable (Sorted String Table)

**What it is:**

- Immutable on-disk file written when MemTable flushes
- Data sorted by partition key
- Never modified after written — updates create new SSTables
- Deletions create tombstone markers (not immediate deletes)

---

### CommitLog

**What it is:**

- Sequential append-only log on disk, one per node
- Every write appended to CommitLog before MemTable
- Purpose: crash recovery (replay CommitLog if node crashes before MemTable flush)
- Truncated after MemTable flushes to disk

---

### Compaction in Cassandra

**What it is:**

- Merges multiple SSTables into one
- Removes tombstones (deleted records)
- Keeps only latest version of each row
- Reduces read latency (fewer SSTables to check)

**Strategies:**

- SizeTieredCompactionStrategy: default, triggers when many SSTables of similar size accumulate — good for write-heavy
- LeveledCompactionStrategy: organizes SSTables in levels — good for read-heavy
- TimeWindowCompactionStrategy: groups SSTables by time window — good for time-series data

---

### Cassandra Data Model

**Hierarchy:**

- Cluster → Keyspace → Table → Row → Columns

**Keyspace:**

- Top-level container (equivalent to database in RDBMS)
- Defines replication strategy and replication factor

**Primary Key components:**

- Partition Key: determines which node stores the row (hashed)
- Clustering Columns: determines sort order of rows within a partition
- Together: Partition Key + Clustering Columns = Primary Key

**Wide Row:**

- One partition key with many clustering column values
- All rows in one partition stored together on same node, sorted by clustering columns
- Very efficient for range queries within a partition

---

## QUICK VIVA COMPARISON TABLE

|Feature|HDFS/Hadoop|HBase|Cassandra|
|---|---|---|---|
|Architecture|Master-Slave|Master-Slave|Peer-to-Peer|
|Master node|NameNode|HMaster|None|
|Slave node|DataNode|RegionServer|All nodes equal|
|Coordination|Secondary NameNode|ZooKeeper|Gossip Protocol|
|Write log|EditLog|WAL|CommitLog|
|In-memory store|—|MemStore|MemTable|
|Disk format|HDFS blocks|HFile|SSTable|
|SPOF|Yes (NameNode)|Partial (HMaster)|No|
|Consistency|Strong|Strong|Tunable|
|Query language|HiveQL (via Hive)|Java API / Scan|CQL|
|Best for|Batch processing|Random read/write|Write-heavy, multi-DC|

---

These cover everything a viva examiner typically asks at the component level. The comparison table at the end is especially useful for questions like "how is HBase different from Cassandra" or "what does ZooKeeper do that Secondary NameNode does not."