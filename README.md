# FinGuard 🛡️ - Enterprise Anti-Fraud AI Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Ollama-1C3C3C.svg)](https://www.langchain.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2.0-red.svg)](https://docs.pydantic.dev/)

**FinGuard** is an enterprise-grade autonomous fraud detection microservice built using Python, LangChain, local Ollama models (`qwen2.5:1.5b`), and FastAPI. It processes high-risk financial transactions in real-time, executing schema validations, LLM-based risk assessments, and compliance decision enforcement.

---

## 🏛️ System Architecture

```text
               +----------------------------------+
               |  Inbound HTTP POST /api/v1/analyze|
               +-----------------+----------------+
                                 |
                                 v
               +----------------------------------+
               |     FastAPI / Pydantic V2        |
               |   (Schema & Type Validation)     |
               +-----------------+----------------+
                                 |
                                 v
               +----------------------------------+
               |  Risk Analyst Agent (LangChain)  |
               |  (Local LLM: qwen2.5:1.5b)       |
               +-----------------+----------------+
                                 |
                                 v
               +----------------------------------+
               |      Decision Maker Agent        |
               |  (APPROVED / FLAGGED_FOR_REVIEW) |
               +-----------------+----------------+
                                 |
                                 v
               +----------------------------------+
               | JSON Response + Loguru Audit Trail|
               +----------------------------------+

               Key Features & Design Decisions
Modular Clean Architecture: Strict separation of concerns across agents (/app/agents), payload schemas (/app/schemas), and core configurations (/app/core).

Guaranteed Structured Outputs: Leverages ChatOllama.with_structured_output() bound to strict Pydantic models. Eliminates brittle string parsing and regular expressions.

Structured Audit Logging: Integrated loguru for colorized console output and continuous background file rotation (logs/finguard.log) for compliance auditing.

Asynchronous REST API: Built on FastAPI to deliver production-ready throughput, health check endpoints (/health), and OpenAPI/Swagger documentation (/docs).

Installation & Setup
Prerequisites
Python 3.10+

Local Ollama instance running with the model pulled:

Bash
ollama pull qwen2.5:1.5b