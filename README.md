# median_filter

## Author
Bartłomiej Chwiłkowski (chwilko)
[github](https://github.com/chwilko/median_filter)

## license
MIT license

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
Package implements Producer - Consumer design pattern with a small extension.
This extension is Broker.

Producer produces data for the queue;
Consumer consumes data from the queue;
Broker uses data from the first queue to add to the second queue.

Moreover, package implements a special case of Broker (MedianFilter) nad a special case of Consumer (Recorder).

### MedianFilter
MedianFilter takes an array, resize it and applies median filter.

### Recorder
Recorder saves arrays as a pictures.


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
example of usage
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
  * producer
    * Producer
  * broker
    * Broker
  * consumer
    * Consumer
  * worker
    * Worker
  * median_filter
    * MedianFilter
  * recorder 
    * Recorder
  * common
    * set_n_steps

