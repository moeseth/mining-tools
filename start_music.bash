export GPU_MAX_HEAP_SIZE=100
export GPU_USE_SYNC_OBJECTS=1
export GPU_MAX_ALLOC_PERCENT=100
export GPU_SINGLE_ALLOC_PERCENT=100

./ethdcrminer64 -epool stratum+tcp://music.minerpool.net:8009 -ewal 0x0f4f79bdfbb6a3540f7379cf0f708d55c2b1b35d -epsw x -allpools 1 -allcoins -gser 2 -eworker miner1
