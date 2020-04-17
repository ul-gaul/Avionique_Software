python3 -m pycrc --model=crc-16-ccitt --algorithm=bbb  --generate=c -o crc.c
python3 -m pycrc --model=crc-16-ccitt --algorithm=bbb  --generate=h -o crc.h
mv crc.c crc.cpp
