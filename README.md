# Apriori Algorithm

## **Implementation**

### Scripting Language

- Python 3

### Dataset

- The utilized dataset contains anonymized retail market basket data from an anonymous Belgian retail store.
- Dataset link: http://fimi.uantwerpen.be/data/retail.dat

- Dataset excerpt:

```
48,331,332,333,334,335,336,337,338,339
18,37,38,41,48,147,340,341,342,343,344,345,346,347
32,39,41,48,348,349,350
48,351,352,353,354,355,356,357,358,359,360,361,362,363,364
365,366
38,39,41,48,60,367,368,369,370,371,372,373,374,375
1,11,39,41,48,65,89,376,377,378,379,380,381,382,383,384,385
386,387,388,389
38,41,390
38,55,391
32,43,151,152,201,258,340,392,393,394,395,396,397,398,399
338,400,401,402,403,404
39,405,406,407
```

### Import Libraries

- We import the csv Python library to read in the dataset saved inside a CSV file
- We import the itertools Python library to be used for generating subsequence combinations of elements from an input iterable object
- We import the collections Python library to be used for creating dictionary data structures to store, insert and retrieve key-value pairs
- We import the prettytable Python library to present the output results in a nice tabular layout


```python
import csv
import itertools
import collections
import prettytable
```

### Apriori Algorithm Class

We implemented the algorithm in a modular form for better data management as well as better organization. In the initialization function of the class, we specify the required local variables (CSV dataset file name, minimum support value with default 0.15, minimum confidence value with default 0.5) and trigger the dataset importation process as well as the start routine that will kick off the algorithm.


```python
class Apriori:

	def __init__(self, filename, min_supp=0.15, min_conf=0.5):
		self.filename = filename
		self.dataset = self.import_dataset()
		self.min_supp = min_supp
		self.min_conf = min_conf
		self.items = []
		self.rules = []
		self.start()
```

### Importing/Pre-Processing Dataset

In the below routine we import the corresponding dataset file, read in the first 3000 lines from that CSV file and convert each line to an immutable frozenset object initialized with elements from the given row of data. Note that the resulting dataset is saved as a generator object.


```python
	def import_dataset(self):
		with open(self.filename, "rt") as dataset_csvfile:
			dataset_reader = csv.reader(dataset_csvfile, delimiter=",")
			dataset = list(dataset_reader)
			for line in dataset[:3000]:
				entry = frozenset(line)
				yield entry
```

### Calculating Support
Below is the implementation of routine that takes as input parameters an item and the length of the transaction list then calculates the support  and returns its value.


```python
	def calculate_supp(self, item, len_tl):
		return item/len_tl
```

### Subset Combinations

The below implemented routine returns non-empty subsets made up of elements from the passed array (list) parameter.


```python
	def get_subsets(self, arr):
		L = []
		for i, a in enumerate(arr):
			L.append(itertools.combinations(arr, i + 1))
		return itertools.chain(*L)
```

### Items Satisfying Minimum Support

The below implemented routine calculates the support for items in the passed itemset list parameter, then returns a subset of this given itemset having only elements that have support values greater or equal to the provided minimum support value.


```python
	def get_item_min_support(self, itemset, transaction_list, freqset):
		localSet = collections.defaultdict(int)
		for item in itemset:
			for transaction in transaction_list:
				if item.issubset(transaction):
					freqset[item] += 1
					localSet[item] += 1
		_itemset = set()
		for item, count in localSet.items():
			supp = float(count)/len(transaction_list)
			if supp >= self.min_supp:
				_itemset.add(item)
		return _itemset
```

### Joining Set

The below implemented routine joins a given set with itself then returns back to the caller the itemset made up of a specified length of elements that is predetermined through the passed paramater.


```python
	def join_set(self, itemset, length):
		S = []
		for i in itemset:
			for j in itemset:
				x = i.union(j)
				if len(x) == length:
					S.append(x)
		return set(S)
```

### Obtaining Itemset and Transaction List

The below implemented routine loops over the dataset generator and returns an itemset list for each transaction which represents an entry in the dataset.


```python
	def get_itemset_transactionlist(self):
		TL = []
		S = set()
		for entry in self.dataset:
			T = frozenset(entry)
			TL.append(T)
			for item in T:
				S.add(frozenset([item]))
		return S, TL
```

### Displaying Results

The below implemented routine is used to display the final results at the conclusion of the algorithm runtime. Firstly, this function will print the list of itemsets with their support values that satisfy the minimum support condition that we enforced, as well as the length of each itemset. Secondly, this routine will print out the mined association rules by displaying found antecedents and their corresponding consequents along with their confidence values that satisfy the mimimum confidence condition that we initially enforced.


```python
	def display(self):
		print(" [+] Items:")
		t = prettytable.PrettyTable(["Itemset", "Support (>= {})".format(self.min_supp), "Length"])
		ITEMS = sorted(self.items, key=lambda x: x[1])
		for item, support in ITEMS:
			t.add_row([item, round(support, 3), len(item)])
		print(t)
		print("")
		print(" [+] Association Rules:")
		t = prettytable.PrettyTable(["Antecedent", "Consequent", "Confidence (>= {})".format(self.min_conf)])
		RULES = sorted(self.rules, key=lambda x: x[1])
		for rule, confidence in RULES:
			ant, cons = rule
			t.add_row([ant, cons, round(confidence, 3)])
		print(t)
```

### Apriori Algorithm Trigger Routine

The below implemented routine is the lead function that will kick off the apriori algorithm process. As a result of its runtime we accumulate an array of itemsets with each having its support value, and this array will be saved locally onto the class's variables to be called upon in the display function of the class. In addition, we accumulate an array containing each antecedent along with its corresponding consequent and its confidence value, to be saved within the class's local variables for calling upon it later in the display function of the class at the conlusion of the algorithm run.


```python
	def start(self):
		itemset, transaction_list = self.get_itemset_transactionlist()
		freqset = collections.defaultdict(int)
		tempset = {}
		currset = self.get_item_min_support(itemset, transaction_list, freqset)
		i = 2

		while currset != set([]):
			tempset[i-1] = currset
			currset = self.get_item_min_support(self.join_set(currset, i), transaction_list, freqset)
			i += 1

		for x, value in tempset.items():
			for item in value:
				i = tuple(item)
				supp = self.calculate_supp(freqset[item], len(transaction_list))
				self.items.append((i, supp))

		for x, value in list(tempset.items())[1:]:
			for item in value:
				for element in map(frozenset, [x for x in self.get_subsets(item)]):
					diff = item.difference(element)
					if len(diff) > 0:
						item_supp = self.calculate_supp(freqset[item], len(transaction_list))
						element_supp = self.calculate_supp(freqset[element], len(transaction_list))
						confidence = item_supp/element_supp
						if confidence >= self.min_conf:
							self.rules.append(((tuple(element), tuple(diff)), round(confidence, 3)))
```

### Driver Routine

Below is the main driver routine which creates an Apriori object that will import the dataset, then passes the dataset generator over to the local dataset variable within the class, then initiates the algorithm by triggering the start routine of the algorithm which will manage calling the corresponding functions in order. In return, the object has on its initialization routine a call for the displayer function, which will print in a nice way the resulting itemset and the list of association rules.


```python
def main():
	print("\n" + "="*70)
	print(" Apriori Algrithm")
	print("="*70 + "\n")
	APRIORI = Apriori(filename="retail.dat", min_supp=0.15, min_conf=0.5)
	APRIORI.display()
```

### Full Code

Here is the full code put together.


```python
import csv
import itertools
import collections
import prettytable



class Apriori:

	def __init__(self, filename, min_supp=0.15, min_conf=0.5):
		self.filename = filename
		self.dataset = self.import_dataset()
		self.min_supp = min_supp
		self.min_conf = min_conf
		self.items = []
		self.rules = []
		self.start()


	def import_dataset(self):
		with open(self.filename, "rt") as dataset_csvfile:
			dataset_reader = csv.reader(dataset_csvfile, delimiter=",")
			dataset = list(dataset_reader)
			for line in dataset[:3000]:
				entry = frozenset(line)
				yield entry


	def calculate_supp(self, item, len_tl):
		return item/len_tl


	def get_subsets(self, arr):
		L = []
		for i, a in enumerate(arr):
			L.append(itertools.combinations(arr, i + 1))
		return itertools.chain(*L)


	def get_item_min_support(self, itemset, transaction_list, freqset):
		localSet = collections.defaultdict(int)
		for item in itemset:
			for transaction in transaction_list:
				if item.issubset(transaction):
					freqset[item] += 1
					localSet[item] += 1
		_itemset = set()
		for item, count in localSet.items():
			supp = float(count)/len(transaction_list)
			if supp >= self.min_supp:
				_itemset.add(item)
		return _itemset


	def join_set(self, itemset, length):
		S = []
		for i in itemset:
			for j in itemset:
				x = i.union(j)
				if len(x) == length:
					S.append(x)
		return set(S)


	def get_itemset_transactionlist(self):
		TL = []
		S = set()
		for entry in self.dataset:
			T = frozenset(entry)
			TL.append(T)
			for item in T:
				S.add(frozenset([item]))
		return S, TL


	def display(self):
		print(" [+] Items: \n")
		t = prettytable.PrettyTable(["Itemset", "Support (>= {})".format(self.min_supp), "Length"])
		ITEMS = sorted(self.items, key=lambda x: x[1])
		for item, support in ITEMS:
			t.add_row([item, round(support, 3), len(item)])
		print(t)
		print("")
		print(" [+] Association Rules: \n")
		t = prettytable.PrettyTable(["Antecedent", "Consequent", "Confidence (>= {})".format(self.min_conf)])
		RULES = sorted(self.rules, key=lambda x: x[1])
		for rule, confidence in RULES:
			ant, cons = rule
			t.add_row([ant, cons, round(confidence, 3)])
		print(t)


	def start(self):
		itemset, transaction_list = self.get_itemset_transactionlist()
		freqset = collections.defaultdict(int)
		tempset = {}
		currset = self.get_item_min_support(itemset, transaction_list, freqset)
		i = 2

		while currset != set([]):
			tempset[i-1] = currset
			currset = self.get_item_min_support(self.join_set(currset, i), transaction_list, freqset)
			i += 1

		for x, value in tempset.items():
			for item in value:
				i = tuple(item)
				supp = self.calculate_supp(freqset[item], len(transaction_list))
				self.items.append((i, supp))

		for x, value in list(tempset.items())[1:]:
			for item in value:
				for element in map(frozenset, [x for x in self.get_subsets(item)]):
					diff = item.difference(element)
					if len(diff) > 0:
						item_supp = self.calculate_supp(freqset[item], len(transaction_list))
						element_supp = self.calculate_supp(freqset[element], len(transaction_list))
						confidence = item_supp/element_supp
						if confidence >= self.min_conf:
							self.rules.append(((tuple(element), tuple(diff)), round(confidence, 3)))


def main():
	print("\n" + "="*70)
	print(" Apriori Algrithm")
	print("="*70 + "\n")
	APRIORI = Apriori(filename="retail.dat", min_supp=0.15, min_conf=0.5)
	APRIORI.display()


main()
```

### Output

    
    ======================================================================
     Apriori Algrithm
    ======================================================================
    
     [+] Items: 
    
    +--------------+-------------------+--------+
    |   Itemset    | Support (>= 0.15) | Length |
    +--------------+-------------------+--------+
    |   ('32',)    |       0.167       |   1    |
    | ('39', '41') |       0.201       |   2    |
    |   ('38',)    |       0.202       |   1    |
    |   ('41',)    |       0.263       |   1    |
    | ('39', '48') |       0.305       |   2    |
    |   ('48',)    |       0.439       |   1    |
    |   ('39',)    |       0.569       |   1    |
    +--------------+-------------------+--------+
    
     [+] Association Rules: 
    
    +------------+------------+---------------------+
    | Antecedent | Consequent | Confidence (>= 0.5) |
    +------------+------------+---------------------+
    |  ('39',)   |  ('48',)   |        0.536        |
    |  ('48',)   |  ('39',)   |        0.695        |
    |  ('41',)   |  ('39',)   |        0.763        |
    +------------+------------+---------------------+


