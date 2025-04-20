# 🔌 Kafka + PySpark Streaming with Docker Compose

This project demonstrates how to run a **real-time data pipeline** using Apache Spark Structured Streaming and Kafka, all containerized with Docker Compose.

---

## 📂 Project Structure

```
.
├── docker-compose.yml
├── spark/
│   ├── Dockerfile
│   └── app/
│       ├── consumer.py
│       └── producer.py
└── README.md
```

---

## 🚀 Quick Start

### 1. Build and start all containers

```bash
docker-compose up --build -d
```

This will spin up:
- Zookeeper
- Kafka broker
- Spark container (custom image with required dependencies)
- Kafka UI (available at http://localhost:8080)

---

### 2. Create Kafka topic manually

Before running the Spark consumer, **manually create the topic** `sensor-data` in the **Kafka UI**:

1. Go to [http://localhost:8080](http://localhost:8080)
2. Select your local Kafka cluster
3. Click "Create Topic"
4. Name: `sensor-data`

---

### 3. Start the Spark Streaming Consumer

Open a terminal and run:

```bash
docker exec -it spark-container bash
spark-submit /app/consumer.py
```

This will launch the Spark application that reads data from the Kafka topic `sensor-data`, parses it, applies windowed aggregations, and prints results to the console.

---

### 4. Start the Producer (Simulated Sensor Data)

In a second terminal window, run:

```bash
docker exec -it spark-container bash
python /app/producer.py
```

This script will send fake sensor readings to Kafka in JSON format.

---

## 🔧 Under the Hood

### Kafka Setup (via Docker Compose)

- `zookeeper` (port 2181)
- `kafka` (port 9092, internal name: `kafka`)
- `kafka-ui` (port 8080)

### Spark Container

Custom image based on `bitnami/spark:3.5.0` with:

- Kafka connectors:
  - `spark-sql-kafka-0-10_2.12-3.5.0.jar`
  - `kafka-clients-3.5.1.jar`
  - `spark-token-provider-kafka-0-10_2.12-3.5.0.jar`
  - `commons-pool2-2.11.1.jar`
- Python libraries:
  - `kafka-python`
  - `pandas`

---

## 📝 Data Format

The Kafka messages are JSON-encoded and follow this schema:

```json
{
  "sensor_id": 1,
  "temperature": 22.5,
  "timestamp": 1713626357
}
```

---

## 📊 Streaming Logic (consumer.py)

- Reads JSON messages from Kafka topic `sensor-data`
- Parses them using defined schema
- Converts Unix timestamps to `event_time`
- Applies **10-second tumbling window aggregation** to calculate average temperature per sensor
- Outputs results to console

---

## 🧪 Helpful Commands

View logs:

```bash
docker-compose logs -f spark
```

List running containers:

```bash
docker ps
```

Stop all containers:

```bash
docker-compose down -v
```