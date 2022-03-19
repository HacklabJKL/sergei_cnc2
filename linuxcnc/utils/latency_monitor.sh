while true
do
	sleep 0.1
	TMAX=$(halcmd getp hm2_5i25.0.read.tmax)
	if [ $TMAX -ge 500000 ]; then
		halcmd setp hm2_5i25.0.read.tmax 0
		echo -n $TMAX ' '
		date +%H:%M:%S.%N
	fi
	echo $TMAX
done
