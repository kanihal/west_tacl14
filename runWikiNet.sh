#!/bin/sh

echo "Compiling..."
mvn compile #> /dev/null
mvn dependency:build-classpath -Dmdep.outputFile=classpath.out #> /dev/null
#mkdir output #> /dev/null

for i in `seq 1 8`
do
    echo "############ $i-$((i+1)) ##################" >> WikiCombined.log
    echo "Running HL-MRF-Q on Wiki..."
    #args = joint? train_suff test_suff
    java -Xmx8g -cp ./target/classes:`cat classpath.out` infolab.WikiCombined 0 $i  $((i+1)) | tee -a WikiCombined.log
    # java -Xmx8g -cp ./target/classes:`cat classpath.out` infolab.WikiCombined 1 $i  $((i+1)) | tee -a WikiCombined.log
done
echo "Store output files..."
