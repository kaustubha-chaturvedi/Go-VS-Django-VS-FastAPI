# Benchmarking  Server Performance Python's Django And FastApi vs. Go

This project benchmarks the performance of Python's Django and DjangoRestFramework and Go servers for GET and POST requests using the Python `requests` library and measures the response times for each iteration.

- Both servers use same production database server running Postgres.
- Each GET and POST Request queries db synchronously. 
- First Get and then Post Query request is made to test read write operations.
- Djnago and Go server are synchronous whereas fastapi is an async.
- Gunicorn was used for django and Uvicron for fastapi whereas Go server is run using go run command.

## Setup

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kaustubha-chaturvedi/Go-VS-DjangoRestFramework.git

2. Install the required Python packages:
    ```bash 
    pip install -r requirements.txt

3. Running the Benchmark

    Adjust the server URLs in the Python script to match your Python and Go server endpoints.

    Run the benchmark script:
    ```bash
    python bench.py

### Results
CSV File
The benchmark results are stored in a CSV file named `benchmark_results.csv`, containing the iteration number, times for GET and POST requests in seconds.

| Iteration | Django - GET Time (seconds) | Django - POST Time (seconds) | Go - GET Time (seconds) | Go - POST Time (seconds) | FastAPI - GET Time (seconds) | FastAPI - POST Time (seconds) |
|-----------|-----------------------------|------------------------------|-------------------------|--------------------------|------------------------------|-------------------------------|
| 1         | 5.2                         | 6.29                         | 0.06                    | 0.08                     | 0.05                         | 5.25                          |
| 2         | 5.19                        | 5.19                         | 0.04                    | 0.06                     | 0.04                         | 0.1                           |
| 3         | 5.18                        | 5.19                         | 0.04                    | 0.06                     | 0.04                         | 0.1                           |
| 4         | 5.19                        | 5.19                         | 0.04                    | 0.06                     | 0.04                         | 0.1                           |
| 5         | 5.2                         | 5.19                         | 0.04                    | 0.06                     | 0.04                         | 0.12                          |
| 6         | 5.2                         | 5.19                         | 0.04                    | 0.06                     | 0.05                         | 0.11                          |
| 7         | 5.2                         | 5.19                         | 0.05                    | 0.06                     | 0.04                         | 0.11                          |
| 8         | 5.2                         | 5.19                         | 0.04                    | 0.06                     | 0.05                         | 0.1                           |
| 9         | 5.19                        | 5.2                          | 0.05                    | 0.06                     | 0.05                         | 0.12                          |
| 10        | 5.21                        | 5.19                         | 0.05                    | 0.06                     | 0.05                         | 0.11                          |


### Graphs
Single graph `Comparision.png` is generated
![Comparision](./comparison.png)
