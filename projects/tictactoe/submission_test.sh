#XXX : Use only this script to test your submission. Exec : ./submission_test.sh your_archive.tar.gz
#/!\ Make sure you have installed python3 and flake8 !

chmod 755 test_no_error.sh
chmod 755 test_optimality.sh
chmod 755 test_style.sh
./test_no_error.sh $1
./test_agent_valid.sh
./test_optimality.sh
./test_style.sh
