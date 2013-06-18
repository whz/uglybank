#!/bin/sh


ACCOUNTS=$(cat saldot.txt | awk '{print $3}'| sort | uniq)
echo "---"
for account in $ACCOUNTS; do
	echo $account
	MONTHS=$(cat saldot.txt | grep $account | awk -F "-" '{print $1 "-" $2}'| sort | uniq)
	for month in $MONTHS; do
		echo -n "$month max "
		cat saldot.txt | grep $account | grep "^$month" | awk '{print $4}'|sort -n |tail -n 1
		echo -n "$month min "
		cat saldot.txt | grep $account | grep "^$month" | awk '{print $4}'|sort -n |head -n 1
	done
done
echo "---"
