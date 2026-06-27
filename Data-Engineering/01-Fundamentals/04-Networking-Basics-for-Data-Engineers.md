# Networking Basics for Data Engineers

**Phase:** 1 (Foundation) — **DEFER UNTIL PHASE 5**  
**Prerequisites:** `02-Linux-Bash-Essentials.md`  
**When to Skip:** Skip now. Return in Phase 5 when deploying to cloud.  
**Projects This Enables:** Cloud deployment, Kafka networking, VPC configuration

## What to Cover (When You Return in Phase 5)

### 1. Core Concepts
- IP addresses (IPv4 vs IPv6)
- DNS and domain resolution
- Ports and sockets
- TCP vs UDP (TCP for data pipelines, UDP for streaming where loss is acceptable)

### 2. Network Architecture
- OSI 7-layer model (focus on Layers 3-7)
- Subnets, CIDR notation, netmasks
- Public vs Private IP addresses
- NAT and port forwarding

### 3. Security Basics
- Firewalls (`iptables`, `ufw`, cloud security groups)
- TLS/SSL and certificates
- SSH tunneling and key-based auth
- VPNs and VPCs

### 4. Data Engineering Specifics
- How Kafka brokers communicate (port 9092)
- Database connection strings and pooling
- REST API communication (HTTP methods, status codes)
- gRPC for high-performance internal services

## Why Defer This?

You don't need networking to write a Python script that reads a CSV. You need networking when:
- Your Spark cluster nodes can't talk to each other
- Your Kafka consumers can't reach brokers
- Your cloud VPC is misconfigured
- Your database connection times out

These are Phase 5 problems.

## Return Here After
→ `12-Containerization-and-Infrastructure/01-Docker-Fundamentals-for-Data-Engineers.md`
