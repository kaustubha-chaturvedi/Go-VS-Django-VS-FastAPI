import requests
import json
import time
import csv
import matplotlib.pyplot as plt

def benchmark_get_request(url, iteration, label):
    start_time = time.time()
    response = requests.get(url)
    response.close()
    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"{iteration} | GET | {label} | {elapsed_time:.4f} | {response.status_code}")
    return elapsed_time

def benchmark_post_request(url, iteration, data, label):
    start_time = time.time()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.close()
    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"{iteration} | POST | {label} | {elapsed_time:.4f} | {response.status_code}")
    return elapsed_time

def run_benchmark(url, iterations, label):
    get_times = []
    post_times = []

    for i in range(1, iterations + 1):
        get_time = benchmark_get_request(url, i, label)
        post_time = benchmark_post_request(url, i, {"name": f"Sample Item {label} {i}"}, label)
        
        get_times.append(get_time)
        post_times.append(post_time)

    return get_times, post_times

def plot_comparison(labels, get_times_python, get_times_go, post_times_python, post_times_go):
    iterations = list(range(1, len(get_times_python) + 1))
    get_times_python_ms = [time * 1000 for time in get_times_python]  
    get_times_go_ms = [time * 1000 for time in get_times_go]  
    post_times_python_ms = [time * 1000 for time in post_times_python]  
    post_times_go_ms = [time * 1000 for time in post_times_go]  

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.plot(iterations, get_times_python_ms, marker='o', linestyle='-', color='blue', label=f'{labels[0]} - GET Request')
    plt.plot(iterations, get_times_go_ms, marker='o', linestyle='-', color='red', label=f'{labels[1]} - GET Request')
    plt.xlabel('Iteration')
    plt.ylabel('Time (milliseconds)')
    plt.title('GET Request Comparison: Python vs Go')
    plt.legend()
    plt.grid(True)

    for i, (x, y) in enumerate(zip(iterations, get_times_python_ms)):
        plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', color='blue')
    for i, (x, y) in enumerate(zip(iterations, get_times_go_ms)):
        plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', color='red')

    plt.subplot(1, 2, 2)
    plt.plot(iterations, post_times_python_ms, marker='o', linestyle='-', color='blue', label=f'{labels[0]} - POST Request')
    plt.plot(iterations, post_times_go_ms, marker='o', linestyle='-', color='red', label=f'{labels[1]} - POST Request')
    plt.xlabel('Iteration')
    plt.ylabel('Time (milliseconds)')
    plt.title('POST Request Comparison: Python vs Go')
    plt.legend()
    plt.grid(True)

    for i, (x, y) in enumerate(zip(iterations, post_times_python_ms)):
        plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', color='blue')
    for i, (x, y) in enumerate(zip(iterations, post_times_go_ms)):
        plt.text(x, y, f'{y:.2f}', ha='right', va='bottom', color='red')

    plt.tight_layout()
    plt.savefig('comparison.png')


def save_to_csv(filename, labels, get_times_python, get_times_go, post_times_python, post_times_go):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Iteration', f'{labels[0]} - GET Time (seconds)', f'{labels[1]} - GET Time (seconds)',
                         f'{labels[0]} - POST Time (seconds)', f'{labels[1]} - POST Time (seconds)'])

        for i, (get_py, get_go, post_py, post_go) in enumerate(zip(get_times_python, get_times_go, post_times_python, post_times_go), start=1):
            writer.writerow([i, get_py, get_go, post_py, post_go])
if __name__ == "__main__":
    iterations = int(input("Enter number of iterations: "))
    url_py = "http://localhost:8000/items/"
    url_go = "http://localhost:8080/items"
    labels = ["Python", "Go"]

    get_times_python, post_times_python = run_benchmark(url_py, iterations, "Python")
    get_times_go, post_times_go = run_benchmark(url_go, iterations, "Go")

    plot_comparison(labels, get_times_python,get_times_go,post_times_python,post_times_go)
    save_to_csv('benchmark_results.csv', labels, get_times_python, get_times_go, post_times_python, post_times_go)