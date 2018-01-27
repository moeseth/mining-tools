export GPU_MAX_HEAP_SIZE=100
export GPU_USE_SYNC_OBJECTS=1
export GPU_MAX_ALLOC_PERCENT=100
export GPU_SINGLE_ALLOC_PERCENT=100

sudo /usr/bin/amdcovc fanspeed:0,1,2,3,4,5=70

sudo /usr/bin/python /home/moe/Desktop/claymore_ether/noethfee.py &> /home/moe/Desktop/claymore_ether/minerfee.log &

/home/moe/Desktop/claymore_ether/ethdcrminer64 -epool eth-asia1.nanopool.org:9999 -ewal 0x0f4f79bdfbb6a3540f7379cf0f708d55c2b1b35d.miner1 -epsw x -mode 1 -mport 0
