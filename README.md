# median_filter
## Author
Bartłomiej Chwiłkowski (chwilko)
[github](https://github.com/chwilko/median_filter)

## Table of contents
- [median\_filter](#median_filter)
  - [Author](#author)
  - [Table of contents](#table-of-contents)
  - [General info](#general-info)
    - [MedianFilter](#medianfilter)
    - [Recorder](#recorder)
  - [Installation](#installation)
    - [download](#download)
    - [setup](#setup)
    - [run](#run)
  - [How to use](#how-to-use)
  - [Package](#package)


## General info
Package implement Producer - Consumer design pattern with a small extension.
This extension is Broker.

Producer produce data for the queue;
Consumer consume data from the queue;
Broker uses data from the first queue to add to the second queue.

Moreover, are implemented special Broker - MedianFilter and special Consumer - Recorder.

### MedianFilter
MedianFilter takes array resize them and applies it median filter.

### Recorder
Recorder save arrays as pictures.


## Installation
### download
```
git clone https://github.com/chwilko/median_filter.git
```
### setup
using `poetry`
```
poetry shell
poetry install
```

or using `pip`
```
pip install --requirement requirement.txt
```
### run
```
python3 main.py
```

## How to use
example using
```
counter = set_n_steps(n_steps)
queue0: Queue = Queue()
queue1: Queue = Queue()

producer = Producer(queue0, lambda: (next(counter), producer_foo), interval)
broker = Broker(queue0, queue1, broker_foo)
consumer = Consumer(queue1, consumer_foo)

producer.start()
broker.start()
consumer.start()

producer.join()
broker.join()
consumer.join()
```
you will see more in the file `main.py`

## Package
* median_filter
  * basic
    * Producer
    * Broker
    * Consumer
  * median_filter
    * MedianFilter
  * recorder 
    * Recorder
  * common
    * StopValue
    * set_n_steps

