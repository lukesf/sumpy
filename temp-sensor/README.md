# Temperature sensor (ds18b20) 
* Read and log temperature sensor via cron job

Wired like this:
![Water proof probe](https://cdn-learn.adafruit.com/assets/assets/000/075/364/original/temperature___humidity_ds18b20-waterproof-40pin_bb.png?1557225868)
  
Notes:
* Temperature sensor is awesome I've used them repeatedly for adjusting for thermal expansion etc simple, no sensitive adc required. 
* need to enable 1 wire interface via raspi-config
* python script reads sensor
* crontab appends to date named file.  

output:
```
> cat ~/raspi-sump/csv/2023-08-24-temp.csv 
2023-08-24 20:13:14, 21.375, 70.475
2023-08-24 20:14:03, 21.437, 70.5866
2023-08-24 20:15:02, 21.375, 70.475
```

## References
* https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
