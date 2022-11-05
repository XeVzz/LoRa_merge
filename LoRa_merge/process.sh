LoRa_path='./LoRa'
no_path='./no_file'


LoRa_input='/home/mlwu/work/ST_dataset/Banqaio_2021-2022/LoRa'
no_output='/home/mlwu/work/ST_dataset/Banqaio_2021-2022/L0'


./clean.sh
cp $LoRa_input/* $LoRa_path

python3 ./new_merge.py

cp $no_path/* $no_output


