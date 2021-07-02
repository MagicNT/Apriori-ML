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
			t.add_row([item, round(support, 5), len(item)])
		print(t)
		print("")
		print(" [+] Association Rules: \n")
		t = prettytable.PrettyTable(["Antecedent", "Consequent", "Confidence (>= {})".format(self.min_conf)])
		RULES = sorted(self.rules, key=lambda x: x[1])
		for rule, confidence in RULES:
			ant, cons = rule
			t.add_row([ant, cons, round(confidence, 5)])
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
							self.rules.append(((tuple(element), tuple(diff)), round(confidence, 5)))


def main():
	print("\n" + "="*70)
	print(" Apriori Algrithm")
	print("="*70 + "\n")
	APRIORI = Apriori(filename="retail.dat", min_supp=0.15, min_conf=0.5)
	APRIORI.display()


main()

