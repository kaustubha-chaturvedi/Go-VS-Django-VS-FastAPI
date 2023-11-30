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
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.close()
    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"{iteration} | POST | {label} | {elapsed_time:.4f} | {response.status_code}")
    return elapsed_time

def run_benchmark(urls, iterations, labels):
    get_times = {label: [] for label in labels}
    post_times = {label: [] for label in labels}

    for i in range(1, iterations + 1):
        for label in labels:
            get_time = benchmark_get_request(urls[label], i, label)
            post_time = benchmark_post_request(urls[label], i, {"name": f"Sample Item {label} {i}"}, label)

            get_times[label].append(get_time)
            post_times[label].append(post_time)

    return get_times, post_times


def plot_comparison(labels, get_times, post_times):
    iterations = list(range(1, len(get_times[labels[0]]) + 1))
    get_times_ms = {label: [time * 1000 for time in times] for label, times in get_times.items()}
    post_times_ms = {label: [time * 1000 for time in times] for label, times in post_times.items()}

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    for label in labels:
        plt.plot(
            iterations,
            get_times_ms[label],
            marker="o",
            linestyle="-",
            label=f"{label} - GET Request",
        )
        for x, y in zip(iterations, get_times_ms[label]):
            plt.text(x, y, f"{y:.2f}", ha="right", va="bottom")

    plt.xlabel("Iteration")
    plt.ylabel("Time (milliseconds)")
    plt.title("GET Request Comparison")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    for label in labels:
        plt.plot(
            iterations,
            post_times_ms[label],
            marker="o",
            linestyle="-",
            label=f"{label} - POST Request",
        )
        for x, y in zip(iterations, post_times_ms[label]):
            plt.text(x, y, f"{y:.2f}", ha="right", va="bottom")

    plt.xlabel("Iteration")
    plt.ylabel("Time (milliseconds)")
    plt.title("POST Request Comparison")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("comparison.png")


def save_to_csv(filename, labels, get_times, post_times):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        header_row = ["Iteration"]
        for label in labels:
            header_row.extend([
                f"{label} - GET Time (seconds)",
                f"{label} - POST Time (seconds)",
            ])
        writer.writerow(header_row)

        iterations = len(get_times[labels[0]])
        for i in range(iterations):
            row = [i+1]
            for label in labels:
                row.extend([round(get_times[label][i], 2), round(post_times[label][i], 2)])
            writer.writerow(row)


if __name__ == "__main__":
    iterations = int(input("Enter number of iterations: "))
    urls = {
        # "Django": "http://localhost:5000/items/",
        "Go": "http://localhost:8080/items",
        "FastAPI": "http://localhost:8000/items",
    }
    
    labels = list(urls.keys())

    get_times, post_times = run_benchmark(urls, iterations, labels)

    plot_comparison(labels, get_times, post_times)
    save_to_csv("benchmark_results.csv", labels, get_times, post_times)