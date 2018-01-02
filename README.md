# 黃凱欣的個人秘書

## Setup

### Prerequisite
* Python 3

#### Install Dependency
```sh
pip install -r requirements.txt
```

* pygraphviz (For visualizing Finite State Machine)

### Run Locally

*`ngrok` 


#### Run the sever

```sh
python3 app.py
```

## Finite State Machine
![fsm](./explanation.jpg)

## Usage
The initial state is set to `initial`.

`state0` state (welcome message:你想「加行程」還是「查行程」？) is triggered by any words

* state0
	* Input: santence included "add" or "加"
		* Reply: "什麼時候呢？"
		* .......
		* .......
		* added!

	* Input: santence included "check" or "查"
		* Reply: "想查接下來幾個活動？"
		* ........

## Author
[hoiian](https://github.com/hoiian)
