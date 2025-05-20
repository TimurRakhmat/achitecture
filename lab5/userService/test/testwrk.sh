echo "      1 thread:"
echo "With redis:"
wrk -d 10 -t 1 -c 10 --latency -s getredis.lua http://localhost:8000
echo "Without redis:"
wrk -d 10 -t 1 -c 10 --latency -s get.lua http://localhost:8000
echo "      5 threads:"
echo "With redis:"
wrk -d 10 -t 5 -c 10 --latency -s getredis.lua http://localhost:8000
echo "Without redis:"
wrk -d 10 -t 5 -c 10 --latency -s get.lua http://localhost:8000
echo "      10 threads:"
echo "With redis:"
wrk -d 10 -t 10 -c 10 --latency -s getredis.lua http://localhost:8000
echo "Without redis:"
wrk -d 10 -t 10 -c 10 --latency -s get.lua http://localhost:8000