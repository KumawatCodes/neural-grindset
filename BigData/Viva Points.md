# Big Data — Complete Viva Points (Unit Wise)

---

## UNIT 1 — Introduction to Big Data & Hadoop

**What is Big Data?**

- Data too large, fast, or complex for traditional tools to handle
- Requires distributed storage and parallel processing

**Why Big Data?**

- Traditional databases can't handle petabytes of data
- Need to process massive volumes fast
- MPP (Massive Parallel Processing) — divide data, process in parallel across many nodes simultaneously

**5 V's — one line each:**

- Volume — huge amount of data (petabytes)
- Velocity — speed of data generation (real-time streams)
- Variety — different formats (text, video, JSON, logs)
- Veracity — trustworthiness/accuracy of data
- Value — useful insights extracted from data

**Velocity vs Veracity:**

- Velocity = how fast data arrives
- Veracity = how reliable/accurate the data is

---

## UNIT 2 — Components of Hadoop

**4 Core Components:**

- HDFS — distributed file storage
- MapReduce — parallel data processing framework
- YARN — resource manager (CPU + RAM allocation)
- Common — shared libraries used by all components

**Other Hadoop Ecosystem Tools:**

- Hive — SQL-like queries on HDFS data
- HBase — NoSQL real-time database on HDFS
- ZooKeeper — distributed coordination service
- Pig — scripting language for data transformation
- Flume — collects and ingests log/streaming data into HDFS
- Sqoop — transfers data between RDBMS and HDFS

---

## UNIT 2 — HDFS Architecture (Most Asked)

**HDFS Components:**

- NameNode (Master) — stores metadata only, no actual data
- DataNode (Slave) — stores actual data blocks
- Secondary NameNode — checkpointing only, NOT a backup

**What is NameNode?**

- Master daemon of HDFS
- Stores: file names, block IDs, DataNode locations, permissions
- Keeps metadata in RAM — fast access
- Uses FSImage (snapshot) + EditLog (change log) on disk
- Single point of failure in Hadoop v1

**Why NameNode is Highly Available (Hadoop v2):**

- Hadoop v1: one NameNode = single point of failure
- Hadoop v2: Active NameNode + Standby NameNode
- ZooKeeper monitors both — if Active dies, Standby takes over automatically
- Shared EditLog stored in JournalNodes (quorum)
- Clients always connect to Active NameNode

**What is DataNode?**

- Slave node — stores actual data blocks (128MB default)
- Sends heartbeat to NameNode every 3 seconds (I am alive)
- Sends block report every 6 hours (list of all blocks it holds)
- Serves read/write requests directly from clients

**What is Secondary NameNode?**

- NOT a backup — common misconception
- Merges FSImage + EditLog periodically → creates new FSImage
- Called checkpointing — reduces NameNode restart time
- Runs every 1 hour or when EditLog hits 64MB

**What is Replication?**

- Each block stored on 3 DataNodes by default (replication factor = 3)
- Rack-aware: 1st copy local node, 2nd different rack, 3rd same rack as 2nd
- If DataNode dies → NameNode detects → triggers re-replication automatically

**Pipeline (Write Path):**

- Client → DataNode 1 → DataNode 2 → DataNode 3 (pipeline replication)
- Acknowledgment flows back: DN3 → DN2 → DN1 → Client
- This chain is called the replication pipeline

**Master Node vs Slave Node:**

- Master: NameNode — manages metadata, coordinates everything
- Slave: DataNode — does the actual storage work
- Master tells slaves what to do, slaves report back

**Metadata:**

- Information ABOUT the data — not the data itself
- In HDFS: file names, block locations, permissions, timestamps, replication count
- Stored in NameNode RAM + FSImage on disk

**Daemon Processes (jps command shows these):**

- NameNode — HDFS master
- DataNode — HDFS worker
- SecondaryNameNode — checkpointing
- ResourceManager — YARN master
- NodeManager — YARN worker
- JobHistoryServer — stores completed job info

**What is ZooKeeper?**

- Distributed coordination service
- In HDFS HA: monitors NameNodes, triggers failover if Active dies
- In HBase: stores metadata location, detects RegionServer failures
- Provides: distributed locking, leader election, cluster state storage
- Runs as ensemble of 3 or 5 nodes (odd number for quorum)

**What is Zonal Node / JournalNode?**

- JournalNodes store shared EditLog in HA setup
- Active NameNode writes every change to JournalNodes
- Standby NameNode reads from JournalNodes to stay in sync
- Quorum: minimum 3 JournalNodes — majority must agree (2 out of 3)

---

## UNIT 3 — MapReduce & YARN

**What is MapReduce?**

- Programming model for parallel data processing across a cluster
- Splits data → Map phase (transform) → Shuffle/Sort → Reduce phase (aggregate)
- Fault tolerant — failed tasks auto re-executed
- Write-once, read-many — not good for real-time/streaming

**What is Mapper?**

- Processes one input split independently
- User writes map() — transforms input into intermediate key-value pairs
- Output stored on local disk temporarily
- Example: (line) → (word, 1) for each word

**What is Reducer?**

- Receives all values grouped by same key after shuffle
- User writes reduce() — aggregates values
- Output written to HDFS
- Example: (word, [1,1,1]) → (word, 3)

**What is Driver?**

- Configures and submits the MapReduce job
- Sets: mapper class, reducer class, output types, input/output paths
- Calls job.waitForCompletion() to run the job

**Shuffle and Sort:**

- Framework automatically moves mapper output to correct reducer (shuffle)
- Sorts all key-value pairs by key before reduce runs (sort)
- Most network-intensive phase
- Developer writes zero code for this

**Combiner:**

- Optional local reducer runs on mapper output before shuffle
- Reduces network data transfer
- Only valid for commutative + associative operations (sum, count — yes; average — no)

**Why MapReduce is Replaced by Spark:**

- MapReduce writes intermediate data to disk after every step — slow
- Spark keeps data in memory (RAM) — 100x faster
- MapReduce poor for streaming/live data — batch only
- Spark supports: batch, streaming, ML, graph — all in one engine
- MapReduce has high latency — each job takes seconds to minutes to start

**JobTracker (Hadoop v1):**

- Master for MapReduce — accepted jobs, assigned tasks, monitored progress
- Did too many things — resource management + job scheduling together
- Single point of failure
- Scaled poorly beyond 4000 nodes
- Replaced by YARN in Hadoop v2

**TaskTracker (Hadoop v1):**

- Slave — ran Map and Reduce tasks assigned by JobTracker
- Fixed Map slots + Fixed Reduce slots — poor resource utilization
- Replaced by NodeManager + Containers in YARN

**YARN Components (Hadoop v2):**

- ResourceManager (Master): Scheduler + ApplicationsManager — manages all cluster resources
- NodeManager (each worker): manages local resources, launches Containers
- ApplicationMaster (per job): negotiates resources, coordinates tasks for one job
- Container: unit of CPU + RAM — where actual tasks run — dynamic, not fixed slots

**JobTracker vs ResourceManager:**

|Point|JobTracker (v1)|ResourceManager (v2)|
|---|---|---|
|Role|Resource + Job management|Resource management only|
|Per job management|Itself|ApplicationMaster|
|Scalability|~4000 nodes|Tens of thousands|
|SPOF|Yes|Handled via ZooKeeper HA|

**TaskTracker vs NodeManager:**

|Point|TaskTracker (v1)|NodeManager (v2)|
|---|---|---|
|Resources|Fixed Map/Reduce slots|Dynamic Containers|
|Utilization|Poor (slots idle)|Better (any task in any container)|
|Non-MR workloads|No|Yes (Spark, Tez, Flink)|

---

## UNIT 4 — Hive Architecture

**What is Hive?**

- Data warehouse on top of Hadoop
- HiveQL (SQL-like) → translated to MapReduce/Tez/Spark jobs
- Schema on read — schema applied at query time not write time
- Not for real-time — batch processing only

**Components of Hive Architecture:**

- Driver — receives query, manages lifecycle
- Compiler — parses HiveQL → logical plan → physical plan
- Optimizer — optimizes the plan
- Executor — submits to MapReduce/Tez/Spark
- Metastore — metadata DB (MySQL/Derby) — table names, columns, HDFS locations
- HDFS — stores actual data

**What is Metastore?**

- Stores metadata: table names, column types, partition info, HDFS path
- Backed by relational DB — MySQL (production), Derby (testing)
- NOT in HDFS — in a relational database

**Where is metadata stored in Hive?**

- Metadata → relational database (MySQL/Derby) backing Metastore
- Actual data → HDFS

**Hive vs RDBMS:**

|Point|Hive|RDBMS|
|---|---|---|
|Storage|HDFS|Local disk|
|Schema|On read|On write|
|Processing|MapReduce/Tez batch|In-process real-time|
|Latency|High (seconds-minutes)|Low (milliseconds)|
|Updates|Very limited|Full support|

**Why Hive is Slower:**

- Every query launches MapReduce/Tez job — high startup overhead
- No indexes by default — full table scan
- Data on HDFS — network overhead

**Partitioning:**

- Divides data into subdirectories by column value
- Query reads only relevant partition — skips rest
- HDFS path: /warehouse/table/year=2023/

**Bucketing:**

- Divides data into fixed number of files using hash(column) % num_buckets
- Buckets created as files inside table/partition directory on HDFS
- Enables efficient map-side joins and sampling

**Static vs Dynamic Partitioning:**

- Static: user specifies partition value manually at load time
- Dynamic: Hive reads value from data, assigns partition automatically

---

## UNIT 5 — HBase Architecture

**What is HBase?**

- NoSQL column-family database on HDFS
- Provides random real-time read/write on large datasets
- Modeled after Google Bigtable
- Companies using it: Facebook, Twitter, Adobe

**HBase Architecture Components:**

- HMaster — assigns regions, handles schema changes, load balancing
- RegionServer — serves actual read/write requests
- ZooKeeper — coordination, stores hbase:meta location, detects failures
- Region — contiguous sorted range of rows, unit of distribution
- MemStore — in-memory write buffer per column family
- WAL — Write Ahead Log — crash recovery
- HFile — immutable on-disk file on HDFS
- BlockCache — read cache per RegionServer

**HMaster vs NameNode:**

- Both are masters but different systems
- HMaster: not in read/write path — clients go directly to RegionServer
- NameNode: clients must contact it first to find block locations

**WAL purpose:**

- Logs every write before MemStore
- If RegionServer crashes → WAL replayed → no data loss

**MemStore:**

- In-memory write buffer, sorted by row key
- Flushes to HFile when full (128MB default)
- Converts random writes to sequential HDFS writes

**Write Path:** Client → ZooKeeper → RegionServer → WAL → MemStore → (flush) → HFile

**Read Path:** Client → ZooKeeper → RegionServer → BlockCache → MemStore → HFile

**Compaction:**

- Minor: merges few small HFiles — frequent, lightweight
- Major: merges ALL HFiles — removes tombstones, expensive

---

## UNIT 6 — Cassandra Architecture

**What is Cassandra?**

- NoSQL distributed database, peer-to-peer architecture
- No master, no slave — every node equal
- Optimized for write-heavy, high availability workloads
- CAP: AP — Available + Partition Tolerant

**Peer-to-Peer Architecture:**

- All nodes in a ring — each owns a token range
- Any node can serve any request — no single point of failure
- Contrast with Hadoop: has NameNode master (SPOF)

**Gossip Protocol:**

- Each node gossips with 1-3 neighbors every second
- Shares: node status, load, token ranges
- Entire cluster knows state of all nodes within few rounds
- No central monitor needed

**Murmur Hash:**

- Default partitioner in Cassandra
- Hashes partition key → 64-bit token → determines which node owns the row
- Ensures uniform data distribution across ring

**Partition Key:**

- Determines which node stores the row (via Murmur3 hash)
- All rows with same partition key on same node
- Bad design → hot spots

**Clustering Column:**

- Determines sort order of rows within a partition
- Default order: ASC
- Enables range queries within a partition

**Primary Key — 3 purposes:**

- Uniqueness
- Data distribution (partition key part)
- Data ordering (clustering column part)

**Wide Rows:**

- One partition key + many clustering column values
- All stored together on same node, sorted
- Problem: if too large → one node overloaded (hot spot)
- Keep partition under 100MB

**Consistency Levels:**

- ONE — fastest, least consistent
- QUORUM — majority must respond — balanced
- ALL — all replicas must respond — strongest, highest latency

**Write Path:** Client → Coordinator → Replica nodes → CommitLog → MemTable → (flush) → SSTable

**Read Path:** Client → Coordinator → Replica → MemTable → Bloom Filter → SSTable → return latest

**ALLOW FILTERING:**

- Queries non-primary-key columns
- Requires full cluster scan — very slow
- Cassandra rejects by default — must add ALLOW FILTERING explicitly

**Index:**

- Secondary index on non-key column
- Better than ALLOW FILTERING for repeated queries
- Stored locally per node

---

## CROSS UNIT COMPARISON (Most Asked Viva)

**Master nodes across systems:**

|System|Master|Worker|
|---|---|---|
|HDFS|NameNode|DataNode|
|MapReduce v1|JobTracker|TaskTracker|
|YARN|ResourceManager|NodeManager|
|HBase|HMaster|RegionServer|
|Cassandra|None (peer-to-peer)|All nodes equal|

**Write logs across systems:**

|System|Log Name|Purpose|
|---|---|---|
|HDFS|EditLog|Records metadata changes|
|HBase|WAL|Crash recovery for MemStore|
|Cassandra|CommitLog|Crash recovery for MemTable|

**In-memory stores:**

|System|Name|Flushes To|
|---|---|---|
|HBase|MemStore|HFile on HDFS|
|Cassandra|MemTable|SSTable on disk|

**Coordination:**

|System|Coordinator|Role|
|---|---|---|
|HDFS HA|ZooKeeper|NameNode failover|
|HBase|ZooKeeper|RegionServer monitoring, meta location|
|Cassandra|Gossip Protocol|Cluster state sharing, no central coordinator|