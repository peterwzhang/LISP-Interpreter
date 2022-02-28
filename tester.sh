#! /bin/sh

numTests=18 # UPDATE THIS TO THE NUMBER OF TESTS
sucesses=0

getInput() {
    echo "Enter which test case you would like to run, or \"ALL\" to run all tests: "
    read -r num
}

runTest() {
    echo "Running test case $1"
    ./tester/kamincpp.out < tester/tests/test"$1".txt > tester/tests/test"$1".out
    python3 src/project1.py < tester/tests/test"$1".txt > tester/tests/test"$1".ans
    matchedLines=$(diff -w -y --suppress-common-lines "tester/tests/test$1.ans" "tester/tests/test$1.out" | wc -l | tr -d '[:space:]')
    if [ "$matchedLines" -eq "0" ]; then
        echo "Test case $1 passed"
        sucesses=$((sucesses+1))
    else
        echo "Test case $1 failed"
    fi
}

test() {
    if [ "$1" = "ALL" ]; then
        for i in $(seq 1 $numTests); do
            runTest "$i"
        done
    else
        runTest "$1"
        numTests=1
    fi
    echo "Number of tests passed: $sucesses/$numTests"
}

getInput
test "$num"